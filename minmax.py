import math

def minimax_decision(state, player):
    def max_value(state):
        if terminal_test(state):
            return utility(state)
        v = float('-inf')
        for a in actions(state):
            v = max(v, min_value(result(state, a, 'X')))
        return v

    def min_value(state):
        if terminal_test(state):
            return utility(state)
        v = float('inf')
        for a in actions(state):
            v = min(v, max_value(result(state, a, 'O')))
        return v

    best_score = float('-inf')
    best_action = None
    for a in actions(state):
        v = min_value(result(state, a, player))
        if v > best_score:
            best_score = v
            best_action = a
    return best_action

def actions(state):
    return [i for i, v in enumerate(state) if v == ' ']

def result(state, action, player):
    new_state = state.copy()
    new_state[action] = player
    return new_state

def utility(state):
    for (x, y, z) in [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                      (0, 3, 6), (1, 4, 7), (2, 5, 8),
                      (0, 4, 8), (2, 4, 6)]:
        if state[x] == state[y] == state[z] != ' ':
            return 1 if state[x] == 'X' else -1
    return 0

def terminal_test(state):
    if ' ' not in state or utility(state) != 0:
        return True
    return False

def print_board(state):
    for i in range(0, 9, 3):
        print(state[i] + '|' + state[i+1] + '|' + state[i+2])
    print()

state = [' '] * 9
current_player = 'X'

while not terminal_test(state):
    if current_player == 'X':
        move = minimax_decision(state, 'O')
        state[move] = 'X'
    else:
        move = int(input("Enter your move (0-8): "))
        if state[move] != ' ':
            continue
        state[move] = 'O'
    print_board(state)
    current_player = 'O' if current_player == 'X' else 'X'

if utility(state) == 1:
    print("X wins!")
elif utility(state) == -1:
    print("O wins!")
else:
    print("Draw!")
