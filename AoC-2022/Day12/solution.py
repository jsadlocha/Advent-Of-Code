from collections import defaultdict

def print_grid(grid):
  for row in grid:
    for col in row:
      print(f'{col}, ', end='')
    print('')

class Graph:
  def __init__(self):
    self.graph = defaultdict(list)

  def addEdge(self, node, neigh):
    self.graph[node].append(neigh)

  def BFS(self, start_point, end_point):
    visited = [False] * (max(self.graph)+1)

    queue = []

    queue.append([start_point, []])
    visited[start_point] = True

    global grid
    test = []
    finded = []
    while queue:
      node, path = queue.pop(0)
     
      if node == end_point:
        finded = path

      for i in self.graph[node]:
        if visited[i] is False:
          queue.append([i, path+[i]])
          visited[i] = True

    return finded

def create_graph(inp):
  graph = Graph()
  start = 0
  end = 0
  starting_list = []
  grid = []
  for row, line in enumerate(inp):
    grid.append([])
    for col, el in enumerate(line):
      if el == 'E':
        el = '{'
        print(f'col: {col} row: {row}')
      grid[row].append(el)

  for row, line in enumerate(grid):
    for col, el in enumerate(line):
      cur = grid[row][col]
      row_size = len(grid[0])
      if grid[row][col] == '{':
        end = row*row_size+col

      if grid[row][col] == 'S':
        start = row*row_size+col
        grid[row][col] = 'a'
        cur = 'a'
      
      if cur == 'a':
        starting_list.append(row*row_size+col)

      # left
      if ((col-1) > -1) and ((ord(grid[row][col-1])-ord(cur)) < 2):
        graph.addEdge(row*row_size+col, row*row_size+(col-1)) 
      # right
      if ((col+1) < len(grid[0])) and ((ord(grid[row][col+1])-ord(cur)) < 2):
        graph.addEdge(row*row_size+col, row*row_size+(col+1)) 
      # up
      if ((row+1) < len(grid)) and ((ord(grid[row+1][col])-ord(cur)) < 2):
        graph.addEdge(row*row_size+col, (row+1)*row_size+col) 
      # down
      if ((row-1) > -1) and ((ord(grid[row-1][col])-ord(cur)) < 2):
        graph.addEdge(row*row_size+col, (row-1)*row_size+col) 


  return graph, grid, start, end, starting_list

demo = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""
inp = demo
inp = open('input.txt').read()
inp = inp.split('\n')[:-1]


graph, grid, start, end, starting_list = create_graph(inp)

end_list = graph.BFS(start, end)


print(f'Solution1: {len(end_list)}')

l = []
for i in starting_list:
  x = len(graph.BFS(i, end))
  if x > 0:
    l.append(x)

print(f'Solution2: {sorted(l)[0]}')


