from dataclasses import dataclass
import regex as re
import numpy as np
import copy

@dataclass
class Monkey:
  item_list: list
  op_string: str
  test_string: str
  divide: int
  throw_count: int = 0

  def op(self, x: int, y: int = 1) -> int:
    return eval(self.op_string)

  def test(self, x: int) -> int:
    return eval(self.test_string)

  def throw_list(self, lcm: int, div: int) -> list:
    mon_item = []
    for item in self.item_list:
      new_item = self.op(item, div) % lcm
         
      monkey = self.test(new_item)  
      mon_item.append((monkey, new_item))
      self.throw_count += 1
    self.item_list = []
    return mon_item

  def debug_monkey(self):
    print(self.item_list)


def parse_monkeys(monkeys: list) -> list:
  nums = r'\d+'
  lamb = r'[\*+-/]{1}.*[\d+|old]'
  monkey_list = [] 
  divlist = []
  for monkey_el in monkeys:
    line = monkey_el.split('\n')

    list_items = re.findall(nums, line[1])
    list_items = [int(i) for i in list_items]

    ops = re.search(lamb, line[2]).group().split(' ')
    op_string = f'(x {ops[0]} {ops[1] if ops[1] != "old" else "x"})//y'

    
    divideBy = re.findall(nums, line[3])[0]
    mon_true = re.findall(nums, line[4])[0]
    mon_false = re.findall(nums, line[5])[0]
    test_string = f'{mon_true} if (x % {divideBy}) == 0 else {mon_false}'
    
    monkey = Monkey(list_items, op_string, test_string, int(divideBy))
    monkey_list.append(monkey)
    divlist.append(int(divideBy))
  return monkey_list, divlist

def Solve(episodes: int, monkey_list: list, lcm: int, div: int):
  for i in range(episodes):
    for monkey in monkey_list:
      item_list = monkey.throw_list(lcm, div)
      if item_list is None:
        continue
      for mon, item in item_list:
        monkey_list[mon].item_list.append(item)
  count = sorted([i.throw_count for i in monkey_list], reverse=True)
  return count[0] * count[1]



file = open('input.txt').read()
monkeys = file.split('\n\n')

monkey_list, divlist = parse_monkeys(monkeys)
monkey_list2 = copy.deepcopy(monkey_list)
lcm = np.lcm.reduce(divlist)

print(f'Solution1: {Solve(20, monkey_list, lcm, 3)}')
print(f'Solution2: {Solve(10000, monkey_list2, lcm, 1)}')
