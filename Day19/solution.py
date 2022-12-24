demo = """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
"""
import re
inp = demo
# inp = open('input.txt').read()
inp = inp.splitlines()

def dfs(time, cache, recipe, robots, minerals):
  if time == 0:
    return minerals[3] # return goede amount
  


# bp_list->recipe->robot_id->(mineral_cost, mineraltype)
bp = []
mineralList = ['ore', 'clay', 'obsidian']
total = 0
for idx, line in enumerate(inp):
  recipe = []
  for robot in line.split('Each')[1:]:
    r = []
    for cost, mineral in re.findall(r'(\d+) (\w+)', robot):
      r.append((int(cost), mineralList.index(mineral)))
    recipe.append(r)
  bp.append(recipe)

  maxGeode = dfs(24, {}, recipe, [1,0,0,0], [0,0,0,0])
  total += (idx+1) * maxGeode

print(f'Solution1: {total}')
  