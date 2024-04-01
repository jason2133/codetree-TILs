##########################################################################################
### Instruction
# 몬스터가 100만까지 늘어날 수 있음 -> 계산 효율성을 고려해야만 함!

# 효과적으로 코드를 짜기 위해서는
# (몬스터의 위치, 바라보고 있는 방향) 상태에 놓인 몬스터가 몇 마리가 있는지를 관리하는 식으로 구현해야 함.

# 몬스터의 수는 많지만, 격자 크기는 4 x 4로 작기 때문에
# 격자 단위로 시뮬레이션을 진행하는 것이 좋음.
##########################################################################################

### Algorithm
# 몬스터 하나 하나를 전부 관리하게 되면 
# -> 총 몬스터 수를 M 이라고 했을 때, M개의 몬스터들을 매 초마다 한 칸씩 이동시켜줘야 하므로
# 시간 초과가 발생할 가능성이 큼.

# 이때 착안해볼 수 있는 것 :
# 몬스터의 수가 많다고 해도
# -> 결국 (위치, 바라보고 있는 방향)이 일치하는 몬스터들의 움직임은 정확히 동일하다는 것임.
# => 따라서, 동일한 위치에서 동일한 방향을 바라보고 있는 몬스터의 수 자체를 관리하는 식으로 시뮬레이션을 진행하면 됨.

# 이렇게 관리하게 되면
# n x n개의 위치에 대해 각 방향에 맞춰 이동시켜주는 것을 T초 동안 반복하면 되므로
# 시간 복잡도를 줄여줄 수 있음.

# 시체에 대한 처리를 깔끔하게 하기 위해서
# -> 매 초마다 몬스터가 몇 마리씩 있었는지를 전부 저장하여 관리해주는 것이 좋음.

# monster[t][x][y][move_dir] 이라는 배열을 만들어서,
# t초 이후에 위치 (x, y)에서 move_dir 방향을 바라보고 있는 몬스터의 수로 정의해주면 됨.

# 시체가 2번의 턴을 거쳐야 삭제되는 부분
# -> dead[x][y][t] 라는 배열을 만들어서,
# -> (x, y) 위치에서 썩는데 t번의 턴이 남은 몬스터의 수로 정의하여 관리해주면 됨.

##########################################################################################

# 진행되는 턴의 수 t
MAX_T = 25

# N x N 크기
MAX_N = 4

# 방향 숫자 : 방향 d는 1부터 순서대로 ↑, ↖, ←, ↙, ↓, ↘, →, ↗ 를 의미
DIR_NUM = 8

# Pacman 방향 : 상하좌우
P_DIR_NUM = 4

# 시체 썪는거
MAX_DECAY = 2

# 변수 선언 및 입력
n = 4

# 몬스터의 마리 수 m, 진행되는 턴의 수 t
m, t = tuple(map(int, input().split()))

# 팩맨의 위치 저장
px, py = tuple(map(int, input().split()))
px -= 1
py -= 1

# map의 상태
# t번째 턴에 (x, y) 위치에 방향 move_dir를 바라보고 있는 몬스터의 수
## 이걸 이런식으로 접근을 하는구나 -> 개수 관점으로. 
# 계산 효율성을 위해서.

monster = [
    [
        [
            # 방향 move_dir를 바라보고 있는 몬스터의 수
            [0] * DIR_NUM

            # (x, y)  위치
            for i in range(n)
        ]

        for i in range(n)
    ]
    # t번째 턴
    for i in range(MAX_T + 1)
]

# 시체를 관리하기 위한 배열
# (x, y) 위치에서 썪기 t초 전인 시체가
# 몇 개 있는지를 의미함.
dead = [
    [
        # 썪기 t초 전인 시체
        [0] * (MAX_DECAY + 1)

        # (x, y) 위치
        for i in range(n)
    ]
    for i in range(n)
]

# 문제에서 주어지는 방향 순서대로
# dx, dy 값들을 정의함.
# 몬스터를 위한 방향임.
# 방향 d는 1부터 순서대로 ↑, ↖, ←, ↙, ↓, ↘, →, ↗ 를 의미
dxs = [-1, -1, 0, 1, 1, 1, 0, -1]
dys = [0, -1, -1, -1, 0, 1, 1, 1]

# 팩맨을 위한 dx, dy를 따로 정의함.
# 우선순위에 맞춰 상좌하우 순으로 적어줌.
p_dxs = [-1, 0, 1, 0]
p_dys = [0, -1, 0, 1]

# 현재 몇번째 턴인지를 저장함.
t_num = 1

# 영역 내에 있는지를 확인함.
def in_range(x, y):
    return 0 <= x and x < n and 0 <= y and y < n

# 나아가려고 하는 위치가
# 1. 영역 내이 있으며
# 2. 몬스터 시체가 없고
# 3. 팩맨도 없다면
# 이동이 가능함.
def can_go(x, y):
    return in_range(x, y) and dead[x][y][0] == 0 and dead[x][y][1] == 0 and (x, y) != (px, py)

# 다음 위치
def get_next_pos(x, y, move_dir):
    # 현재 위치에서부터
    # 반시계 방향으로 45도씩 회전해보며
    # 가능한 곳이 보이면 바로 이동함.
    for c_dir in range(DIR_NUM):
        n_dir = (move_dir + c_dir + DIR_NUM) % DIR_NUM
        nx = x + dxs[n_dir]
        ny = y + dys[n_dir]

        # 영역 내에 있다면
        if can_go(nx, ny):
            return (nx, ny, n_dir)
    
    # 이동이 불가능하다면,
    # 움직이지 않고 기존 상태 그대로 반환함.
    return (x, y, move_dir)

def move_m():
    # 각 (i, j) 칸에 k 방향을 바라보고 있는 몬스터들이
    # 그 다음으로 이동해야 할 위치 및 방향을 구해서
    # 전부 (칸, 방향) 단위로 이동시켜 줌.
    # 일일이 몬스터마다 위치를 구해 이동시키면 시간초과가 발생함.
    for i in range(n):
        for j in range(n):
            for k in range(DIR_NUM):
                x, y, next_dir = get_next_pos(i, j, k)
                monster[t_num][x][y][next_dir] += monster[t_num - 1][i][j][k]
        
def get_killed_num(dir1, dir2, dir3):
    x, y = px, py
    killed_num = 0

    # 방문한 적이 있는지를 기록함.
    v_pos = []

    for move_dir in [dir1, dir2, dir3]:
        nx = x + p_dxs[move_dir]
        ny = y + p_dys[move_dir]

        # 움직이는 도중에 격자를 벗어나는 경우라면, 선택되면 안됨.
        if not in_range(nx, ny):
            return -1
    
        # 이미 계산한 곳에 대해서는, 중복 계산하지 않음.
        if (nx, ny) not in v_pos:
            killed_num += sum(monster[t_num][nx][ny])
            v_pos.append((nx, ny))
    
    return killed_num

def do_kill(best_route):
    global px, py

    dir1, dir2, dir3 = best_route

    # 정해진 dir1, dir2, dir3 순서에 맞춰 이동하며
    # 몬스터를 잡음.
    for move_dir in [dir1, dir2, dir3]:
        nx = px + p_dxs[move_dir]
        ny = py + p_dys[move_dir]

        for i in range(DIR_NUM):
            dead[nx][ny][MAX_DECAY] += monster[t_num][nx][ny][i]
            monster[t_num][nx][ny][i] = 0

        px, py = nx, ny

def move_p():
    max_cnt = -1
    best_route = (-1, -1, -1)

    # 우선순위 순서대로 수행함.
    for i in range(P_DIR_NUM):
        for j in range(P_DIR_NUM):
            for k in range(P_DIR_NUM):
                m_cnt = get_killed_num(i, j, k)

                # 가장 많은 수의 몬스터를 잡을 수 있는 경우 중
                # 우선순위가 가장 높은 것을 고름.
                if m_cnt > max_cnt:
                    max_cnt = m_cnt
                    best_route = (i, j, k)
    
    # 최선의 루트에 따라
    # 실제 죽이는 것을 진행함.
    do_kill(best_route)

# 시체 썩는거
def decay_m():
    # decay를 진행함. 턴을 하나씩 깎아주면 됨.
    for i in range(n):
        for j in range(n):
            for k in range(MAX_DECAY):
                dead[i][j][k] = dead[i][j][k + 1]
            dead[i][j][MAX_DECAY] = 0

# 몬스터가 복제됨.
def add_m():
    for i in range(n):
        for j in range(n):
            for k in range(DIR_NUM):
                monster[t_num][i][j][k] += monster[t_num - 1][i][j][k]
    
def simulate():
    # 매 초마다 기록하기 때문에 굳이 copy를 진행할 필요는 없음.

    # 각 칸에 있는 몬스터를 이동시킴.
    move_m()

    # 팩맨을 이동시킴.
    move_p()

    # 시체들이 썩어감.
    decay_m()

    # 몬스터가 복제됨.
    add_m()

def count_monster():
    cnt = 0

    # 마지막 턴을 마친 이후의 몬스터 수를 셈.
    for i in range(n):
        for j in range(n):
            for k in range(DIR_NUM):
                cnt += monster[t][i][j][k]

    return cnt

for i in range(m):
    mx, my, mdir = tuple(map(int, input().split()))

    # 1번째 턴의 상태를 기록함.
    monster[0][mx - 1][my - 1][mdir - 1] += 1

# t번 시뮬레이션을 진행함.
while t_num <= t:
    simulate()
    t_num += 1

print(count_monster())