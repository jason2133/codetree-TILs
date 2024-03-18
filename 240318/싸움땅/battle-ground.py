# 총 정보를 저장하는거를 heapq 구조로 할 수 있을듯?
# 그러면 최대 힙, 최소 힙으로 자동으로 되는거잖아?

# n은 격자의 크기, m은 플레이어의 수, k는 라운드의 수
n, m, k = tuple(map(int, input().split()))

gun_info = [[[] for i in range(n)] for j in range(n)]

for i in range(n):
    list_data = list(map(int, input().split()))
    for j in range(n):
        gun_info[i][j].append(list_data[j])

# print(gun_info)
# for i in gun_info:
#     print(i)

player_info = []
player_board = [[[] for i in range(n)] for j in range(n)]
for i in range(m):
    list_data = list(map(int, input().split()))

    list_data.append([])
    
    list_data[0] -= 1
    list_data[1] -= 1

    # 번호, 방향, 플레이어 초기 능력치 / 플레이어가 들고 있는 총
    # player_board[list_data[0]][list_data[1]].append([i, list_data[2], list_data[3], []])
    player_board[list_data[0]][list_data[1]].append([i, list_data[0], list_data[1], list_data[2], list_data[3], []])

    # 얘가 플레이어가 들고 있는 총을 지칭함.
    list_data.insert(0, i)
    player_info.append(list_data)

player_point = [0 for i in range(m)]

# x, y, d, s
# (x, y)는 플레이어의 위치, d는 방향, s는 플레이어의 초기 능력치를 의미
# (x, y)는 플레이어의 위치, d는 방향, s는 플레이어의 초기 능력치 / 플레이어가 들고 있는 총
# 번호 / (x, y)는 플레이어의 위치, d는 방향, s는 플레이어의 초기 능력치 / 플레이어가 들고 있는 총
# for i in player_info:
#     print(i)
# print('-'*30)
# for i in player_board:
#     print(i)
    
# 지금 우리가 다루는 데이터는 총 4개
# gun_info
# player_info
# player_board
# player_point

# 1-1. 첫 번째 플레이어부터 순차적으로 본인이 향하고 있는 방향대로 한 칸만큼 이동
# 방향 d : 0 ~ 3 : 상 우 하 좌
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

def step_1_1_player_move(move_player, player_board):
    player_board[move_player[1]][move_player[2]] = []

    # print('move_player[1]', move_player[1])
    # print('move_player[2]', move_player[2])
    # print('move_player[3]', move_player[3])
    # # print()

    nx = move_player[1] + dx[move_player[3]]
    ny = move_player[2] + dy[move_player[3]]

    if n <= nx:
        nx = (n-1)
        if move_player[3] == 0 or move_player[3] == 1:
            move_player[3] += 2
        else:
            move_player[3] -= 2
    
    if nx < 0:
        nx = 0
        if move_player[3] == 0 or move_player[3] == 1:
            move_player[3] += 2
        else:
            move_player[3] -= 2
    
    if n <= ny:
        ny = (n-1)
        if move_player[3] == 0 or move_player[3] == 1:
            move_player[3] += 2
        else:
            move_player[3] -= 2
    
    if ny < 0:
        ny = 0
        if move_player[3] == 0 or move_player[3] == 1:
            move_player[3] += 2
        else:
            move_player[3] -= 2
    return nx, ny, move_player, player_board

# 번호 / (x, y)는 플레이어의 위치, d는 방향, s는 플레이어의 초기 능력치 / 플레이어가 들고 있는 총
def step_2_1_player(nx, ny, move_player, gun_info, player_board, player_info):
    # player_board[nx][ny].append(move_player)
    
    # 해당 위치에 총이 있는 경우, 해당 플레이어는 총을 획득
    if not gun_info[nx][ny]:
        # 플레이어가 총이 없는 경우
        if not move_player[-1]:
            move_player[-1].append(max(gun_info[nx][ny]))
            gun_info[nx][ny].remove(max(gun_info[nx][ny]))
            player_info[move_player[0]] = move_player
        # 플레이어가 총이 있는 경우
        else:
            if move_player[-1] < max(gun_info[nx][ny]):
                move_player[-1] = []
                move_player[-1].append(max(gun_info[nx][ny]))
                gun_info[nx][ny].remove(max(gun_info[nx][ny]))
                player_info[move_player[0]] = move_player
    player_board[nx][ny].append(move_player)
    return nx, ny, move_player, gun_info, player_board, player_info

# 2-2-1. 만약 이동한 방향에 플레이어가 있는 경우에는 두 플레이어가 싸우게 됨.
# 번호 / (x, y)는 플레이어의 위치, d는 방향, s는 플레이어의 초기 능력치 / 플레이어가 들고 있는 총
def step_2_player_fight(nx, ny, move_player, gun_info, player_board, player_info, player_point, player_num):
    global winner, loser, get_point

    player_1 = move_player
    player_2 = player_board[nx][ny][0]

    # print('player_1', player_1)
    # print('player_2', player_2)

    # player_1_ability = player_1[4] + sum(player_1[5])
    # player_2_ability = player_2[4] + sum(player_2[5])
    player_1_ability = player_1[4] 
    player_2_ability = player_2[4]

    if player_1[5]:
        player_1_ability = player_1[4] + sum(player_1[5])
    
    if player_2[5]:
        player_2_ability = player_2[4] + sum(player_2[5])

    if player_1_ability > player_2_ability:
        winner = player_1
        loser = player_2
        get_point = (player_1[4] + sum(player_1[5])) - (player_2[4] + sum(player_2[5]))

    elif player_1_ability < player_2_ability:
        winner = player_2
        loser = player_1
        get_point = (player_2[4] + sum(player_2[5])) - (player_1[4] + sum(player_1[5]))
    else:
        if player_1[4] > player_2[4]:
            winner = player_1
            loser = player_2
            get_point = (player_1[4] + sum(player_1[5])) - (player_2[4] + sum(player_2[5]))
        elif player_1[4] < player_2[4]:
            winner = player_2
            loser = player_1
            get_point = (player_2[4] + sum(player_2[5])) - (player_1[4] + sum(player_1[5]))
    
    # get_point = 0
    # for i in range(len(player_info)):
    #     # if player_info[i] != winner:
    #     #     get_point += abs(player_info[i][4] - sum(player_info[i][5]))
    #     get_point += abs(player_info[i][4] - sum(player_info[i][5]))
    # # print('player_num', player_num, 'get_point', get_point)
    player_point[player_num] += get_point

    # 2-2-2. 진 플레이어는 본인이 가지고 있는 총을 해당 격자에 내려놓고, 해당 플레이어가 원래 가지고 있던 방향대로 한 칸 이동
    # 만약 이동하려는 칸에 다른 플레이어가 있거나 격자 범위 밖인 경우에는 오른쪽으로 90도씩 회전하여 빈 칸이 보이는 순간 이동
    # 해당 칸에 총이 있다면, 해당 플레이어는 가장 공격력이 높은 총을 획득하고 나머지 총들은 해당 격자에 내려 놓음.
    for i in range(len(loser[-1])):
        gun_info[nx][ny].append(loser[-1][i])
    # gun_info[nx][ny].append(loser[-1].values)
    loser[-1] = []

    for i in range(4):
        d = (loser[3] + i) % 4
        nx = loser[1] + dx[d]
        ny = loser[2] + dy[d]

        if 0 <= nx < n and 0 <= ny < n:
            if not player_board[nx][ny]:
                if gun_info[nx][ny]:
                    # k = max(gun_info[nx][ny])
                    # for j in range(len(loser[-1]))
                    loser[-1].append(max(gun_info[nx][ny]))
                    gun_info[nx][ny].remove(max(gun_info[nx][ny]))
                    player_info[loser[0]] = loser
                    break

    # 2-2-3. 이긴 플레이어는 승리한 칸에 떨어져 있는 총들과 원래 들고 있던 총 중 가장 공격력이 높은 총을 획득하고, 나머지 총들은 해당 격자에 내려 놓음.
    # print('winner[-1]', winner[-1])
    # print('gun_info[nx][ny]', gun_info[nx][ny])

    # if max(winner[-1]) > max(gun_info[nx][ny]):
    #     k = max(winner[-1])
    #     for i in range(len(winner[-1])):
    #         gun_info[nx][ny].append(winner[-1][i])
    #     winner[-1] = [k]
    #     gun_info[nx][ny].remove(k)
    # elif max(winner[-1]) < max(gun_info[nx][ny]):
    #     k = max(gun_info[nx][ny])
    #     for i in range(len(winner[-1])):
    #         gun_info[nx][ny].append(winner[-1][i])
    #     winner[-1] = [k]
    #     gun_info[nx][ny].remove(k)

    if winner[-1] != [] and gun_info[nx][ny] != []:
        # print('winner[-1]', winner[-1])
        # print('gun_info[nx][ny]', gun_info[nx][ny])
        if max(winner[-1]) > max(gun_info[nx][ny]):
            k = max(winner[-1])
            for i in range(len(winner[-1])):
                gun_info[nx][ny].append(winner[-1][i])
            winner[-1] = [k]
            gun_info[nx][ny].remove(k)
        elif max(winner[-1]) < max(gun_info[nx][ny]):
            k = max(gun_info[nx][ny])
            for i in range(len(winner[-1])):
                gun_info[nx][ny].append(winner[-1][i])
            winner[-1] = [k]
            gun_info[nx][ny].remove(k)
    return nx, ny, move_player, gun_info, player_board, player_info, player_point, player_num

for i in range(k):
    for j in range(m):
        move_player = player_info[j]
        nx, ny, move_player, player_board = step_1_1_player_move(move_player, player_board)

        # 만약 이동한 방향에 플레이어가 없다면
        if not player_board[nx][ny]:
            nx, ny, move_player, gun_info, player_board, player_info = step_2_1_player(nx, ny, move_player, gun_info, player_board, player_info)
        
        else:
            # 만약 이동한 방향에 플레이어가 있다면 두 플레이어가 싸우게 됨
            player_num = j
            nx, ny, move_player, gun_info, player_board, player_info, player_point, player_num = step_2_player_fight(nx, ny, move_player, gun_info, player_board, player_info, player_point, player_num)

print(player_point)