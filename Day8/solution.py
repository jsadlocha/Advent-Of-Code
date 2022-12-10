
def check_row(grid, row, col):
  vis_l = True
  vis_r = True
  for i in range(0, col):
    if (int(grid[row][i]) >= int(grid[row][col])):
      vis_l = False

  for j in range(col+1, col_len):
    if (int(grid[row][j]) >= int(grid[row][col])):
      vis_r = False

  return vis_l or vis_r

def check_col(grid, row, col):
  vis_u = True
  vis_b = True
  for i in range(0, row):
    if (int(grid[i][col]) >= int(grid[row][col])):
      vis_u = False

  for j in range(row+1, row_len):
    if (int(grid[j][col]) >= int(grid[row][col])):
      vis_b = False

  return vis_u or vis_b

def row_distance(grid, row, col):
  count_l = 0
  count_r = 0
  for i in range(col-1, -1, -1):
    count_l+=1
    if (int(grid[row][i]) >= int(grid[row][col])):
      break

  for j in range(col+1, col_len):
    count_r += 1
    if (int(grid[row][j]) >= int(grid[row][col])):
      break
  
  return count_l * count_r

def col_distance(grid, row, col):
  count_u = 0
  count_b = 0
  for i in range(row-1, -1, -1):
    count_u += 1
    if (int(grid[i][col]) >= int(grid[row][col])):
      break

  for j in range(row+1, row_len):
    count_b += 1
    if (int(grid[j][col]) >= int(grid[row][col])):
      break

  return count_u * count_b

grid = open('input.txt').read().split('\n')[:-1]

count = 0
col_len = len(grid[0])
row_len = len(grid)
max_value = 0
for row in range(col_len):
  for col in range(row_len):
    tmp = row_distance(grid, row, col)*col_distance(grid,row,col)
    max_value = max(max_value, tmp)
    if (check_row(grid, row, col) or check_col(grid, row, col)):
      count += 1

    
print(f'Solution1: {count}')
print(f'Solution2: {max_value}')