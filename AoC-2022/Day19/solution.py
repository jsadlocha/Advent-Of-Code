demo = """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
"""
import re

inp = demo
inp = open('input.txt').read()
inp = inp.splitlines()

recipe = []
mineralMaxCost = []

def dfs(time, cache, robots, minerals):
  if time == 0:
    return minerals[3]

  key = tuple([time, *robots, *minerals])
  if key in cache:
    return cache[key]

  max_val = minerals[3] + robots[3] * time
  
  for btype, rec in enumerate(recipe):
    if btype != 3 and robots[btype] >= mineralMaxCost[btype]:
      continue

    wait = 0
    for ramt, rtype in rec:
      if robots[rtype] == 0:
        break
      wait = max(wait, -(-(ramt - minerals[rtype]) // robots[rtype]))
    else:
      remtime = time - wait - 1
      if remtime <= 0:
        continue
      bots_ = robots[:]
      amt_ = [x + y * (wait + 1) for x, y in zip(minerals, robots)]
      for ramt, rtype in rec:
        amt_[rtype] -= ramt
      bots_[btype] += 1
      for i in range(3):
        amt_[i] = min(amt_[i], mineralMaxCost[i] * remtime)
      max_val = max(max_val, dfs(remtime, cache, bots_, amt_))
 
  cache[key] = max_val 
  return max_val

# bp_list->recipe->robot_id->(mineral_cost, mineraltype)
mineralList = ['ore', 'clay', 'obsidian']
total = 0
for idx, line in enumerate(inp):
  recipe = []
  mineralMaxCost = [0, 0, 0, 0]
  for r_id, robot in enumerate(line.split('Each')[1:]):
    r = []
    for cost, mineral in re.findall(r'(\d+) (\w+)', robot):
      index_mineral = mineralList.index(mineral)
      mineralMaxCost[index_mineral] = max(int(cost), mineralMaxCost[index_mineral])
      r.append((int(cost), index_mineral))
    recipe.append(r)

  maxGeode = dfs(24, {}, [1,0,0,0], [0,0,0,0])
  print(f'id: {idx} max geode: {maxGeode}')
  total += (idx+1) * maxGeode

total2 = 1
for idx, line in enumerate(inp):
  recipe = []
  mineralMaxCost = [0, 0, 0, 0]
  for r_id, robot in enumerate(line.split('Each')[1:]):
    r = []
    for cost, mineral in re.findall(r'(\d+) (\w+)', robot):
      index_mineral = mineralList.index(mineral)
      mineralMaxCost[index_mineral] = max(int(cost), mineralMaxCost[index_mineral])
      r.append((int(cost), index_mineral))
    recipe.append(r)

  maxGeode = dfs(32, {}, [1,0,0,0], [0,0,0,0])
  print(f'id: {idx} max geode: {maxGeode}')
  total2 *= maxGeode

  if idx == 2:
    break

print(f'Solution1: {total}')
print(f'Solution2: {total2}')


  