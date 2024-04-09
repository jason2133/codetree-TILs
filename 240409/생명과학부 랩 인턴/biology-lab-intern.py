# # 1. 승용이는 첫번째 열부터 탐색을 시작합니다.
# # 2. 해당 열의 위에서 아래로 내려가며 탐색할 때 제일 빨리 발견한 곰팡이를 채취합니다. 
# # 곰팡이를 채취하고 나면 해당 칸은 빈칸이 되며, 
# # 해당 열에서 채취할 수 있는 곰팡이가 없는 경우도 있을 수 있음에 유의합니다

# # 3. 해당 열에서 채취 시도가 끝나고 나면 곰팡이는 이동을 시작합니다.

# # 4. 입력으로 주어진 방향과 속력으로 이동하며 격자판의 벽에 도달하면 
# # 반대로 방향을 바꾸고 속력을 유지한 채로 이동합니다. 
# # 방향을 바꿀 때는 시간이 걸리지 않습니다.

# # 5. 모든 곰팡이가 이동을 끝낸 후에 
# # 한 칸에 곰팡이가 두마리 이상일 때는 
# # 크기가 큰 곰팡이가 다른 곰팡이를 모두 잡아먹습니다.

# # 6. 이 모든 과정은 1초가 걸리며 이후 승용이는 오른쪽 열로 이동해서 위의 과정을 반복합니다.

# # 격자판의 크기 n, m과 곰팡이의 수 k
# n, m, k = tuple(map(int, input().split()))
# board = [[[] for i in range(m)] for j in range(n)]

# # 곰팡이의 정보 x, y, s, d, b
# # x, y는 곰팡이의 위치
# # s는 1초동안 곰팡이가 움직이는 거리
# # d는 이동 방향
# # b는 곰팡이의 크기
# for i in range(k):
#     input_data = list(map(int, input().split()))
#     input_data[0] -= 1
#     input_data[1] -= 1
#     board[input_data[0]][input_data[1]].append(input_data[2:])

# ### 인턴이 채취한 곰팡이 크기의 총 합을 출력

# def num_1_search(starting_point, board, answer):
#     for i in range(n):
#         if board[i][starting_point]:
#             answer += board[i][starting_point][0][-1]
#             board[i][starting_point] = []
#             break
#     return board, answer

# # d는 1~4까지의 정수로 주어지며
# # 1인 경우는 위, 
# # 2인 경우는 아래, 
# # 3인 경우는 오른쪽, 
# # 4인 경우는 왼쪽
# def next_loc(i, j, s, d):
#     # 위 아래
#     if d == 1 or d == 2:
#         cycle = 2*n - 2
#         if d == 2:
#             s += i
#         elif d == 1:
#             s += (2*n - 2 - i)
        
#         s %= cycle
#         if s >= n:
#             return (2*n - 2 - s, j, 1)
#         else:
#             return (s, j, 2)
    
#     # 왼쪽 오른쪽
#     elif d == 3 or d == 4:
#         cycle = 2*m - 2
#         # 오른쪽
#         if d == 4:
#             s += j
#         # 왼쪽
#         elif d == 3:
#             s += (2*m - 2- j)
        
#         s %= cycle
#         if s >= m:
#             return (i, 2*m - 2 - s, 3)
#         else:
#             return (i, s, 4)

# # 곰팡이의 정보 x, y, s, d, b
# # x, y는 곰팡이의 위치
# # s는 1초동안 곰팡이가 움직이는 거리
# # d는 이동 방향
# # b는 곰팡이의 크기
# # def next_loc(i, j, s, d)
# def move_gompangei(board):
#     for i in range(n):
#         for j in range(m):
#             if board[i][j]:
#                 gompangei = board[i][j][0]
#                 next_x, next_y, next_dir = next_loc(i, j, gompangei[0], gompangei[1])
#                 board[next_x][next_y].append([gompangei[0], next_dir, gompangei[-1]])
#                 board[i][j].remove(gompangei)
#                 if len(board[next_x][next_y]) >= 2:
#                     max_value = max(board[next_x][next_y], key=lambda x: x[-1])
#                     board[next_x][next_y] = [max_value]
#     return board

# starting_point = -1
# answer = 0

# for i in range(m):
#     starting_point += 1
#     board, answer = num_1_search(starting_point, board, answer)
#     board = move_gompangei(board)

# print(answer)
###############################################################

# R, C, M = tuple(map(int, input().split()))
# board = [[[] for i in range(C)] for j in range(R)]

# for i in range(M):
#     shark = list(map(int, input().split()))
#     shark[0] -= 1
#     shark[1] -= 1
#     board[shark[0]][shark[1]].append(shark[2:])

# nakksi_king = -1
# answer = 0

# def num_1_nakksi_move(nakksi_king, board, answer):
#     for i in range(R):
#         if board[i][nakksi_king]:
#             answer += board[i][nakksi_king][0][-1]
#             board[i][nakksi_king] = []
#             break
#     return board, answer

# # s는 속력, d는 이동 방향, z는 크기
# # d가 1인 경우는 위, 2인 경우는 아래, 3인 경우는 오른쪽, 4인 경우는 왼쪽

# def cal_next_loc(i, j, s, d):
#     # 위 혹은 아래
#     if d == 1 or d == 2:
#         cycle = 2 * R - 2
#         if d == 2:
#             s += i
#         elif d == 1:
#             s += (2*R - 2 - i)
        
#         s %= cycle
#         if s >= R:
#             s = (2*R - 2 - s)
#             return (s, j)
#         return (s, j)
#     # 오른쪽 혹은 왼쪽
#     else:
#         cycle = 2 * C - 2
#         if d == 3:
#             s += j
#         elif d == 4:
#             s += (2*C - 2 - j)
        
#         s %= cycle
#         if s >= C:
#             s = (2*C - 2 - s)
#             return (i, s)
#         return (i, s)

# def num_3_shark_move(board):
#     for i in range(R):
#         for j in range(C):
#             if board[i][j]:
#                 shark = board[i][j][0]
#                 next_x, next_y = cal_next_loc(i, j, shark[0], shark[1])
#                 board[next_x][next_y].append(board[i][j][0])
#                 # board[i][j] = []
#                 board[i][j].remove(board[i][j][0])
#                 if len(board[next_x][next_y]) >= 2:
#                     board[next_x][next_y] = [max(board[next_x][next_y], key=lambda x: x[-1])]
#     return board

# for i in range(C):
#     nakksi_king += 1
#     board, answer = num_1_nakksi_move(nakksi_king, board, answer)
#     board = num_3_shark_move(board)

# print(answer)

import sys
# sys.setrecursionlimit(10 ** 8)
input = lambda: sys.stdin.readline().rstrip()


def fish(j):
    for i in range(R):
        if board[i][j]:
            x = board[i][j][2]
            board[i][j] = 0
            return x
    return 0


def move():
    global board  # board[i][j] 안에는 (s,d,z)의 값이 들어있음. 상어가 없는 경우엔 0이 들어있음
    new_board = [[0 for _ in range(C)] for _ in range(R)]  # 상어들의 새 위치를 담을 공간
    for i in range(R):
        for j in range(C):
            if board[i][j]:
                # 이 상어의 다음 위치는
                ni, nj, nd = get_next_loc(i, j, board[i][j][0], board[i][j][1])
                if new_board[ni][nj]:
                    new_board[ni][nj] = max(
                        new_board[ni][nj],
                        (board[i][j][0], nd, board[i][j][2]),
                        key=lambda x: x[2],
                    )
                else:
                    new_board[ni][nj] = (board[i][j][0], nd, board[i][j][2])

    board = new_board  # board가 이제 상어들의 새 위치를 가리키도록


def get_next_loc(i, j, speed, dir):

    if dir == UP or dir == DOWN:  # i
        cycle = R * 2 - 2
        if dir == UP:
            speed += 2 * (R - 1) - i
        else:
            speed += i

        speed %= cycle
        if speed >= R:
            return (2 * R - 2 - speed, j, UP)
        return (speed, j, DOWN)

    else:  # j
        cycle = C * 2 - 2
        if dir == LEFT:
            speed += 2 * (C - 1) - j
        else:
            speed += j

        speed %= cycle
        if speed >= C:
            return (i, 2 * C - 2 - speed, LEFT)
        return (i, speed, RIGHT)


UP, DOWN, RIGHT, LEFT = 1, 2, 3, 4
R, C, M = map(int, input().split())
board = [[0 for _ in range(C)] for _ in range(R)]

for i in range(M):
    r, c, s, d, z = map(int, input().split())
    r, c = r - 1, c - 1
    board[r][c] = (s, d, z)
    # s : speed
    # d : 1(up), 2(down), 3(right), 4(left)
    # z : size


ans = 0
for j in range(C):
    ans += fish(j)
    move()

print(ans)