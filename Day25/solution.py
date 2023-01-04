
demo = """1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122
"""

inp = demo
inp = open('input.txt').read()
inp = inp.splitlines()

stod = {
  '=': -2,
  '-': -1,
  '0': 0,
  '1': 1,
  '2': 2
}

dtos = {v: k for k, v in stod.items()}

total = 0
for line in inp:
  d = 0
  for i, c in enumerate(reversed(line)):
    d += stod[c] * 5**i
  total += d

t = total
snaf = ""
while t > 0:
  d = ((t+2) % 5) -2
  snaf += dtos[d]
  t -= d
  t //= 5

print(snaf[::-1])
