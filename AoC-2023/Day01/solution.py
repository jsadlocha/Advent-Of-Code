import re

demo = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""

demo2 = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""

# inp = demo2
inp = open("input.txt").read()
inp = inp.split("\n")[:-1]
hashmap = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9", "1":"1", "2":"2", "3":"3", "4":"4", "5":"5", "6":"6", "7":"7", "8":"8", "9":"9"}
solution1 = 0
solution2 = 0
for line in inp:
    out = re.findall(r'\d', line)
    out2 = re.findall(r'(?=(\d|one|two|three|four|five|six|seven|eight|nine))', line)
    solution1 += int(out[0] + out[-1])
    solution2 += int(hashmap[out2[0]] + hashmap[out2[-1]])

print(solution1)
print(solution2)
