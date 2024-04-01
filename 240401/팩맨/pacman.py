# 4x4 격자 -> m개의 몬스터, 1개의 팩맨
# 각각의 몬스터 -> 상하좌우, 대각선 방향 중 하나를 가짐.

# 팩맨 게임 -> 턴 단위로 진행됨.
# 한턴은 다음과 같이 진행됨.
# 1. 몬스터 복제 시도
# 2. 몬스터 이동
# 3. 팩맨 이동
# 4. 몬스터 시체 소멸
# 5. 몬스터 복제 완성

# 1. 몬스터 복제 시도
# 현재의 위치에서 자신과 같은 방향을 가진 몬스터를 복제함.
# 복제된 몬스터는 아직은 부화되지 않은 상태로 움직이지 못함.
# 알의 형태를 띄고 있는 복제된 몬스터 -> 현재 시점을 기준으로 각 몬스터와 동일한 방향을 지니게 됨.
# 이후 이 알이 부화할 시 해당 방향을 지닌 채로 꺠어나게 됨.

# 2. 몬스터 이동
# 몬스터는 현재 자신이 가진 방향대로 한 칸 이동함.

# 움직이려는 칸에 몬스터 시체가 있거나, 
# 팩맨이 있는 경우거나 
# 격자를 벗어나는 방향일 경우에는 
### -> 반시계 방향으로 45도를 회전한 뒤 해당 방향으로 갈 수 있는지 판단

# 만약 갈 수 없다면, 
# 가능할 때까지 반시계 방향으로 45도씩 회전하며 
# 해당 방향으로 갈 수 있는지를 확인

# 만약 8 방향을 다 돌았는데도 불구하고, 
# 모두 움직일 수 없었다면 해당 몬스터는 움직이지 않음.

# 3. 팩맨 이동
# 팩맨의 이동은 총 3칸을 이동
# 각 이동마다 상하좌우의 선택지를 가지게 됨.
# 총 4가지의 방향을 3칸 이동 -> 총 64개의 이동 방법이 존재함.

# 몬스터를 가장 많이 먹을 수 있는 방향으로 움직이게 됨.

# 만약 가장 많이 먹을 수 있는 방향이 여러개라면 
# 상 - 하 - 좌 - 우의 우선순위를 가짐.

# 우선순위가 높은 순서대로 배열
#  "상상상 - 상상좌 - 상상하 - 상상우 - 상좌상 - 상좌좌 - 상좌하 - ..."
### -> 이동하는 과정에서 격자 바깥을 나가는 경우는 고려 X

# 이동하는 칸에 있는 몬스터는 모두 먹어치운 뒤, 그 자리에 몬스터의 시체를 남김.
# 팩맨 : 알을 먹지 않음.
# 움직이기 전에 함께 있었던 몬스터도 먹지 않음.
# 이동하는 과정에 있는 몬스터만 먹음.

# 4. 몬스터 시체 소멸
# 몬스터의 시체 -> 총 2턴동안만 유지됨.
# 시체가 생기고 나면 시체가 소멸되기 까지는 총 두 턴을 필요로 함.

# 5. 몬스터 복제 완성
# 알 형태였던 몬스터가 부화
# 처음 복제가 된 몬스터의 방향을 지닌 채로 깨어나게 됨.

##### 모든 턴이 진행되고 난 뒤 살아 남은 몬스터의 마리 수를 출력하는 프로그램을 작성

# 1번째 줄
# 몬스터의 마리 수 m
# 진행되는 턴의 수 t
m, t = tuple(map(int, input().split()))

# 격자
# 4 x 4 크기임
board = [[[] for i in range(4)] for j in range(4)]

### 다루어야 할 캐릭터
# 팩맨 : 7
# 몬스터 : 2
# 몬스터 알 : 1 
# 몬스터 시체 : -2 -> -1 -> 0

# 2번째 줄
# 팩맨의 격자에서의 초기 위치 r, c
pacman_info = list(map(int, input().split()))
board[pacman_info[0] - 1][pacman_info[1] - 1].append([7, 0])

# m개의 줄
# 몬스터의 위치 r, c와 방향 정보 d
# 방향 d는 1부터 순서대로 ↑, ↖, ←, ↙, ↓, ↘, →, ↗ 를 의미
monster_info = []
for i in range(m):
    monster_input = list(map(int, input().split()))
    monster_input[0] -= 1
    monster_input[1] -= 1
    monster_input[2] -= 1
    # monster_info.append(monster_input)
    # 몬스터 번호 / 몬스터의 방향
    board[monster_input[0]][monster_input[1]].append([2, monster_input[2]])

# for i in board:
#     print(i)
# print('-'*30)

# 1. 몬스터 복제 시도
# 현재의 위치에서 자신과 같은 방향을 가진 몬스터를 복제함.
# 복제된 몬스터는 아직은 부화되지 않은 상태로 움직이지 못함.
# 알의 형태를 띄고 있는 복제된 몬스터 -> 현재 시점을 기준으로 각 몬스터와 동일한 방향을 지니게 됨.
# 이후 이 알이 부화할 시 해당 방향을 지닌 채로 꺠어나게 됨.
def num_1_copy_monster(board):
    for i in range(4):
        for j in range(4):
            if board[i][j]:
                for k in range(len(board[i][j])):
                    if board[i][j][k][0] == 2:
                        board[i][j].append([1, board[i][j][k][-1]])
    return board
                
# 2. 몬스터 이동
# 몬스터는 현재 자신이 가진 방향대로 한 칸 이동함.

# 움직이려는 칸에 몬스터 시체가 있거나, 
# 팩맨이 있는 경우거나 
# 격자를 벗어나는 방향일 경우에는 
### -> 반시계 방향으로 45도를 회전한 뒤 해당 방향으로 갈 수 있는지 판단

# 만약 갈 수 없다면, 
# 가능할 때까지 반시계 방향으로 45도씩 회전하며 
# 해당 방향으로 갈 수 있는지를 확인

# 만약 8 방향을 다 돌았는데도 불구하고, 
# 모두 움직일 수 없었다면 해당 몬스터는 움직이지 않음.

# 방향 d는 1부터 순서대로 ↑, ↖, ←, ↙, ↓, ↘, →, ↗ 를 의미
dx = [-1, -1, 0, 1, 1, 1, 0, -1]
dy = [0, -1, -1, -1, 0, 1, 1, 1]

def num_2_monster_move(board):
    board_move_thing = [[[] for i in range(4)] for j in range(4)]
    for i in range(4):
        for j in range(4):
            if board[i][j]:
                for k in range(len(board[i][j])):
                    # 몬스터라면
                    if board[i][j][k][0] == 2:
                        monster_move = board[i][j][k]
                        monster_move_direction = board[i][j][k][-1]

                        for m in range(8):
                            direction = (monster_move_direction + m) % 8
                            nx = i + dx[direction]
                            ny = j + dy[direction]

                            # 격자를 벗어나는 방향일 경우에는 
                            if not (0 <= nx < 4 and 0 <= ny < 4):
                                continue
                            elif [-2, 0] in board[nx][ny] or [-1, 0] in board[nx][ny]:
                                continue
                            elif [7, 0] in board[nx][ny]:
                                continue
                            else:
                                board_move_thing[nx][ny].append([monster_move[0], direction])
                                board[i][j][k] = []
                                break

    for i in range(4):
        for j in range(4):
            if board[i][j] != []:
                if [] in board[i][j]:
                    board[i][j].remove([])
    
    for i in range(4):
        for j in range(4):
            if board_move_thing[i][j] != []:
                board[i][j] += board_move_thing[i][j]
    return board

# 3. 팩맨 이동
# 팩맨의 이동은 총 3칸을 이동
# 각 이동마다 상하좌우의 선택지를 가지게 됨.
# 총 4가지의 방향을 3칸 이동 -> 총 64개의 이동 방법이 존재함.

# 몬스터를 가장 많이 먹을 수 있는 방향으로 움직이게 됨.

# 만약 가장 많이 먹을 수 있는 방향이 여러개라면 
# 상 - 하 - 좌 - 우의 우선순위를 가짐.

# 우선순위가 높은 순서대로 배열
#  "상상상 - 상상좌 - 상상하 - 상상우 - 상좌상 - 상좌좌 - 상좌하 - ..."
### -> 이동하는 과정에서 격자 바깥을 나가는 경우는 고려 X

# 이동하는 칸에 있는 몬스터는 모두 먹어치운 뒤, 그 자리에 몬스터의 시체를 남김.
# 팩맨 : 알을 먹지 않음.
# 움직이기 전에 함께 있었던 몬스터도 먹지 않음.
# 이동하는 과정에 있는 몬스터만 먹음.

# 상 좌 하 우
dx_pacman = [-1, 0, 1, 0]
dy_pacman = [0, -1, 0, 1]

# 상상상 상상좌 상상하 상상우 상좌상 상좌좌 ... 이거 정렬 어케 하지?
# 000
# 001
# 002
# 003
# 010
# 중복순열 아니야?
from itertools import product
input_data = [i for i in range(4)]
list_input = product(input_data, repeat=3)
# for i in list_input:
#     print(i)

list_input = list(list_input)
# print(list_input)

### 중복순열 -> itertools가 아니라 백트래킹으로 구해야 하는데.

def num_3_pacman_move(board, list_input):
    pacman_info = []
    for i in range(4):
        for j in range(4):
            if board[i][j] != []:
                if [7, 0] in board[i][j]:
                    pacman_info.append([i, j])
                    break
    
    monster_num_min = -1
    pacman_candidate = []
    for i in range(64):
        monster_num = 0
        nx = pacman_info[0][0]
        ny = pacman_info[0][1]
        for j in range(3):
            nx += dx_pacman[list_input[i][j]] 
            ny += dy_pacman[list_input[i][j]]

            # 범위 안에 있고
            if 0 <= nx < 4 and 0 <= ny < 4:
                if board[nx][ny] != []:
                    for j in range(len(board[nx][ny])):
                        # 몬스터라면
                        if board[nx][ny][j][0] == 2:
                            monster_num += 1
        
        if monster_num > monster_num_min:
            monster_num_min = monster_num
            pacman_candidate = []
            pacman_candidate.append(list_input[i])
        
        elif monster_num == monster_num_min:
            pacman_candidate.append(list_input[i])
    
    return pacman_info, pacman_candidate

# for i in pacman_candidate:
#     print(i)
# print(pacman_info)
# print(pacman_move_direction)

# # 상 좌 하 우
# dx_pacman = [-1, 0, 1, 0]
# dy_pacman = [0, -1, 0, 1]

def num_3_pacman_eat(board, pacman_info, pacman_move_direction):
    nx = pacman_info[0][0]
    ny = pacman_info[0][1]
    for i in range(3):
        nx += dx_pacman[pacman_move_direction[i]]
        ny += dy_pacman[pacman_move_direction[i]]

        if board[nx][ny] != []:
            for j in range(len(board[nx][ny])):
                if board[nx][ny][j][0] == 2:
                    board[nx][ny][j][0] = -2
    board[pacman_info[0][0]][pacman_info[0][1]].remove([7, 0])
    board[nx][ny].append([7, 0])
    return board 

# 4. 몬스터 시체 소멸
# 몬스터의 시체 -> 총 2턴동안만 유지됨.
# 시체가 생기고 나면 시체가 소멸되기 까지는 총 두 턴을 필요로 함.

def num_4_monster_sichae(board):
    for i in range(4):
        for j in range(4):
            if board[i][j] != []:
                for k in range(len(board[i][j])):
                    if board[i][j][k][0] == -2 or board[i][j][k][0] == -1:
                        board[i][j][k][0] += 1
                    elif board[i][j][k][0] == 0:
                        board[i][j][k] = []
    
    for i in range(4):
        for j in range(4):
            if board[i][j] != []:
                if [] in board[i][j]:
                    board[i][j].remove([])
    return board

# 5. 몬스터 복제 완성
# 알 형태였던 몬스터가 부화
# 처음 복제가 된 몬스터의 방향을 지닌 채로 깨어나게 됨.
def num_5_monster_copy(board):
    for i in range(4):
        for j in range(4):
            if board[i][j] != []:
                for k in range(len(board[i][j])):
                    if board[i][j][k][0] == 1:
                        board[i][j][k][0] = 2
    return board

# 마지막 정답
def final_answer(board):
    answer = 0
    for i in range(4):
        for j in range(4):
            if board[i][j] != []:
                for k in range(len(board[i][j])):
                    if board[i][j][k][0] == 2:
                        answer += 1
    return answer

###################################
for num in range(t):
    board = num_1_copy_monster(board)
    # print('1. 몬스터 복제 시도')
    # for i in board:
    #     print(i)

    board = num_2_monster_move(board)

    # print('-' * 30)
    # # 방향 d는 1부터 순서대로 ↑, ↖, ←, ↙, ↓, ↘, →, ↗ 를 의미
    # print('2. 몬스터 이동')
    # for i in board:
    #     print(i)
    # print('-'*30)

    # print('3. 팩맨 이동')
    pacman_info, pacman_candidate = num_3_pacman_move(board, list_input)
    pacman_move_direction = pacman_candidate[0]
    board = num_3_pacman_eat(board, pacman_info, pacman_move_direction)
    # for i in board:
    #     print(i)

    board = num_4_monster_sichae(board)

    # print('4. 몬스터 시체 소멸')
    # for i in board:
    #     print(i)
    # print('-' * 30)

    board = num_5_monster_copy(board)
    # print('5. 몬스터 복제 완성')
    # for i in board:
    #     print(i)
    # print('-' * 30)

answer = final_answer(board)
print(answer)