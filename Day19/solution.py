demo = """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
"""
import re
import gc
# import psutil

inp = demo
# inp = open('input.txt').read()
inp = inp.splitlines()

recipe = []
mineralMaxCost = []

def dfs(time, cache, robots, minerals):
  if time == 0:
    return minerals[3]

  key = (time, tuple(robots), tuple(minerals))
  if key in cache:
   return cache[key]

  max_val = 0
  for id, r in enumerate(recipe):
    if id != 3 and robots[id] >= mineralMaxCost[id]:
     continue
    for cost, mtyp in r:
      if cost > minerals[mtyp]:
        break
    else:
      m = minerals[:]
      rob = robots[:]
      for cost, mtyp in r:
        m[mtyp] -= cost
      rob[id] += 1

      for id, r in enumerate(robots):
        m[id] += r

      max_val = max(max_val, dfs(time-1, cache, rob, m))

  cache[key] = max_val 

  for id, r in enumerate(robots):
      minerals[id] += r
  max_val = max(max_val, dfs(time-1, cache, robots[:], minerals[:]))
  #if time == 13:
  # gc.collect()
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
  gc.collect()


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
  gc.collect()
  
  if idx == 3:
    break

print(f'Solution1: {total}')
print(f'Solution2: {total2}')


  