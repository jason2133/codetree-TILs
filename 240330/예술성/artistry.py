# 그림 : n * n 크기의 격자
# 각 칸의 색깔을 1 이상 10 이하의 숫자로 표현

# 예술 점수는 모든 그룹 쌍의 조화로움의 합으로 정의됨.

# 그룹 a와 그룹 b의 조화로움
# (그룹 a에 속한 칸의 수 + 그룹 b에 속한 칸의 수 ) x 그룹 a를 이루고 있는 숫자 값 x 그룹 b를 이루고 있는 숫자 값 x 그룹 a와 그룹 b가 서로 맞닿아 있는 변의 수

# 그룹 쌍 간의 조화로움의 값이 0보다 큰 조합인 것들의 조화로움의 값을 전부 더함.
# -> 초기 예술 점수

# 이후 그림에 대한 회전을 진행함.
# 회전은 정중을 기준으로 두 선을 그어 만들어지는 십자 모양과 그 외의 부분으로 나뉘어 진행됨.

# 십자 모양 -> 통째로 반시계 방향으로 90도 회전함.
# 십자 모양을 제외한 4개의 정사각형 -> 각각 개별적으로 시계 방향으로 90도씩 회전이 진행됨.
### -> 두 부분에 대한 회전이 동시에 진행됨.

##### DFS? BFS?
n = int(input())

from collections import deque

dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

board = []
for i in range(n):
    input_data = list(map(int, input().split()))
    board.append(input_data)

visited_bfs = [[False for i in range(n)] for j in range(n)]

group_list = []

# def bfs(x, y, board, visited_bfs):
#     visited_bfs[x][y] = True
#     group_candidate = [[x, y]]
#     deque_go = deque([(x, y)])

#     # 큐 와 엔 어 투
#     while deque_go:
#         deque_x, deque_y = deque_go.popleft()
#         for i in range(4):
#             nx = deque_x + dx[i]
#             ny = deque_y + dy[i]

#             if 0 <= nx < n and 0 <= ny < n:
#                 if visited_bfs[nx][ny] == False:
#                     if board[nx][ny] == board[deque_x][deque_y]:
#                         visited_bfs[nx][ny] = True
#                         group_candidate.append([nx, ny])
#                         deque_go.append((nx, ny))
#     group_list.append(group_candidate)

# for i in range(n):
#     for j in range(n):
#         bfs(i, j, board, visited_bfs)
    
# for i in group_list:
#     print(i)

def bfs(x, y, board, visited_bfs):
    if visited_bfs[x][y] == True:
        pass
    else:
        visited_bfs[x][y] = True
        group_candidate = [[x, y]]
        deque_go = deque([(x, y)])

        # 큐 와 엔 어 투
        while deque_go:
            deque_x, deque_y = deque_go.popleft()
            for i in range(4):
                nx = deque_x + dx[i]
                ny = deque_y + dy[i]

                if 0 <= nx < n and 0 <= ny < n:
                    if visited_bfs[nx][ny] == False:
                        if board[nx][ny] == board[deque_x][deque_y]:
                            visited_bfs[nx][ny] = True
                            group_candidate.append([nx, ny])
                            deque_go.append((nx, ny))
        group_list.append(group_candidate)

for i in range(n):
    for j in range(n):
        bfs(i, j, board, visited_bfs)
    
# for i in group_list:
#     print(i)

# BFS를 이용하여 각 그룹 분류 완료
    
##### 조화로움 점수 정의
### 그룹 a와 그룹 b의 조화로움
# (그룹 a에 속한 칸의 수 + 그룹 b에 속한 칸의 수)
# 그룹 a를 이루고 있는 숫자 값
# 그룹 b를 이루고 있는 숫자 값
# 그룹 a와 그룹 b가 서로 맞닿아 있는 변의 수
    
## 그룹 a와 그룹 b가 서로 맞닿아 있는 변의 수
# 이거 어케함?
# 그룹 2, 그룹 4 : [1], [3]

from itertools import combinations
list_num = [i for i in range(len(group_list))]
list_combinations = list(combinations(list_num, 2))

# print(list_combinations)

# for i in list_combinations:
#     print(i)

# print(group_list)
# print(group_list[1])
# print(len(group_list[1]))

def group_score_calculate(a, b, group_list, board):
    # (그룹 a에 속한 칸의 수 + 그룹 b에 속한 칸의 수 )
    num_1_a = len(group_list[a])
    num_1_b = len(group_list[b])

    # 그룹 a를 이루고 있는 숫자 값 x 그룹 b를 이루고 있는 숫자 값
    # num_2_a = board[num_1_a[0][0]][num_1_a[0][1]]
    # num_2_b = board[num_1_b[0][0]][num_1_b[0][1]]
    num_2_a = board[group_list[a][0][0]][group_list[a][0][1]]
    num_2_b = board[group_list[b][0][0]][group_list[b][0][1]]

    # 그룹 a와 그룹 b가 서로 맞닿아 있는 변의 수
    num_3_a_and_b = 0
    for i in range(len(group_list[a])):
        num_3_x = group_list[a][i][0]
        num_3_y = group_list[a][i][1]

        for j in range(4):
            nx = num_3_x + dx[j]
            ny = num_3_y + dy[j]

            # 범위 안에 있고
            if 0 <= nx < n and 0 <= ny < n:
                if [nx, ny] in group_list[b]:
                    num_3_a_and_b += 1

    # (그룹 a에 속한 칸의 수 + 그룹 b에 속한 칸의 수 ) x 그룹 a를 이루고 있는 숫자 값 x 그룹 b를 이루고 있는 숫자 값 x 그룹 a와 그룹 b가 서로 맞닿아 있는 변의 수
    answer = (num_1_a + num_1_b) * (num_2_a) * (num_2_b) * (num_3_a_and_b)
    # print(f'{num_1_a} + {num_1_b} * {num_2_a} * {num_2_b} * {num_3_a_and_b}')
    
    return answer

# answer = group_score_calculate(1, 3, group_list, board)
# print(answer)

####### 초기 예술 점수를 구한 뒤에는 그림에 대한 회전을 진행함.
# 회전은 정중을 기준으로 두 선을 그어 만들어지는 십자 모양과 그 외 부분으로 나뉘어 진행
# 1. 두 선을 그어 만들어지는 십자 모양
board_copy = [[0 for i in range(n)] for j in range(n)]
line_length_num = n // 2
anti_clock_pos = []

list_go_1 = []
list_go_2 = []
for i in range(0, line_length_num):
    list_go_1.append([line_length_num, i])
    list_go_2.append([i, line_length_num])
anti_clock_pos.append(list_go_2)
anti_clock_pos.append(list_go_1)

list_go_1 = []
list_go_2 = []
for i in range(line_length_num + 1, n):
    list_go_1.append([line_length_num, i])
    list_go_2.append([i, line_length_num])
anti_clock_pos.append(list_go_2)
anti_clock_pos.append(list_go_1)
# print(anti_clock_pos)
anti_clock_pos_2 = anti_clock_pos.copy()
k = anti_clock_pos_2.pop(0)
anti_clock_pos_2.insert(-1, k)
# print(anti_clock_pos_2)

# def anti_clock_roate(board, board_copy, anti_clock_pos, anti_clock_pos_2):
#     for i in range(len(anti_clock_pos)):
#         board_copy[anti_clock_pos_2[i][0]][anti_clock_pos_2[i][1]] = board[anti_clock_pos[i][0]][anti_clock_pos[i][1]]
#     for i in range(n):
#         for j in range(n):
#             if board_copy[i][j] == 0:
#                 pass
#             else:
#                 board[i][j] = board_copy[i][j]
#     return board

# def anti_clock_roate(board, board_copy, anti_clock_pos, anti_clock_pos_2):
#     for i in range(len(anti_clock_pos)):
#         for j in range(len(anti_clock_pos[i])):
#             board_copy[anti_clock_pos_2[i][j][0]][anti_clock_pos_2[i][j][1]] = board[anti_clock_pos[i][j][0]][anti_clock_pos[i][j][1]]
#     board_copy[n // 2][n // 2] = board[n // 2][n // 2]
#     for i in board_copy:
#         print(i)
#     for i in range(n):
#         for j in range(n):
#             if board_copy[i][j] != 0:
#                 board[i][j] = board_copy[i][j]
#     return board

# board = anti_clock_roate(board, board_copy, anti_clock_pos, anti_clock_pos_2)
# print('anti clock rotate')
# for i in board:
#     print(i)
# print('-'*30)

def anti_clock_roate(board, board_copy, anti_clock_pos, anti_clock_pos_2):
    for i in range(len(anti_clock_pos)):
        for j in range(len(anti_clock_pos[i])):
            board_copy[anti_clock_pos_2[i][j][0]][anti_clock_pos_2[i][j][1]] = board[anti_clock_pos[i][j][0]][anti_clock_pos[i][j][1]]
    board_copy[n // 2][n // 2] = board[n // 2][n // 2]
    return board_copy
    # for i in board_copy:
    #     print(i)
    # for i in range(n):
    #     for j in range(n):
    #         if board_copy[i][j] != 0:
    #             board[i][j] = board_copy[i][j]
    # return board

# board_anti_clock_rotate = anti_clock_roate(board, board_copy, anti_clock_pos, anti_clock_pos_2)
# print('anti clock rotate')
# for i in board:
#     print(i)
# print('-'*30)


# 2. 그 외 부분
line_length_num = n // 2
board_copy = [[0 for i in range(n)] for j in range(n)]

start_pos = [[0, 0], [0, line_length_num + 1], [line_length_num + 1, 0], [line_length_num + 1, line_length_num + 1]]

def clock_rotate(board, board_copy, line_length_num, start_pos):
    for k in range(len(start_pos)):
        for i in range(line_length_num):
            for j in range(line_length_num):
                board_copy[start_pos[k][0] + j][start_pos[k][1] + line_length_num - 1 - i] = board[start_pos[k][0] + i][start_pos[k][1] + j]
    return board_copy
        # board_copy[start_pos[i][0] + line_length_num - 1 - ][start_pos[i][1] + i]

# board_after = clock_rotate(board, board_copy, line_length_num, start_pos)

def one_and_two_sum(board_anti_clock_rotate, board_after):
    for i in range(n):
        for j in range(n):
            if board_anti_clock_rotate[i][j] != 0:
                board_after[i][j] = board_anti_clock_rotate[i][j]
    return board_after

# board_after = one_and_two_sum(board_anti_clock_rotate, board_after)

# for i in board_after:
#     print(i)

######### 실행
real_answer = 0

# 초기 예술 점수
answer_num_1 = 0
for i in range(len(list_combinations)):
    answer = group_score_calculate(list_combinations[i][0], list_combinations[i][1], group_list, board)
    answer_num_1 += answer
# print(answer_num_1)
real_answer += answer_num_1

# 1회
board_copy = [[0 for i in range(n)] for j in range(n)]
board_anti_clock_rotate = anti_clock_roate(board, board_copy, anti_clock_pos, anti_clock_pos_2)
board_after = clock_rotate(board, board_copy, line_length_num, start_pos)
board_after = one_and_two_sum(board_anti_clock_rotate, board_after)
answer_num_1 = 0
for i in range(len(list_combinations)):
    answer = group_score_calculate(list_combinations[i][0], list_combinations[i][1], group_list, board_after)
    answer_num_1 += answer
# print(answer_num_1)
real_answer += answer_num_1

# 2회
board_copy = [[0 for i in range(n)] for j in range(n)]
board_anti_clock_rotate = anti_clock_roate(board_after, board_copy, anti_clock_pos, anti_clock_pos_2)
board_after = clock_rotate(board_after, board_copy, line_length_num, start_pos)
board_after = one_and_two_sum(board_anti_clock_rotate, board_after)
answer_num_1 = 0
for i in range(len(list_combinations)):
    answer = group_score_calculate(list_combinations[i][0], list_combinations[i][1], group_list, board_after)
    answer_num_1 += answer
# print(answer_num_1)
real_answer += answer_num_1

# 3회
board_copy = [[0 for i in range(n)] for j in range(n)]
board_anti_clock_rotate = anti_clock_roate(board_after, board_copy, anti_clock_pos, anti_clock_pos_2)
board_after = clock_rotate(board_after, board_copy, line_length_num, start_pos)
board_after = one_and_two_sum(board_anti_clock_rotate, board_after)
answer_num_1 = 0
for i in range(len(list_combinations)):
    answer = group_score_calculate(list_combinations[i][0], list_combinations[i][1], group_list, board_after)
    answer_num_1 += answer
# print(answer_num_1)
real_answer += answer_num_1

print(real_answer)