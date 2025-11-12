from graphviz import Digraph
from IPython.display import display

class Node:
    def __init__(self, value=None, children=None):
        self.value = value        # leaf nodes have value
        self.children = children  # internal nodes have children list
        self.id = id(self)        # unique id for graphviz


def build_tree(leaf_values):
    leaves = [Node(value=v) for v in leaf_values]

    max1 = Node(children=leaves[0:2])
    max2 = Node(children=leaves[2:4])
    max3 = Node(children=leaves[4:6])
    max4 = Node(children=leaves[6:8])

    min1 = Node(children=[max1, max2])
    min2 = Node(children=[max3, max4])

    root = Node(children=[min1, min2])
    return root


def alpha_beta(node, depth, alpha, beta, maximizing_player, path, pruned_paths):
    if node.value is not None:
        path.append(node.value)
        return node.value, path

    if maximizing_player:
        max_eval = float('-inf')
        best_path = None
        for child in node.children:
            val, child_path = alpha_beta(child, depth + 1, alpha, beta, False, path.copy(), pruned_paths)
            if val > max_eval:
                max_eval = val
                best_path = child_path
            alpha = max(alpha, val)
            if beta <= alpha:
                idx = node.children.index(child)
                for prune_child in node.children[idx + 1:]:
                    collect_pruned(prune_child, pruned_paths)
                break
        return max_eval, best_path
    else:
        min_eval = float('inf')
        best_path = None
        for child in node.children:
            val, child_path = alpha_beta(child, depth + 1, alpha, beta, True, path.copy(), pruned_paths)
            if val < min_eval:
                min_eval = val
                best_path = child_path
            beta = min(beta, val)
            if beta <= alpha:
                idx = node.children.index(child)
                for prune_child in node.children[idx + 1:]:
                    collect_pruned(prune_child, pruned_paths)
                break
        return min_eval, best_path


def collect_pruned(node, pruned_paths):
    if node.value is not None:
        pruned_paths.append(node)
    else:
        for child in node.children:
            collect_pruned(child, pruned_paths)


def visualize_tree(node, pruned_nodes, dot=None):
    if dot is None:
        dot = Digraph()
    
    label = str(node.value) if node.value is not None else ""
    color = 'red' if node in pruned_nodes else 'black'
    
    dot.node(str(node.id), label=label, color=color, fontcolor=color)
    
    if node.children:
        for child in node.children:
            visualize_tree(child, pruned_nodes, dot)
            dot.edge(str(node.id), str(child.id))
    
    return dot


if __name__ == "__main__":
    print("Enter 8 leaf node values (left to right):")
    leaves = [int(input(f"Leaf {i + 1}: ")) for i in range(8)]

    tree = build_tree(leaves)
    pruned = []
    value, path = alpha_beta(tree, 0, float('-inf'), float('inf'), True, [], pruned)

    print(f"\nValue at root node: {value}")
    print(f"Path from root to best leaf: {path}")
    print(f"Pruned leaf nodes: {[n.value for n in pruned] if pruned else 'No nodes pruned'}")

    # Inline visualization
    dot = visualize_tree(tree, pruned)
    display(dot)  # This will display the tree directly in Jupyter/Colab
