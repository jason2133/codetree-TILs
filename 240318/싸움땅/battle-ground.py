##### Instruction
# 플레이어들 : 특정 규칙에 따라 움직일 때, 각 라운드마다 결과를 계산하는 시뮬레이션 문제
# 이동, 총 획득, 플레이어 간의 전투 등 상태 변화를 적절히 추적하여 정확한 결과를 도출하는 것이 핵심임.
# 플레이어 이동 후 총 획득, 다른 플레이어와의 전투 및 전투의 승자 결정, 총 내려두기와 획득 등을 규칙에 따라 구현해야 함.
# -> 임시 저장 등을 이용해서 각 단계를 체게적으로 구현해 나가는 것이 중요함.

##### Algorithm
# 시뮬레이션 -> 여러 단계로 나누어짐.
# 각 플레이어 : 자신의 위치에서 지정된 방향으로 이동 -> 해당 위치에 다른 플레이어가 있으면 싸움을 벌임.
# 무기가 있는 경우 취득하고, 총이 여러 개 있는 경우 공격력이 가장 높은 총을 선택함.

### 시뮬레이션은 플레이어가 1명씩 순서대로 움직이면서 아래와 같은 단계를 수행함.
# 1. 다음 칸으로 이동할 때 한 칸을 움직이되, 격자 밖으로 나가는 경우 반대 방향으로 한 칸 움직임
# 2. 이동한 위치에 총이 있으면 총을 주움. 현재 보유한 총과 비교해 공격력이 더 높으면 바꿈.
# 3. 이동한 위치에 이미 다른 플레이어가 있는 경우, 해당 위치에서 싸움을 진행함.
# -> 싸움의 결과는 플레이어의 초기 능력치와 보유한 총의 공격력을 합한 수치로 결정됨.
# 4. 싸움에서 진 플레이어는 보유하던 총을 떨구고 지정된 규칙에 따라 다음 칸으로 움직임.
# 5. 싸움에서 이긴 플레이어는 상대방과 자신이 보유한 총 중 가장 강력한 총을 선택하여 보유하고, 나머지 총은 원래 위치에 두게 됨.

### 플레이어 정보
# tuple을 이용해 표현
# 위치, 방향, 능력치, 보유 총의 공격력 등이 저장됨.

### 맵
# 각 격자에 놓여 있는 총의 목록이 벡터 형태로 관리됨.
# 격자 밖으로 나갈 수 없도록 경계 체크가 실행됨.

### 모든 라운드의 시뮬레이션이 수행된 후, 각 라운드에서 각 플레이어가 얻은 포인트를 출력함.

EMPTY = (-1, -1, -1, -1, -1, -1)

# 변수 선언 및 입력
# n : 격자의 크기
# m : 플레이어의 수
# k : 라운드의 수
n, m, k = tuple(map(int, input().split()))

# 각 칸마다 놓여있는 총 목록을 관리함

##############################################
# gun_info에 대한 나의 접근 방법은 맞았네!
##############################################
gun = [
    [[] for i in range(n)]
    for j in range(n)
]

# n개의 줄에 걸쳐 격자에 있는 총의 정보가 주어짐.
# 각 줄에는 각각의 행에 해당하는 n개의 수가 공백을 사이에 두고 주어짐.
for i in range(n):
    nums = list(map(int, input().split()))
    for j in range(n):
        # 총이 놓여 있는 칸
        if nums[j] != 0:
            gun[i][j].append(nums[j])

##############################################
# player_info에 대한 나의 접근 방법도 맞았네! 아...
##############################################

# 각 칸마다 플레이어 정보를 관리함.
# 순서대로 (num, x, y, d, s, a) 정보를 관리함.
# (x, y) 위치에서 방향 d를 보고 있으며
# 초기 능력치가 s인 num번 플레이어가
# 공격력이 a인 총을 들고 있음을 뜻함.
# 총이 없으면 a는 0임.
            
players = []

# m개의 줄에 걸쳐 플레이어들의 정보 x, y, d, s가 공백을 사이에 두고 주어짐.
#  (x, y)는 플레이어의 위치, d는 방향, s는 플레이어의 초기 능력치를 의미
# 방향 d는 0부터 3까지 순서대로 ↑, →, ↓, ←을 의미
for i in range(m):
    x, y, d, s = tuple(map(int, input().split()))
    players.append((i, x - 1, y - 1, d, s, 0))

# 입력으로 주어지는 방향 순서대로 dx, dy를 정의함.
# 방향 d는 0부터 3까지 순서대로 ↑, →, ↓, ←을 의미
# 상 우 하 좌
dxs = [-1, 0, 1, 0]
dys = [0, 1, 0, -1]

# 플레이어들의 포인트 정보를 기록함.
points = [0] * m

# (x, y)가 격자를 벗어나는지 확인함.
##############################################
# 이렇게 따로 별도의 함수를 만드는 것도 하나의 팁이겠구나.
##############################################

def in_range(x, y):
    return 0 <= x and x < n and 0 <= y and y < n

# 현재 (x, y) 위치에서 방향 d를 보고 있을 때, 그 다음 위치와 방향을 찾아줌
##############################################
# 여기서 실수가 있었다. 반대 방향으로 돌아간다는 것은 +1, -1이 아니라 +2, -2 이런 식으로 했어야 했다.
##############################################
def get_next(x, y, d):
    nx = x + dxs[d]
    ny = y + dys[d]

    # 격자를 벗어나면 방향을 뒤집어 반대 방향으로 한 칸 이동함.
    if not in_range(nx, ny):
        # 반대 방향 : 0 < 2 / 1 < 3
        if d < 2:
            d = (d + 2)
        else:
            d = (d - 2)
        nx = x + dxs[d]
        ny = y + dys[d]
    return (nx, ny, d)

# 해당 칸에 있는 Player를 잧아줌.
# 없다면 EMPTY를 반환함.
def find_player(pos):
    for i in range(m):
        _, x, y, _, _, _ = players[i]
        if pos == (x, y):
            return players[i]
    return EMPTY

# Player p의 정보를 갱신해줌.
def update(p):
    num, _, _, _, _, _ = p

    # Player의 위치를 찾아 값을 갱신해줌.
    for i in range(m):
        num_i, _, _, _, _, _ = players[i]

        if num_i == num:
            players[i] = p
            break

# 플레이어 p를 pos 위치로 이동시켜 줌.
def move(p, pos):
    num, x, y, d, s, a = p
    nx, ny = pos

    # 가장 좋은 총으로 갱신해줌.
    gun[nx][ny].append(a)
    gun[nx][ny] = sorted(gun[nx][ny])[::-1]
    a = gun[nx][ny][0]
    gun[nx][ny].pop(0)

    p = (num, nx, ny, d, s, a)
    update(p)

# 진 사람의 움직임을 진행함.
# 결투에서 패배한 위치는 pos임.
def loser_move(p):
    num, x, y, d, s, a = p

    # 먼저 현재 위치에 총을 내려놓게 됨.
    gun[x][y].append(a)

    # 빈 공간을 찾아 이동하게 됨
    # 현재 방향에서 시작하여
    # 90도씩 시계방향으로 회전하다가
    # 비어있는 최초의 곳으로 이동함.
    for i in range(4):
        ndir = (d + i) % 4
        nx = x + dxs[ndir]
        ny = y + dys[ndir]

        if in_range(nx, ny) and find_player((nx, ny)) == EMPTY:
            p = (num, x, y, ndir, s, 0)
            move(p, (nx, ny))
            break

# p1과 p2가 pos에서 만나 결투를 진행함.
def duel(p1, p2, pos):
    num1, _, _, d1, s1, a1 = p1
    num2, _, _, d2, s2, a2 = p2

    # (초기 능력치 + 총의 공격력, 초기 능력치) 순으로 우선순위를 매겨 비교함.

    # p1이 이긴 경우
    if (s1 + a1, s1) > (s2 + a2, s2):
        # p1은 포인트를 얻게 됨.
        points[num1] += (s1 + a1) - (s2 + a2)

        # p2는 진 사람의 움직임을 진행함.
        loser_move(p2)

        # 이후 p1은 이긴 사람의 움직임을 진행함.
        move(p1, pos)
    
    # p2가 이긴 경우
    else:
        # p2는 포인트를 얻게 됨.
        points[num2] += (s2 + a2) - (s1 + a1)

        # p1은 진 사람의 움직임을 진행함.
        loser_move(p1)

        # 이후 p2는 이긴 사람의 움직임을 진행함.
        move(p2, pos)

# 1라운드를 진행함.
def simulate():
    # 첫번째 플레이어부터 순서대로 진행함.
    for i in range(m):
        num, x, y, d, s, a = players[i]

        # Step 1-1. 현재 플레이어가 움직일 그 다음 위치와 방향을 구함.
        nx, ny, ndir = get_next(x, y, d)

        # 해당 위치에 있는 전 플레이어의 정보를 얻어옴.
        next_player = find_player((nx, ny))

        # 현재 플레이어의 위치와 방향을 보정해줌.
        curr_player = (num, nx, ny, ndir, s, a)
        update(curr_player)

        # Step 2. 해당 위치로 이동해봄.
        # Step 2-1. 해당 위치에 플레이어가 없다면, 그대로 움직임.
        if next_player == EMPTY:
            move(curr_player, (nx, ny))
        
        # Step 2-2. 해당 위치에 플레이어가 있다면, 결투를 진행함.
        else:
            duel(curr_player, next_player, (nx, ny))
    
# k번에 걸쳐 시뮬레이션을 진행함.
for i in range(k):
    simulate()

# 각 플레이어가 획득한 포인트를 출력함
for point in points:
    print(point, end = ' ')