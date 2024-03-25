### 시뮬레이션

##########################################################################
### Intuition
# 술래잡기 게임 : 최종 점수 -> 술래가 도망자를 잡는 횟수에 비례함.
# 술래와 도망자들이 일정한 규칙에 따라 움직인다는 사실에 주의해야 함.
# 술래와 도망자의 움직임 패턴을 이해하고, 이를 효과적으로 시뮬레이션하여 술래가 각 턴마다 얻을 수 있는 점수를 계산하도록 함.

# 도망자의 이동 -> 술래와의 거리 판단, 격자 범위 내 이동 등의 조건을 충족해야 함.
# 술래의 이동 -> 정해진 패스에 따른 것이므로 술래의 진행 경로를 미리 계산해두고 시뮬레이션 중 이를 따라 이동함.
####### 이 접근 방법은 맞았는데 ㅠ 왜 그럴까...

# 나무로 가려진 도망자 -> 술래에게 보이지 않으므로 이런 예외 사항도 고려해야 함.
# 이러한 시뮬레이션을 k번 반복하여, 게임이 종료될 때까지의 술래의 총 점수를 계산함.
##########################################################################

##########################################################################
### Algorithm
# 먼저, 술래의 이동 경로를 계산함.
# 격자의 중심에서 시작하여 달팽이 모양의 경로에 따라 격자의 끝까지 도달하면 다시 중앙으로 이동하는 경로를 구성함.
# -> 술래의 정방향과 역방향 이동 경로를 각각 계산함.

# 다음으로, 모든 턴에서 다음과 같은 과정을 수행함.
# 도망자가 술래와의 거리를 고려하여 움직임.
# 술래가 움직임.
# 술래가 시야 내에 있는 도망자를 잡고 점수를 획득함.

# 술래와 도망자의 움직임 -> 각자 규칙이 존재하므로 코드에서 각 조건을 체크하면서 적절히 처리함.

# 도망자는 격자를 벗어나지 않고 술래가 있는 칸으로는 이동하지 않으며,
# 격자의 경계에 도달하면 반대 방향으로 이동할 수 있어야 함.

# 술래는 규칙적인 경로를 따라 이동 및 방향 전환 후 시야 내에 있는 도망자를 잡음.

# 이 과정을 k번 반복한 후, 술래의 최종 점수를 출력함.
##########################################################################

# 문제 풀이

# 변수 선언 및 출력
n, m, h, k = tuple(map(int, input().split()))

# 각 칸에 있는 도망자 정보를 관리함.
# 도망자의 방향만 저장하면 충분함.
hiders= [
    [[] for i in range(n)]
    for j in range(n)
]

next_hiders = [
    [[] for i in range(n)]
    for j in range(n)
]

tree = [
    [False] * n
    for i in range(n)
]

# 정방향 기준으로
# 현재 위치에서 술래가 움직여야 할 방향을 관리함.
seeker_next_dir = [
    [0] * n
    for i in range(n)
]

# 역방향 기준으로
# 현재 위치에서 술래가 움직여야 할 방향을 관리함.
seeker_rev_dir = [
    [0] * n
    for i in range(n)
]

# 술래의 현재 위치
seeker_pos = (n // 2, n // 2)

# 술래가 움직이는 방향
# 정방향이면 True
# 아니라면 False
forward_facing = True

ans = 0

# 술래 정보를 입력받음.
for i in range(m):
    x, y, d = tuple(map(int, input().split()))
    hiders[x - 1][y - 1].append(d)

# 나무 정보를 입력받음.
for i in range(h):
    x, y = tuple(map(int, input().split()))
    tree[x - 1][y - 1] = True

# 정중앙으로부터 끝까지 움직이는 경로를 계산해줌.
def initialize_seeker_path():
    # 상우하좌 순서대로 넣어줌
    dxs = [-1, 0, 1, 0]
    dys = [0, 1, 0, -1]

    # 시작 위치와 방향,
    # 해당 방향으로 이동할 횟수를 설정함.
    curr_x, curr_y = n // 2, n // 2
    move_dir = 0
    move_num = 1

    while curr_x or curr_y:
        # move_num만큼 이동
        for i in range(move_num):
            seeker_next_dir[curr_x][curr_y] = move_dir
            curr_x = curr_x + dxs[move_dir]
            curr_y = curr_y + dys[move_dir]

            seeker_rev_dir[curr_x][curr_y] = move_dir + 2 if move_dir < 2 else move_dir - 2

            # 이동하는 도중 (0, 0)으로 오게 되면,
            # 움직이는 것을 종료함.
            if not curr_x and not curr_y:
                break
        
        # 방향을 바꿈.
        move_dir = (move_dir + 1) % 4

        # 만약 현재 방향이 위 혹은 아래가 된 경우에는
        # 특정 방향으로 움직여야 할 횟수를 1 증가시킴.
        if move_dir == 0 or move_dir == 2:
            move_num += 1

# 격자 내에 있는지를 판단함.
def in_range(x, y):
    return 0 <= x and x < n and 0 <= y and y < n

def hider_move(x, y, move_dir):
    # 좌우하상 순서대로 넣어줌.
    dxs = [0, 0, 1, -1]
    dys = [-1, 1, 0, 0]

    nx = x + dxs[move_dir]
    ny = y + dys[move_dir]

    # Step 1. 만약 격자를 벗어난다면 우선 방향을 틀어줌.
    if not in_range(nx, ny):
        # 0 <. 1, 2 <. 3이 되어야 함.
        move_dir = 1 - move_dir if move_dir < 2 else 5 - move_dir
        nx = x + dxs[move_dir]
        ny = y + dys[move_dir]

    
    # Step 2. 그 다음 우치에 술래가 없다면 움직여줌.
    if (nx, ny) != seeker_pos:
        next_hiders[nx][ny].append(move_dir)
    
    # 술래가 있다면 더 움직이지 않음.
    else:
        next_hiders[x][y].append(move_dir)

def dist_from_seeker(x, y):
    # 현재 술래의 위치를 불러옴.
    seeker_x, seeker_y = seeker_pos
    return abs(seeker_x - x) + abs(seeker_y - y)

def hider_move_all():
    # Step 1. next hider를 초기화해줌.
    for i in range(n):
        for j in range(n):
            next_hiders[i][j] = []
    
    # Step 2. hider를 전부 움직여줌.
    for i in range(n):
        for j in range(n):
            # 술래와의 거리가 3 이내인 도망자들에 대해서만 움직여줌
            if dist_from_seeker(i, j) <= 3:
                for move_dir in hiders[i][j]:
                    hider_move(i, j, move_dir)
            
            # 그렇지 않다면 현재 위치 그대로 넣어줌.
            else:
                for move_dir in hiders[i][j]:
                    next_hiders[i][j].append(move_dir)
        
    # Step 3. next hider 값을 옮겨줌.
    for i in range(n):
        for j in range(n):
            hiders[i][j] = next_hiders[i][j]
            
# 현재 술래가 바라보는 방향을 가져옴.
def get_seeker_dir():
    # 현재 술래의 위치를 불러옴.
    x, y = seeker_pos

    # 어느 방향으로 움직여야 하는지에 대한 정보를 가져옴.
    move_dir = 0

    if forward_facing:
        move_dir = seeker_next_dir[x][y]
    
    else:
        move_dir = seeker_next_dir[x][y]
    
    return move_dir

def check_facing():
    global forward_facing

    # Case 1. 정방향으로 끝에 다다른 경우라면, 방향을 바꿔줌
    if seeker_pos == (0, 0) and forward_facing:
        forward_facing = False
    
    # Case 2. 역방향으로 끝에 다다른 경우라도, 방향을 바꿔줌
    if seeker_pos == (n // 2, n // 2) and not forward_facing:
        forward_facing = True
    
def seeker_move():
    global seeker_pos

    x, y = seeker_pos

    # 상우하좌 순서대로 넣어줌
    dxs = [-1, 0, 1, 0]
    dys = [0, 1, 0, -1]

    move_dir = get_seeker_dir()

    # 술래를 한칸 움직여줌
    seeker_pos = (x + dxs[move_dir], y + dys[move_dir])

    # 끝에 도달했다면 방향을 바꿔줌
    check_facing()

def get_score(t):
    global ans

    # 상우하좌 순서대로 넣어줌
    dxs = [-1, 0, 1, 0]
    dys = [0, 1, 0, -1]

    # 현재 술래의 위치를 불러옴
    x, y = seeker_pos

    # 술래의 방향을 불러옴
    move_dir = get_seeker_dir()

    # 3칸을 바라봄
    for dist in range(3):
        nx = x + dist * dxs[move_dir]
        ny = y + dist * dys[move_dir]

        # 격자를 벗어나지 않으며, 나무가 없는 위치라면
        # 도망자들을 전부 잡게 됨.
        if in_range(nx, ny) and not tree[nx][ny]:
            # 해당 위치의 도망자 수만큼 점수를 얻게 됨.
            ans += t * len(hiders[nx][ny])

            # 도망자들이 사라지게 됨
            hiders[nx][ny] = []

def simulate(t):
    # 도망자가 움직임
    hider_move_all()

    # 술래가 움직임
    seeker_move()

    # 점수를 얻음
    get_score(t)

# 술래잡기 시작 전에
# 구현 상의 편의를 위해
# 술래 경로 정보를 미리 계산함.
initialize_seeker_path()

# k번에 걸쳐 술래잡기를 진행함.
for t in range(1, k + 1):
    simulate(t)

print(ans)