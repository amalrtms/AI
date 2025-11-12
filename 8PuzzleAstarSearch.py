from heapq import heappush, heappop

GOAL_STATE = (
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 0)
)

def is_solvable(state):
    flattened = [tile for row in state for tile in row if tile != 0]
    inversions = 0
    for i in range(len(flattened)):
        for j in range(i + 1, len(flattened)):
            if flattened[i] > flattened[j]:
                inversions += 1
    return inversions % 2 == 0

def get_target_position(tile):
    for r, row in enumerate(GOAL_STATE):
        for c, val in enumerate(row):
            if val == tile:
                return r, c

def get_manhattan_distance(state):
    distance = 0
    for r, row in enumerate(state):
        for c, tile in enumerate(row):
            if tile != 0:
                tr, tc = get_target_position(tile)
                distance += abs(tr - r) + abs(tc - c)
    return distance

def valid_moves(state):
    for r, row in enumerate(state):
        for c, tile in enumerate(row):
            if tile == 0:
                blank_r, blank_c = r, c
    moves = []
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nr, nc = blank_r + dr, blank_c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            moves.append((nr, nc))
    return moves

def apply_move(state, move):
    blank_pos = None
    for r, row in enumerate(state):
        for c, tile in enumerate(row):
            if tile == 0:
                blank_pos = (r, c)
    r_blank, c_blank = blank_pos
    r_move, c_move = move
    new_state = [list(row) for row in state]
    new_state[r_blank][c_blank], new_state[r_move][c_move] = new_state[r_move][c_move], new_state[r_blank][c_blank]
    return tuple(tuple(row) for row in new_state)

class Node:
    def __init__(self, state, parent, g, f):
        self.state = state
        self.parent = parent
        self.g = g
        self.f = f
    def __lt__(self, other):
        return self.f < other.f

def reconstruct_path(node):
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    return path[::-1]

def get_misplaced_tiles(state):
    misplaced = 0
    for r, row in enumerate(state):
        for c, tile in enumerate(row):
            if tile != 0 and tile != GOAL_STATE[r][c]:
                misplaced += 1
    return misplaced

def a_star_search(start_state, heuristic_type="manhattan"):
    if not is_solvable(start_state):
        return None
    open_list = []
    closed_set = set()
    if heuristic_type == "manhattan":
        h = get_manhattan_distance(start_state)
    else:
        h = get_misplaced_tiles(start_state)
    start_node = Node(start_state, None, 0, h)
    heappush(open_list, start_node)
    while open_list:
        current_node = heappop(open_list)
        if current_node.state == GOAL_STATE:
            return reconstruct_path(current_node)
        closed_set.add(current_node.state)
        for move in valid_moves(current_node.state):
            child_state = apply_move(current_node.state, move)
            if child_state in closed_set:
                continue
            g = current_node.g + 1
            if heuristic_type == "manhattan":
                h = get_manhattan_distance(child_state)
            else:
                h = get_misplaced_tiles(child_state)
            f = g + h
            heappush(open_list, Node(child_state, current_node, g, f))
    return None

start = (
    (1, 2, 3),
    (4, 5, 6),
    (0, 7, 8)
)

path = a_star_search(start, "manhattan")
if path:
    for step in path:
        for row in step:
            print(row)
        print()
else:
    print("No solution found.")
