import random
import matplotlib.pyplot as plt
from IPython.display import clear_output
import time

# 🎚️ You can change this to slow down or speed up the animation
DELAY = 0.8  # seconds between frames (try 0.3–1.5)

def compute_conflicts(board):
    """Calculate the number of attacking pairs of queens."""
    conflicts = 0
    n = len(board)
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1
    return conflicts

def get_best_neighbor(board):
    """Find the neighbor with the fewest conflicts."""
    n = len(board)
    best_board = board[:]
    best_conflicts = compute_conflicts(board)
    
    for col in range(n):
        original_row = board[col]
        for row in range(n):
            if row != original_row:
                new_board = board[:]
                new_board[col] = row
                new_conflicts = compute_conflicts(new_board)
                if new_conflicts < best_conflicts:
                    best_conflicts = new_conflicts
                    best_board = new_board
    return best_board, best_conflicts

def draw_board(board, step, conflicts, restart):
    """Visualize the board using matplotlib (Colab-compatible)."""
    n = len(board)
    clear_output(wait=True)
    plt.figure(figsize=(5, 5))
    plt.title(f"Restart {restart} | Step {step}\nConflicts: {conflicts}")
    plt.xlim(-0.5, n - 0.5)
    plt.ylim(-0.5, n - 0.5)
    plt.gca().set_xticks(range(n))
    plt.gca().set_yticks(range(n))
    plt.grid(True)
    
    # Draw queens (red = in conflict, green = safe)
    for col in range(n):
        row = board[col]
        color = "green"
        for c2 in range(n):
            if c2 != col:
                if board[c2] == row or abs(board[c2] - row) == abs(c2 - col):
                    color = "red"
                    break
        plt.plot(col, row, "o", color=color, markersize=20)
    
    plt.show()
    time.sleep(DELAY)

def hill_climbing_visual_all_trials(n, max_restarts=50):
    """Hill climbing algorithm that visualizes all trials."""
    for restart in range(1, max_restarts + 1):
        board = [random.randint(0, n - 1) for _ in range(n)]
        current_conflicts = compute_conflicts(board)
        step = 0
        
        # Print summary for each restart
        print(f"\n🚀 Starting Restart #{restart}")
        time.sleep(1)
        
        while True:
            draw_board(board, step, current_conflicts, restart)
            neighbor, neighbor_conflicts = get_best_neighbor(board)
            
            if neighbor_conflicts >= current_conflicts:
                print(f"🔸 Local optimum reached at Restart {restart}, Step {step} (Conflicts = {current_conflicts})")
                time.sleep(1.5)
                break  # Stop exploring this restart
            
            board = neighbor
            current_conflicts = neighbor_conflicts
            step += 1
        
        if current_conflicts == 0:
            draw_board(board, step, 0, restart)
            print(f"✅ Solution found after {restart} restarts!")
            return board
        
        time.sleep(1.0)
    
    print("\n❌ No solution found after maximum restarts.")
    return None

# Run it
n = int(input("Enter N for N-Queens: "))
hill_climbing_visual_all_trials(n)
