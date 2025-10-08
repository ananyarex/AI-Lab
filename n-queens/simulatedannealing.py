import random
import math
import matplotlib.pyplot as plt
from IPython.display import clear_output
import time

# You can adjust this delay for visualization speed (0.2–1.0 works well)
DELAY = 0.5  

def compute_conflicts(board):
    """Count number of attacking pairs of queens."""
    conflicts = 0
    n = len(board)
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1
    return conflicts

def random_neighbor(board):
    """Generate a random neighboring state by moving one queen."""
    n = len(board)
    new_board = board[:]
    col = random.randint(0, n - 1)
    new_row = random.randint(0, n - 1)
    new_board[col] = new_row
    return new_board

def draw_board(board, step, temp, conflicts):
    """Draw the chessboard in Colab-friendly way."""
    n = len(board)
    clear_output(wait=True)
    plt.figure(figsize=(5, 5))
    plt.title(f"Step {step} | Temp={temp:.4f} | Conflicts={conflicts}")
    plt.xlim(-0.5, n - 0.5)
    plt.ylim(-0.5, n - 0.5)
    plt.gca().set_xticks(range(n))
    plt.gca().set_yticks(range(n))
    plt.grid(True)

    for col in range(n):
        row = board[col]
        color = "green"
        for c2 in range(n):
            if c2 != col and (board[c2] == row or abs(board[c2] - row) == abs(c2 - col)):
                color = "red"
                break
        plt.plot(col, row, "o", color=color, markersize=20)

    plt.show()
    time.sleep(DELAY)

def simulated_annealing(n, initial_temp=100, cooling_rate=0.99, min_temp=0.001, visualize=True):
    """Simulated Annealing algorithm for N-Queens."""
    board = [random.randint(0, n - 1) for _ in range(n)]
    current_conflicts = compute_conflicts(board)
    temp = initial_temp
    step = 0

    best_board = board[:]
    best_conflicts = current_conflicts

    while temp > min_temp and current_conflicts > 0:
        neighbor = random_neighbor(board)
        neighbor_conflicts = compute_conflicts(neighbor)
        delta = neighbor_conflicts - current_conflicts

        # Accept neighbor if better OR with probability exp(-Δ/T)
        if delta < 0 or random.random() < math.exp(-delta / temp):
            board = neighbor
            current_conflicts = neighbor_conflicts

            if current_conflicts < best_conflicts:
                best_board = board[:]
                best_conflicts = current_conflicts

        if visualize:
            draw_board(board, step, temp, current_conflicts)

        temp *= cooling_rate
        step += 1

    if current_conflicts == 0:
        print(f"✅ Solution found in {step} steps!")
    else:
        print(f"⚠️ Ended with {current_conflicts} conflicts after {step} steps (temp={temp:.4f})")

    draw_board(board, step, temp, current_conflicts)
    return board

# Run it
n = int(input("Enter N for N-Queens: "))
simulated_annealing(n)
