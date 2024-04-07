### Intuition
# 시뮬레이션을 진행함.
# n 제한이 작기 때문 -> 사무실, 에어컨 위치 등을 별도로 관리 X
# 매 시뮬레이션마다 모든 격자 칸들을 순회하며 진행해도 무방함.

# 시원함이 섞이는 처리를 깔끔하게 하기 위해 -> temp 배열을 사용함.
# 인접한 칸에 벽이 있는지에 대한 처리를 잘 하기 위해, dx, dy 테크닉을 상좌우하 순서대로 이용하면 좋음.

### Algorithm
# 먼저 주어진 벽에 대한 처리를 깔끔하게 해야 함.
# 벽은 결국 특정 위치 (x, y)에서 move_dir 방향으로 나아간다고 했을 때 불가능함을 나타내는데 쓰일 것이기에
# -> block[x][y][move_dir] 이렇게 저장하면 편함.

# 인접한 칸으로 이동시 -> dx, dy 테크닉을 활용하면 편함.
# 반대 방향으로 쉽게 전환하기 위해서는 -> 상하 / 좌우끼리 3-move-dir 관계에 놓이게 설정하면 좋음.

# 문제에서 벽의 위가 0, 벽의 왼쪽이 1으로 주어졌기 때문에
# dx, dy 순서를 상좌우하로 놓으면 좋음.

## => 이후, 모든 사무실의 시원함 정도가 k 이상이 되기 전까지 다음 과정을 반복하면 됨.

##############################################
### Step 1. 에이컨에서 시원함을 발산함.
##############################################
# 이 문제에서 가장 복잡하며, 처리하기 까다로운 과정임.
# 한 에어컨에 대한 처리가 되면 -> 각 에어컨은 독립적으로 동작하기 때문에 -> 동일한 방식으로 처리하면 됨.

# 하나의 에어컨에 대해 시원함이 퍼지는 과정
# 재귀함수 (혹은 BFS를 이용한 전파)를 이용하면 깔끔하게 구현이 가능함.

# 벽에 대한 처리가 따로 필요하지 않다면, for문을 이용해서도 쉽게 구현이 가능하겠지만,
# 벽의 유무에 따라 그 뒤에 놓인 칸에 시원함이 퍼지지 않을 수도 있어 단순히 for문을 이용하면 case가 많아지고 코드 길이가 길어지게 됨.
# BFS를 이용하여도 비슷한 방식으로 구현이 가능함.

##### 재귀함수 spread(x, y, move_dir, power)의 역할
### => (x, y) 위치에서 move_dir 방향으로 power만큼의 시원함을 만들었고, 이는 그 다음 칸에도 계속 영향을 미칠거야!!!

# 에어컨의 역할 -> 바로 앞 칸에 power 5를 가지고 spread를 시작했다고 볼 수 있음.
# => spread 함수는 현재 위치 (x, y)를 기준으로 다음 3개의 칸에 대해 영향을 끼칠 수 있음.
# => 케이스 별로 벽의 유무에 따라 영향을 미치지 못할 수도 있음.

##### 재귀함수를 이용하면,
# 같은 칸에 도달했을 때 중복하여 시원함을 누적하게 될 수도 있음
# -> 이를 방지하고자 visited 체크를 꼭 해야 함!!!!!

# 당연하게도 에어컨이 바뀔때마다 visited 값을 초기화하여
# 값이 잘 누적될 수 있도록 해줘야 하지만,
# 이 문제에서는 n이 무척 작기 때문에 별도의 테크닉 없이
# 매 에어컨마다 n^2의 칸을 전부 순회하여 모든 칸에 대해 초기화를 진행해도 무방함.

##############################################
### Step 2. 시원함이 Mix 됨.
##############################################
# 동시에 상호작용이 일어나는 문제
# -> temp라는 별도의 배열을 사용하는 것이 좋음.

# 각 칸에 대해 교환이 일어난 이후의 결과 -> temp에 저장
# => 다시 기존 배열에 값을 옮겨주면 깔끔하게 구현이 가능함.

##############################################
### Step 3. 외벽과 인접한 칸의 시원함이 떨어짐.
##############################################
# 각 칸들 중 양쪽 끝에 해당하는 경우
# -> 1씩 감소

##############################################

DIR_NUM = 4
OFFICE = 1

# 변수 선언 및 입력
n, m, k = tuple(map(int, input().split()))

grid = []
for i in range(n):
    input_data = list(map(int, input().split()))
    grid.append(input_data)
    
# 각 위치의 시원함 정도를 관리함.
# 처음에는 전부 0임.
coolness = [[0] * n for i in range(n)]

# 시원함을 mix할 때 동시에 일어나는 처리를 편하게 하기 위해 사용될 배열임.
temp = [[0] * n for i in range(n)]

# dx, dy 순서를 상좌우하로 설정함.
# 입력으로 주어지는 숫자에 맞추며
# 4에서 현재 방향을 뺐을 때, 반대 방향이 나오도록 설정한 것임.
dxs = [-1, 0, 0, 1]
dys = [0, -1, 1, 0]

# 현재 위치 (x, y)에서 해당 방향으로 이동한다 했을 때
# 벽이 있는지를 나타냄.
block = [[[False] * DIR_NUM for i in range(n)] for j in range(n)]

# 시원함을 전파할 시
# 한 에어컨에 대해
# 겹쳐서 퍼지는 경우를 막기 위해
# visited 배열을 사용함.
visited = [[False] * n for i in range(n)]

# 현재까지 흐른 시간을 나타냄.
elapsed_time = 0

# (x, y)가 격자 내에 있는지를 판단함.
def in_range(x, y):
    return 0 <= x and x < n and 0 <= y and y < n

# (dx, dy)로부터 move_dir 값을 추출해냄.
def rev_dir(x_diff, y_diff):
    for i, (dx, dy) in enumerate(zip(dxs, dys)):
        if dx == x_diff and dy == y_diff:
            return i
    return -1

# (x, y) 위치에서 move_dir 방향으로
# power만큼의 시원함을 만들어줌.
# 이는 그 다음 칸에도 영향을 끼침.
def spread(x, y, move_dir, power):
    # power가 0이 되면 전파를 멈춤.
    if power == 0:
        return

    # 방문 체크를 하고, 해당 위치에 power를 더해줌.
    visited[x][y] = True
    coolness[x][y] += power
    
    # Case 1. 직진하여 전파되는 경우임.
    nx = x + dxs[move_dir]
    ny = y + dys[move_dir]
    
    # 범위 안에 있고
    if in_range(nx, ny):
        # 방문하지 않았으며
        if not visited[nx][ny]:
            # 벽 없으면
            if not block[x][y][move_dir]:
                spread(nx, ny, move_dir, power - 1)
    
    # Case 2. 대각선 방향으로 전파되는 경우임.
    # 좌우
    if dxs[move_dir] == 0:
        for nx in [x + 1, x - 1]:
            ny = y + dys[move_dir]
            # 꺾여 들어가는 곳에 전부 벽이 없는 경우에만 전파가 가능함.
            # 범위 안에 있고
            if in_range(nx, ny):
                # 방문하지 않았으며
                if not visited[nx][ny]:
                    # 벽이 없다면
                    if not block[x][y][rev_dir(nx - x, 0)]:
                        if not block[nx][y][move_dir]:
                            spread(nx, ny, move_dir, power - 1)
            
    # # 상하
    else:
        for ny in [y + 1, y - 1]:
            nx = x + dxs[move_dir]
            # 꺾여 들어가는 곳에 전부 벽이 없는 경우에만 전파가 가능함.
            # 범위 안에 있고
            if in_range(nx, ny):
                # 방문하지 않았으며
                if not visited[nx][ny]:
                    # 벽이 없다면
                    if not block[x][y][rev_dir(0, ny - y)]:
                        if not block[x][ny][move_dir]:
                            spread(nx, ny, move_dir, power - 1)
                
# visited를 clear하는 코드
def clear_visited():
    for i in range(n):
        for j in range(n):
            visited[i][j] = False
            
# 에어컨에서 시원함을 발산함.
def blow():
    # 각 에어컨에 대해
    # 시원함을 발산함.
    for x in range(n):
        for y in range(n):
            # 에어컨에 대해
            # 해당 방향으로 시원함을 만들어줌.
            if grid[x][y] >= 2:
                if grid[x][y] <= 3:
                    move_dir = 3 - grid[x][y]
                else:
                    move_dir = grid[x][y] - 2
                
                nx = x + dxs[move_dir]
                ny = y + dys[move_dir]
                
                # 전파 전에 visited 값을 초기화해줌.
                clear_visited()
                
                # 세기 5에서 시작하여 계속 전파함.
                spread(nx, ny, move_dir, 5)
                
# (x, y) 위치는
# mix된 이후 시원함이
# 얼마가 되는지를 계산해줌.
def get_mixed_coolness(x, y):
    remaining_c = coolness[x][y]
    
    for i, (dx, dy) in enumerate(zip(dxs, dys)):
        nx = x + dx
        ny = y + dy
        
        # 사이에 벽이 존재하지 않는 경우에만
        # mix가 일어남.
        # 범위 안에 있고
        if in_range(nx, ny):
            # 벽이 없다면
            if not block[x][y][i]:
                # 현재의 시원함이 더 크다면, 그 차이를 4로 나눈 값만큼 빠져나옴.
                if coolness[x][y] > coolness[nx][ny]:
                    remaining_c -= (coolness[x][y] - coolness[nx][ny]) // 4
                    
                # 그렇지 않다면, 반대로 그 차이를 4로 나눈 값만큼 받아오게 됨.
                else:
                    remaining_c += (coolness[nx][ny] - coolness[x][y]) // 4
    return remaining_c

# 시원함이 mix 됨.
def mix():
    # temp 배열을 초기화해줌.
    for i in range(n):
        for j in range(n):
            temp[i][j] = 0
    
    # 각 칸마다 시원함이 mix된 이후의 결과를 받아옴.
    for i in range(n):
        for j in range(n):
            temp[i][j] = get_mixed_coolness(i, j)
    
    # temp 값을 coolness 배열에 다시 옮겨줌.
    for i in range(n):
        for j in range(n):
            coolness[i][j] = temp[i][j]

# 외벽에 해당하는 칸인지를 판단함
def is_outer_wall(x, y):
    return x == 0 or x == n-1 or y == 0 or y == n-1

# 외벽과 인접한 칸 중
# 시원함이 있는 칸에 대해서만
# 1만큼 시원함을 하락시킴
def drop():
    for i in range(n):
        for j in range(n):
            if is_outer_wall(i, j) and coolness[i][j] > 0:
                coolness[i][j] -= 1

# 시원함이 생기는 과정을 반복함.
def simulate():
    global elapsed_time
    
    # Step 1. 에어컨에서 시원함을 발산함.
    blow()
    
    # Step 2. 시원함이 mix 됨.
    mix()
    
    # Step 3. 외벽과 인접한 칸의 시원함이 떨어짐.
    drop()
    
    # 시간이 1분씩 증가함.
    elapsed_time += 1

# 종료해야 할 순간인지를 판단함.
# 모든 사무실의 시원함의 정도가 k 이상이거나
# 흐른 시간이 180분을 넘게 되는지를 살펴봄.
def end():
    # 100분이 넘게 되면 종료함.
    if elapsed_time > 100:
        return True
    
    # 사무실 중에
    # 시원함의 정도가 k 미만인 곳이
    # 단 하나라도 있으면, 아직 끝내면 안됨.
    for i in range(n):
        for j in range(n):
            if grid[i][j] == OFFICE:
                if coolness[i][j] < k:
                    return False
    # 모두 k 이상이면 종료
    return True

for i in range(m):
    bx, by, bdir = tuple(map(int, input().split()))
    bx -= 1
    by -= 1
    
    # 현재 위치 (bx, by)에서 bdir 방향으로 나아가려고 했을 때
    # 벽이 있음을 표시해줌.
    block[bx][by][bdir] = True
    
    nx = bx + dxs[bdir]
    ny = by + dys[bdir]
    
    # 격자를 벗어나지 않는 칸과 벽을 사이에 두고 있다면
    # 해당 칸에서 반대 방향 (3-bdir)으로 진입하려고 할 때도
    # 벽이 있음을 표시해줌.
    if in_range(nx, ny):
        block[nx][ny][3 - bdir] = True
        
# 종료조건이 만족되기 전까지
# 계속 시뮬레이션을 반복합니다.
while not end():
    simulate()

# 출력:
if elapsed_time <= 100:
    print(elapsed_time)
else:
    print(-1)