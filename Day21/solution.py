
demo = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
"""
list_exp = {}
class Expression:
  def __init__(self, x, y, op):
    self.x = x
    self.y = y
    self.op = op
  
  def exec(self):
    x = list_exp[self.x].exec()
    y = list_exp[self.y].exec()
    if self.op == '==':
      return x-y
    return eval(f'{x} {self.op} {y}')

class Number:
  def __init__(self, x):
    self.x = x
  
  def exec(self):
    return self.x

inp = demo
inp = open('input.txt').read()
inp = inp.splitlines()
import re

p_digit = r'\d+'
p_exp = r'(\w+) (.{1}) (\w+)'
for line in inp:
  name, rest = line.split(':')
  val = re.findall(p_digit, rest)
  exp = re.findall(p_exp, rest)
  if len(val) == 1:
    list_exp[name] = Number(val[0])
  else:
    exp = exp[0]
    list_exp[name] = Expression(exp[0], exp[2], exp[1])
  
solution1 = int(list_exp["root"].exec())


list_exp['root'].op = '=='
s = 0
dt = 1000000000000
for i in range(1000):
  list_exp['humn'].x = s
  m_err = list_exp['root'].exec()

  list_exp['humn'].x = s+dt
  r_err = list_exp['root'].exec()

  list_exp['humn'].x = s-dt
  l_err = list_exp['root'].exec()

  if abs(r_err) < abs(m_err):
    s += dt
    continue
  
  if abs(l_err) < abs(m_err):
    s -= dt
    continue
  
  if abs(m_err) < abs(l_err) or abs(m_err) < abs(r_err):
    dt = dt//2

  if abs(m_err) == 0:
    break

print(f'Solution1: {solution1}')
print(f'Solution2: {s}')
