import copy

def calculate_manhattan_distance(current, goal):
    distance = 0
    for row in range(3):
        for col in range(3):
            if current[row][col] != 0:
                goal_x, goal_y = divmod(goal.index(current[row][col]), 3)
                distance += abs(goal_x - row) + abs(goal_y - col)
    return distance

def locate_blank_tile(state):

    for row in range(3):
        for col in range(3):
            if state[row][col] == 0:
                return row, col

def possible_moves(state):

    moves = []
    blank_row, blank_col = locate_blank_tile(state)
    shifts = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dx, dy in shifts:
        new_row, new_col = blank_row + dx, blank_col + dy
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            next_state = copy.deepcopy(state)
            next_state[blank_row][blank_col], next_state[new_row][new_col] = (
                next_state[new_row][new_col],
                next_state[blank_row][blank_col],
            )
            moves.append(next_state)

    return moves

def hill_climbing_search(start, goal):

    current_state = start
    goal_flat = [tile for row in goal for tile in row]
    solution_path = [current_state]

    while True:
        current_flat = [tile for row in current_state for tile in row]
        current_score = calculate_manhattan_distance(current_state, goal_flat)

        neighbors = possible_moves(current_state)
        scored_neighbors = [
            (calculate_manhattan_distance(neighbor, goal_flat), neighbor)
            for neighbor in neighbors
        ]
        scored_neighbors.sort()

        best_score, best_state = scored_neighbors[0]

        if best_score < current_score:
            current_state = best_state
            solution_path.append(current_state)
        else:
            break

    return solution_path, current_score

def display_solution(steps):

    for idx, state in enumerate(steps):
        print(f"Step {idx}:")
        for row in state:
            print(row)
        print()

if __name__ == "__main__":
    initial_state = [
        [1, 2, 3],
        [5, 0, 6],
        [4, 7, 8],
    ]

    goal_state = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0],
    ]

    solution_steps, final_heuristic = hill_climbing_search(initial_state, goal_state)

    print("Steps to solve the puzzle:")
    display_solution(solution_steps)

    if final_heuristic == 0:
        print("Solution successfully found!")
    else:
        print("Algorithm stuck at a local maxima or plateau. Solution not found.")
