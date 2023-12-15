demo = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""

import functools as tl

inp = demo
inp = open('input.txt').read()
inp = inp.split('\n')[:-1]

solution1 = 0
solution2 = 0
valid_game = True
contrainst = { "red": 12, "green": 13, "blue": 14}
max_dict = { "red": 0, "blue": 0, "green": 0}
for gameid, game in enumerate(inp):
    info = game.split(': ')[1]
    sets = info.split('; ')
    for el in sets:
        cubes = el.split(', ')
        for cube in cubes:
            number, color = cube.split(' ')
            max_dict[color] = max(int(number), max_dict[color])
            if int(number) > contrainst[color]:
                valid_game = False
    if valid_game:
        solution1 += gameid+1
    valid_game = True
    solution2 += tl.reduce(lambda x,y: x*y, max_dict.values())
    max_dict = { "red": 0, "blue": 0, "green": 0}

print(solution1)
print(solution2)
