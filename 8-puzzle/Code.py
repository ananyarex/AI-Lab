import copy
import time

# Define the goal state
GOAL_STATE =[[1, 2, 3],
              [4, 5, 6],
              [7, 8, 0]] 

# Directions: up, down, left, right
DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def find_zero(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j
    return -1, -1

def is_goal(state):
    return state == GOAL_STATE

def get_neighbors(state):
    neighbors = []
    x, y = find_zero(state)

    for dx, dy in DIRS:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = copy.deepcopy(state)
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            neighbors.append(new_state)
    return neighbors

def iddfs(start_state):
    depth = 0
    while True:
        visited = set()
        path = []
        found, result_path = dls(start_state, depth, visited, path)
        if found:
            return result_path
        depth += 1

def dls(state, depth, visited, path):
    state_key = str(state)
    if state_key in visited:
        return False, []
    visited.add(state_key)
    path.append(state)

    if is_goal(state):
        return True, path

    if depth == 0:
        path.pop()
        return False, []

    for neighbor in get_neighbors(state):
        found, result_path = dls(neighbor, depth - 1, visited, path)
        if found:
            return True, result_path

    path.pop()
    return False, []

# Example usage:
start_state = [[1, 2, 3],
               [0, 4, 6],
               [7, 5, 8]]

start_time = time.time()
solution_path = iddfs(start_state)
end_time = time.time()
runtime = end_time - start_time

if solution_path:
    print("Solution found in", len(solution_path) - 1, "moves.")
    for step in solution_path:
        for row in step:
            print(row)
        print()
    print(f"Runtime: {runtime:.6f} seconds")
else:
    print("No solution found.")
    print(f"Runtime: {runtime:.6f} seconds")
