import random
import math

# Heuristic: number of pairs of queens attacking each other
def calculate_cost(state):
    cost = 0
    n = len(state)
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                cost += 1
    return cost


# Generate all neighbors of the current state
def get_neighbors(state):
    neighbors = []
    n = len(state)
    for col in range(n):
        for row in range(n):
            if state[col] != row:  # move queen in col to new row
                neighbor = state.copy()
                neighbor[col] = row
                neighbors.append(neighbor)
    return neighbors


# Simulated Annealing algorithm
def simulated_annealing(initial_state, initial_temp=100, cooling_rate=0.95, max_iter=1000):
    current = initial_state
    current_cost = calculate_cost(current)
    temperature = initial_temp

    print(f"Initial state: {current}, Cost = {current_cost}, Temperature = {temperature}")

    for iteration in range(max_iter):
        # Generate neighbors and calculate their costs
        neighbors = get_neighbors(current)
        next_state = random.choice(neighbors)
        next_cost = calculate_cost(next_state)

        # Calculate the difference in energy (deltaE)
        deltaE = next_cost - current_cost

        # Accept the move with the Metropolis criterion
        if deltaE < 0 or random.random() < math.exp(-deltaE / temperature):
            current = next_state
            current_cost = next_cost
            print(f"Move to: {current}, Cost = {current_cost}, deltaE = {deltaE}, Temperature = {temperature}")

        # Decrease the temperature
        temperature *= cooling_rate

        # If the cost is 0, solution is found
        if current_cost == 0:
            print(f"Final state: {current}, Cost = {current_cost}")
            print("✅ Goal state reached!")
            return current, current_cost

    print("❌ Solution not found within maximum iterations.")
    return current, current_cost


# Example usage
if __name__ == "__main__":
    n = int(input("Enter number of queens (N): "))
    print("Enter initial state as space-separated row positions for each column.")
    print("Example for N=4: '1 3 0 2' means queen at (0,1), (1,3), (2,0), (3,2).")

    initial_state = list(map(int, input("Initial state: ").split()))

    if len(initial_state) != n:
        print("❌ Invalid input: Length of initial state must be N.")
    else:
        solution, cost = simulated_annealing(initial_state)

        if cost == 0:
            print("✅ Goal state reached!")
        else:
            print("❌ Solution not found within the time limit.")
