import random

zones = [1, 1, 1, 1]
bot = int(input("Enter start position (1-4): ")) - 1
visited = []
steps = 0

def next_spot(current):
    while True:
        new_pos = random.randint(0, 3)
        if new_pos != current and new_pos not in visited:
            return new_pos

while True:
    print(zones)
    print("Bot at:", bot + 1)

    if zones[bot] == 1:
        zones[bot] = 0
        visited.append(bot)
        steps += 1
        if len(visited) == 4:
            break
        bot = next_spot(bot)
    else:
        visited.append(bot)
        if len(visited) == 4:
            break
        bot = next_spot(bot)

print("Total steps:", steps)
