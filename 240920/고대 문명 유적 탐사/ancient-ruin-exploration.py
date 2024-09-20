import sys
def input():
    return sys.stdin.readline().rstrip()

k, m = map(int, input().split())
board = []
for i in range(5):
    a = list(map(int, input().split()))
    board.append(a)
num_list = list(map(int, input().split()))

arr = [[0 for i in range(5)] for j in range(5)]

# 완전탐색?
# j n-1-i
# n-1-i n-1-j
# n-1-j i

# 3x3 : 9개
# 90, 180, 270 : 3개
### 곱하면 총 개수는 27개

# Starting_point
starting_point = [[0,0], [0,1], [0,2],
                  [1,0], [1,1], [1,2],
                  [2,0], [2,1], [2,2]]

# 회전하는 모든 경우의 수 구했음.
def rotate(arr, board, rotation, starting_point):
    rotate_xy = []
    if rotation == 90:
        # j n-1-i
        for i in range(3):
            for j in range(3):
                arr[starting_point[0] + j][starting_point[1] + 3 - 1 - i] = board[starting_point[0] + i][starting_point[1] + j]
                rotate_xy.append([starting_point[0] + j, starting_point[1] + 3 - 1 - i])
        for i in range(5):
            for j in range(5):
                if [i, j] not in rotate_xy:
                    arr[i][j] = board[i][j]
        return arr
    elif rotation == 180:
        # n-1-i n-1-j
        for i in range(3):
            for j in range(3):
                arr[starting_point[0] + 3 - 1- i][starting_point[1] + 3 - 1 - j] = board[starting_point[0] + i][starting_point[1] + j]
                rotate_xy.append([starting_point[0] + 3 - 1- i, starting_point[1] + 3 - 1 - j])
        for i in range(5):
            for j in range(5):
                if [i, j] not in rotate_xy:
                    arr[i][j] = board[i][j]
        return arr
    elif rotation == 270:
        # n-1-j i
        for i in range(3):
            for j in range(3):
                arr[starting_point[0] + 3 - 1- j][starting_point[1] + i] = board[starting_point[0] + i][starting_point[1] + j]
                rotate_xy.append([starting_point[0] + 3 - 1- j, starting_point[1] + i])
        for i in range(5):
            for j in range(5):
                if [i, j] not in rotate_xy:
                    arr[i][j] = board[i][j]
        return arr

# # 회전하는 경우의 수
# arr_go = rotate(arr, board, 90, starting_point[0])
# for i in arr_go:
#     print(i)

# (1) 유물 1차 획득 가치 최대화
# (2) 그러한 방법이 여러가지인 경우 -> 회전한 각도가 가장 작은 방법을 택함
# (3) 이게 또 여러가지인 경우 -> 회전 중심 좌표의 열이 가장 작은 구간을, 열이 같다면 행이 가장 작은 구간을 택함

# (1) 유물 1차 획득 가치 최대화
# 같은 조각들이 3개 이상 연결된 경우, 조각이 모여 유물이 되고 사라짐.
# 큐 와 왼 어 투
# BFS로 할까?
from collections import deque
visited = [[False for i in range(5)] for j in range(5)]
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]
def bfs(board, x, y, visited, result_list):
    queue_data = deque()
    queue_data.append((x, y))
    # result_list.append([x, y])
    while queue_data:
        queue_data_x, queue_data_y = queue_data.popleft()
        for i in range(4):
            nx = queue_data_x + dx[i]
            ny = queue_data_y + dy[i]
            # 범위 안에 있고
            if 0 <= nx < 5 and 0 <= ny < 5:
                # 방문하지 않았고
                if visited[nx][ny] == False:
                    # 숫자가 같다면
                    if board[nx][ny] == board[queue_data_x][queue_data_y]:
                        visited[nx][ny] = True
                        queue_data.append((nx, ny))
                        result_list.append([nx, ny])

# for i in board:
#     print(i)
# result_list = []
# bfs(board, 1, 1, visited, result_list)
# print(result_list)

def first_yoomul(board):
    final_list = []
    count_num = 0
    for i in range(5):
        for j in range(5):
            result_list = []
            visited = [[False for i in range(5)] for j in range(5)]
            bfs(board, i, j, visited, result_list)
            # print(result_list)
            if len(result_list) >= 3:
                result_list = sorted(result_list)
                if result_list not in final_list:
                    final_list.append(result_list)
                    count_num += len(result_list)
    # (1) 유물 1차 획득 가치 : count_num
    # (2) 회전한 각도 : rotation에 기록될 것임
    # (3) 회전 중심 좌표 열 / 행 : starting_point에 기록될 것임
    return final_list, count_num

#### 유물 회전이랑 1차 획득 가치 최대화 같이 해보자
arr = [[0 for i in range(5)] for j in range(5)]
visited = [[False for i in range(5)] for j in range(5)]
starting_point = [[0,0], [0,1], [0,2],
                  [1,0], [1,1], [1,2],
                  [2,0], [2,1], [2,2]]
rotation_kakdo = [90, 180, 270]

# (1) 유물 1차 획득 가치 최대화
# (2) 그러한 방법이 여러가지인 경우 -> 회전한 각도가 가장 작은 방법을 택함
# (3) 이게 또 여러가지인 경우 -> 회전 중심 좌표의 열이 가장 작은 구간을, 열이 같다면 행이 가장 작은 구간을 택함

# (1) 유물 1차 획득 가치 : count_num
# (2) 회전한 각도 : rotation에 기록될 것임
# (3) 회전 중심 좌표 열 / 행 : starting_point에 기록될 것임

def yoomul_rotation_and_first_value(arr, board, rotation_kakdo, starting_point):
    final_data_check = []
    arr_go = rotate(arr, board, rotation_kakdo, starting_point)
    final_list, count_num = first_yoomul(arr_go)
    final_data_check.append([count_num, rotation_kakdo, starting_point[0], starting_point[1], final_list, arr_go])
    return final_data_check

final_final_data_check = []
starting_point = [[0,0], [0,1], [0,2],
                  [1,0], [1,1], [1,2],
                  [2,0], [2,1], [2,2]]
rotation_kakdo = [90, 180, 270]                  
for i in range(len(starting_point)):
    for j in range(len(rotation_kakdo)):
        arr = [[0 for i in range(5)] for j in range(5)]
        visited = [[False for i in range(5)] for j in range(5)]
        final_data_check = yoomul_rotation_and_first_value(arr, board, rotation_kakdo[j], starting_point[i])
        final_final_data_check.append(final_data_check[0])

final_final_data_check = sorted(final_final_data_check, key=lambda x: (-x[0], x[1], x[2], x[3]))
final_final_final_data = final_final_data_check[0]
print(final_final_final_data)

# 새로운 조각은
# (1) 열 번호가 작은 순으로 조각이 생겨납니다.
# (2) 행 번호가 큰 순으로 조각이 생겨납니다.
new_jokak_index = sum(final_final_final_data[-2], [])
new_jokak_index = sorted(new_jokak_index, key=lambda x: (x[-1], -x[0]))
print(new_jokak_index)
for i in range(len(new_jokak_index)):
    final_final_final_data[-1][new_jokak_index[i][0]][new_jokak_index[i][1]] = num_list[i]

for i in final_final_final_data[-1]:
    print(i)

answer = 0
answer += len(new_jokak_index)
print(answer)