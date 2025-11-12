def show_grid(grid):
    print()
    for r in range(3):
        print(" | ".join(grid[r*3:(r+1)*3]))
        if r < 2:
            print("-" * 9)
    print()

def has_winner(grid, symbol):
    patterns = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for p in patterns:
        if all(grid[i] == symbol for i in p):
            return True
    return False

grid = [" "] * 9
turn = "X"
show_grid(grid)

while True:
    move = input(f"Turn for {turn}. Pick a position (1-9): ")
    if move.isdigit():
        idx = int(move) - 1
        if 0 <= idx < 9 and grid[idx] == " ":
            grid[idx] = turn
        else:
            print("Invalid spot. Try again.")
            continue
    else:
        print("Enter a number.")
        continue

    show_grid(grid)

    if has_winner(grid, turn):
        print(f"{turn} wins the game!")
        break
    if " " not in grid:
        print("Game tied!")
        break

    turn = "O" if turn == "X" else "X"
