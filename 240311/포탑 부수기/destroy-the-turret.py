N, M, K = tuple(map(int, input().split()))

board = []
for i in range(N):
    board.append(list(map(int, input().split())))

attack_check = [[0 for i in range(M)] for j in range(N)]
turn = 1

attack_each_turn_check = [[False for i in range(M)] for j in range(N)]

# 각 숫자는 공격력을 나타냄.
# 공격력이 0이면 부서진 포탑

# 하나의 턴 : 4가지 액션 순서대로 수행 -> K번 반복
# 1. 공격자 선정
# 2. 공격자의 공격
# 2-1. 레이저 공격
# 2-2. 포탄 공격
# 3. 포탑 부서짐
# 4. 포탑 정비

# 1. 공격자 선정
# 부서지지 않은 포탑 중 가장 약한 포탑 찾기 -> 공격자로 선정되기 때문
# 1, 2, 3, 4 -> 이거 정렬 기준 잘 설정하기
# 이 포탑에 대하여 N + M만큼 공격력 추가하기

def step_1_select_attack(board, attack_check):
    max_attack = 5001
    attack_pos = []
    for i in range(N):
        for j in range(M):
            if 1 <= board[i][j]:
                if board[i][j] < max_attack:
                    max_attack = board[i][j]
                    attack_pos = []
                    attack_pos.append([i, j])
                elif board[i][j] == max_attack:
                    attack_pos.append([i, j])
    # 1순위) 가장 최근에 공격한 포탑              
    # 2순위) 각 포탑 위치의 행과 열의 합이 가장 큰 포탑이 가장 약한 포탑
    # 3순위) 각 포탑 위치의 열 값이 가장 큰 포탑
    attack_pos = sorted(attack_pos, key=lambda x: (attack_check[x[0]][x[1]], -(x[0] + x[1]), x[1]))
    board[attack_pos[0][0]][attack_pos[0][1]] += (N + M)
    return board, attack_pos[0]

# 2. 공격자의 공격
# 자신을 제외한 가장 강한 포탑 찾기
# 1, 2, 3, 4 -> 이거 정렬 기준 잘 설정하기
def step_2_attack_to(board, turn, attack_check):
    min_attack = 1
    attack_pos = []
    for i in range(N):
        for j in range(M):
            if 1 <= board[i][j]:
                if min_attack < board[i][j]:
                    min_attack = board[i][j]
                    attack_pos = []
                    attack_pos.append([i, j])
                elif min_attack == board[i][j]:
                    attack_pos.append([i, j])
    # 1순위) 공격한지 가장 오래된 포탑이 가장 강한 포탑  
    # 2순위) 각 포탑 위치의 행과 열의 합이 가장 작은 포탑
    # 3순위) 각 포탑 위치의 열 값이 가장 작은 포탑
    attack_pos = sorted(attack_pos, key=lambda x: (-attack_check[x[0]][x[1]], (x[0] + x[1]), x[1]))
    attack_target = attack_pos[0]
    attack_check[attack_pos[0][0]][attack_pos[0][1]] = turn
    return attack_target

from collections import deque
def step_2_minimum_route(board, blue, red):
    blue_x, blue_y = blue
    red_x, red_y = red

    visited = [(blue_x, blue_y)]
    queue = deque([(blue_x, blue_y, [(blue_x, blue_y)])])

    dx = [0, 1, 0, -1]
    dy = [1, 0, -1, 0]

    while queue:
        queue_x, queue_y, path = queue.popleft()

        for i in range(4):
            nx = queue_x + dx[i]
            ny = queue_y + dy[i]

            if 0 <= nx < N and 0 <= ny < M:
                if nx == red_x and ny == red_y:
                    return path[1:]
                if (nx, ny) not in visited:
                    visited.append((nx, ny))
                    queue.append((nx, ny, path + [(nx, ny)]))
    return -1
    
# 3. 포탑 부서짐
# 공격력 0 이하가 된 포탑은 부서짐

def step_3_destroy_potap(board, attack_each_turn_check):
    for i in range(N):
        for j in range(M):
            if board[i][j] <= 0:
                board[i][j] = 0
                attack_each_turn_check[i][j] = True
    return board, attack_each_turn_check

board, attack_each_turn_check = step_3_destroy_potap(board, attack_each_turn_check)

# 4. 포탑 정비
# 부서지지 않은 포탑 중 공격과 무관했던 포탑 -> 공격력이 1씩 올라감
# 공격과 무관 : 공격자도 아니고, 공격에 피해를 입은 포탑도 아니라는 뜻임.
def step_4_fix_potap(board, attack_each_turn_check):
    for i in range(N):
        for j in range(M):
            if attack_each_turn_check[i][j] == False:
                board[i][j] += 1
    return board, attack_each_turn_check

for k in range(K):
    board, blue = step_1_select_attack(board, attack_check)
    attack_each_turn_check[blue[0]][blue[1]] = True

    red = step_2_attack_to(board, turn, attack_check)
    attack_each_turn_check[red[0]][red[1]] = True

    minimum_route_list = step_2_minimum_route(board, blue, red)

    # 레이저 공격
    for i in range(len(minimum_route_list)):
        board[minimum_route_list[i][0]][minimum_route_list[i][1]] -= (board[blue[0]][blue[1]] // 2)
        attack_each_turn_check[minimum_route_list[i][0]][minimum_route_list[i][1]] = True

    board[red[0]][red[1]] -= board[blue[0]][blue[1]]
    board, attack_each_turn_check = step_4_fix_potap(board, attack_each_turn_check)

answer = 0
for i in board:
    if answer < max(i):
        answer = max(i)
print(answer)