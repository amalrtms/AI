import time

def get_moves(board):
    pos = board.index('_')
    moves_map = {
        0: [1, 3],
        1: [0, 2, 4],
        2: [1, 5],
        3: [0, 4, 6],
        4: [1, 3, 5, 7],
        5: [2, 4, 8],
        6: [3, 7],
        7: [4, 6, 8],
        8: [5, 7],
    }
    return moves_map[pos]

def depth_first(start, goal, limit=20, max_states=5000):
    stack = [(start, [], 0)]
    seen = {tuple(start)}
    count = 0
    t_start = time.time()

    while stack:
        state, path, depth = stack.pop()
        if depth > limit or count > max_states:
            continue

        count += 1
        if state == goal:
            return path, count

        for nxt in reversed(get_moves(state)):
            new_board = list(state)
            blank = new_board.index('_')
            new_board[blank], new_board[nxt] = new_board[nxt], new_board[blank]
            if tuple(new_board) not in seen:
                seen.add(tuple(new_board))
                stack.append((new_board, path + [new_board], depth + 1))

        if time.time() - t_start > 5:  # stop after 5 seconds
            break

    return None, count


start_state = [1, 2, 3,
               4, 8, '_',
               7, 6, 5]

goal_state = [1, 2, 3,
              4, 5, 6,
              7, 8, '_']

t0 = time.time()
result, total = depth_first(start_state, goal_state, limit=20)
t1 = time.time()

if result:
    print("Path to goal:")
    for i, step in enumerate(result, 1):
        print(f"Step {i}: {step}")
else:
    print("No path found or limit reached.")

print("\nTime: {:.6f} seconds".format(t1 - t0))
print("States visited:", total)
