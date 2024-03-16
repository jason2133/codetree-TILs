# N x N 크기의 격자 -> (r, c) 형태로 표현됨

# 1. 빈칸
# 참가자가 이동 가능한 칸

# 2. 벽
# 참가자가 이동할 수 없는 칸
# 1 이상 9 이하의 내구도
# 회전할 때, 내구도가 1씩 깎임.
# 내구도가 0이 되면, 빈칸으로 변경됨.

# 3. 출구
# 참가자가 해당 칸에 도달하면, 즉시 탈출함.

### 1초마다 모든 참가자는 한칸씩 움직임

# 두 위치의 최단 거리 -> |x1 - x2| + |y1 - y2|
# 모든 참가자는 동시에 움직임
# 상하좌우로 움직일 수 있으며, 벽이 없는 곳으로 이동할 수 있음.
# 움직인 칸은 현재 머물러 있던 칸보다 출구까지의 최단 거리가 가까워야 함.
# 움직일 수 있는 칸이 2개 이상이라면, 상하로 움직이는 것을 우선시함.
# 참가자가 움직일 수 없는 상황이라면 움직이지 않음.
# 한칸에 2명 이상의 참가자가 있을 수 있음.

### 모든 참가자가 이동을 끝냈으면, 하단 조건에 의해 미로가 회전함.
# 1명 이상의 참가자와 출구를 포함한 가장 작은 정사각형을 잡음.
# 가장 작은 크기를 갖는 정사각형이 2개 이상이라면, 좌상단 r 좌표가 작은 것이 우선시되고, 그래도 같으면 c 좌표가 작은 것이 우선시됨.
# 선택된 정사각형은 시계방향으로 90도 회전하며, 회전된 벽은 내구도가 1씩 깎임

### K초 동안 계속 반복. K초 전에 모든 참가자가 탈출에 성공한다면 게임이 끝남.
# 게임이 끝났을 때, 모든 참가자들의 이동 거리 합과 출구 좌표를 출력하는 프로그램 작성하기.


# N, M, K
# 미로의 크기, 참가자 수, 게임 시간
N, M, K = 5, 3, 8

board = [[0, 0, 0, 0, 1],
         [9, 2, 2, 0, 0],
         [0, 1, 0, 1, 0],
         [0, 0, 0, 1, 0],
         [0, 0, 0, 0, 0]]

player_info = [[1 - 1, 3 - 1],
               [3 - 1, 1 - 1],
               [3 - 1, 5 - 1]]

exit_info = [3 - 1, 3 - 1]

all_move = 0

def calculate_minimum_distance(player_info, exit_info):
    # distance_list = []
    # for i in range(len(player_info)):
    #     distance = abs(player_info[i][0] - exit_info[0]) + abs(player_info[i][1] - exit_info[1])
    #     distance_list.append(distance)
    distance = abs(player_info[0] - exit_info[0]) + abs(player_info[1] - exit_info[1])
    return distance

from collections import deque
def calculate_minimum_path(player_info, exit_info, board):
    # 상 하 좌 우
    # 상하로 움직이는게 먼저
    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]
    
    x = player_info[0]
    y = player_info[1]
    
    visited = [(x, y)]
    # queue = deque([x, y, [(x, y)]])
    queue = deque([(x, y, [(x, y)])])
    
    while queue:
        x_go, y_go, path = queue.popleft()
        
        for i in range(4):
            nx = x_go + dx[i]
            ny = y_go + dy[i]
            
            if nx == exit_info[0] and ny == exit_info[1]:
                path = path + [(nx, ny)]
                return path
            
            if 0 <= nx < N and 0 <= ny < N:
               if board[nx][ny] == 0:
                   if not (nx, ny) in visited:
                       visited.append((nx, ny))
                       queue.append((nx, ny, path + [(nx, ny)]))
    return -1

# 미로 회전 좌측 상단 좌표 구하기
def calculate_square(player_info, exit_info):
    candidate = []
    distance_max = 1e9
    for i in range(len(player_info)):
        distance = calculate_minimum_distance(player_info[i], exit_info)
        if distance < distance_max:
            distance_max = distance
            candidate = []
            candidate.append(player_info[i])
        elif distance == distance_max:
            candidate.append(player_info[i])
    # return candidate, distance
    candidate_pos = []
    dx_candidate = [distance, -distance, 0, 0]
    dy_candidate = [0, 0, distance, -distance]
    for i in range(len(candidate)):
        for j in range(4):
            nx = candidate[i][0] + dx_candidate[j]
            ny = candidate[i][1] + dy_candidate[j]
            if 0 <= nx < N and 0 <= ny < N:
                if not ([nx, ny]) in candidate_pos:
                    candidate_pos.append([nx, ny])
    candidate_pos = sorted(candidate_pos, key=lambda x: (x[0], x[1]))
    candidate_pos = candidate_pos[0]
    return candidate_pos, distance_max

import copy
# 미로 회전
def rotate_board(candidate_pos, exit_info, board):
    board_copy = copy.deepcopy(board)
    
    # for i in range(N):
    #     for j in range(N):
    #         board_copy[j][N - 1 - i] = board[i][j]
    # return board_copy
    
    for i in range(candidate_pos[0], exit_info[0] + 1):
        for j in range(candidate_pos[1], exit_info[1] + 1):
            board_copy[i][j] = board[j - candidate_pos[1]][i - candidate_pos[0]]
            if board_copy[i][j] > 0:
                board_copy[i][j] -= 1
    return board_copy

for sec in range(K):
    if len(player_info) == 0:
        break
    
    # 참가자 이동
    for i in range(len(player_info)):
        distance = calculate_minimum_distance(player_info[i], exit_info)
        minimum_path = calculate_minimum_path(player_info[i], exit_info, board)
        
        if distance == len(minimum_path):
            player_info[i][0] = minimum_path[0][0]
            player_info[i][1] = minimum_path[0][1]
            
            all_move += 1
            
            # exit 도달하면 없애기
            if player_info[i][0] == exit_info[0] and player_info[i][1] == exit_info[1]:
                player_info.remove(player_info[i])
    
    candidate_pos, distance_max = calculate_square(player_info, exit_info)
    board = rotate_board(candidate_pos, exit_info, board)
    
print(all_move)
for i in board:
    print(i)