import time

def get_moves(board):
    pos = board.index('_')
    moves = {
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
    return moves[pos]

def limited_dfs(state, goal, depth, route, seen):
    if state == goal:
        return route
    if depth == 0:
        return None

    seen.add(tuple(state))
    for move in get_moves(state):
        nxt = list(state)
        blank = nxt.index('_')
        nxt[blank], nxt[move] = nxt[move], nxt[blank]
        if tuple(nxt) not in seen:
            found = limited_dfs(nxt, goal, depth - 1, route + [nxt], seen)
            if found:
                return found
    return None

def iterative_dfs(start, goal, limit=20):
    for d in range(limit + 1):
        seen = set()
        result = limited_dfs(start, goal, d, [start], seen)
        if result:
            return result, d
    return None, limit

start = [1, 2, 3,
         4, 8, '_',
         7, 6, 5]

goal = [1, 2, 3,
        4, 5, 6,
        7, 8, '_']

t0 = time.time()
path, depth = iterative_dfs(start, goal, limit=20)
t1 = time.time()

if path:
    print("Path found:")
    for i, p in enumerate(path):
        print(f"Step {i}: {p}")
else:
    print("Goal not found within depth limit.")

print("\nRuntime: {:.6f} seconds".format(t1 - t0))
print("Depth explored:", depth)
