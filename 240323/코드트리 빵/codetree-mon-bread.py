# 2차원 시뮬레이션
# 빵을 구하고자 하는 -> m명의 사람
# 1번은 1분, 2번은 2분, ..., m번은 m분
# -> 각자 베이스캠프에서 출발하여 편의점으로 이동하기 시작함.
# 사람들은 출발 시간이 되기 전까지 격자 밖에 나와 있으며, 사람들이 목표로 하는 편의점은 모두 다름.
# 모든 일은 n * n 크기의 격자 위에서 진행됨.

# 코드트리 빵을 구하고 싶은 사람은 다음과 같은 방법으로 움직임.
# 3가지 행동 -> 총 1분 동안 진행됨 -> 정확히 1, 2, 3 순서로 진행되어야 함.

# 1.
# 격자에 있는 사람 -> 모두가 본인이 가고 싶은 편의점 방향을 향해 1칸 움직임.
# 최단거리로 움직임
# 최단거리 움직이는 방법 여러가지면, ↑, ←, →, ↓ 의 우선 순위로 움직이게 됨.
# 최단거리 : 상하좌우 인접한 칸 중 이동가능한 칸으로만 이동하여 도달하기까지 거쳐야 하는 최소가 되는 거리

# 2.
# 편의점 도착 -> 해당 편의점에 멈추게 됨.
# 이때부터 다른 사람들은 해당 편의점이 있는 칸을 지나갈 수 없게 됨.

##### 얘 처리를 잘해야겠는걸
# 격자에 있는 사람들이 모두 이동한 뒤에 해당 칸을 지나갈 수 없어지게 됨에 유의함.

# 3.
# 현재 시간 t분, t <= m을 만족한다면 -> t번 사람은 자신이 가고 싶은 편의점과 가장 가까이에 있는 베이스 캠프에 들어감.
# 가장 가까이에 있는것 -> 최단 거리에 해당하는 곳을 의미함.
# 가장 가까운 베이스캠프가 여러 가지인 경우에는 그 중 행이 작은 베이스캠프, 행이 같다면 열이 작은 베이스 캠프로 들어감.
# t번 사람이 베이스 캠프로 이동하는 데에는 시간이 전혀 소요되지 않음.

# 이때부터 다른 사람들은 해당 베이스 캠프가 있는 칸을 지나갈 수 없게 됨.
# t번 사람이 편의점을 향해 움직이기 시작했더라도 해당 베이스 캠프는 앞으로 절대 지나갈 수 없음에 유의함.
# 마찬가지로 격자에 있는 사람들이 모두 이동한 뒤에 해당 칸을 지나갈 수 없어짐에 유의함.

###################################################
# 격자의 크기 n, 사람의 수 m
n, m = tuple(map(int, input().split()))

# n개의 줄 -> 격자의 정보
# 0 빈칸, 1 베이스캠프
board = []

# 베이스캠프 정보
basecamp_info = []
for i in range(n):
    list_input = list(map(int, input().split()))
    for j in range(len(list_input)):
        if list_input[j] == 1:
            basecamp_info.append([i, j])
    board.append(list_input)

# m개의 줄
# 각자의 사람이 가고자 하는 편의점 위치의 행 x, 열 y
market = []
for i in range(m):
    market_input = list(map(int, input().split()))
    market_input = [market_input[0] - 1, market_input[1] - 1]
    market.append(market_input)

# 이동 가능 여부 체크
# n x n 크기의 격자이므로
move_check = [[0 for i in range(n)] for j in range(n)]

# 1.
# 격자에 있는 사람 -> 모두가 본인이 가고 싶은 편의점 방향을 향해 1칸 움직임.
# 최단거리로 움직임
# 최단거리 움직이는 방법 여러가지면, ↑, ←, →, ↓ 의 우선 순위로 움직이게 됨.
# 최단거리 : 상하좌우 인접한 칸 중 이동가능한 칸으로만 이동하여 도달하기까지 거쳐야 하는 최소가 되는 거리

### 최단 경로
# 비큐 리튜
from collections import deque

dx = [-1, 0, 0, 1]
dy = [0, -1, 1, 0]

def shortest_path_1(start, end, board, move_check):
    start_x, start_y = start[0], start[1]
    end_x, end_y = end[0], end[1]

    visited = [(start_x, start_y)]
    queue = deque([(start_x, start_y, [(start_x, start_y)])])

    while queue:
        queue_x, queue_y, path = queue.popleft()

        if queue_x == end_x and queue_y == end_y:
            return path
        
        for i in range(4):
            nx = queue_x + dx[i]
            ny = queue_y + dy[i]

            if 0 <= nx < n and 0 <= ny < n:
                if board[nx][ny] == 0:
                    if move_check[nx][ny] != -1:
                        if not (nx, ny) in visited:
                            visited.append((nx, ny))
                            queue.append((nx, ny, path + [(nx, ny)]))

def shortest_path_2(start, end, board):
    start_x, start_y = start[0], start[1]
    end_x, end_y = end[0], end[1]

    visited = [(start_x, start_y)]
    queue = deque([(start_x, start_y, [(start_x, start_y)])])

    while queue:
        queue_x, queue_y, path = queue.popleft()

        if queue_x == end_x and queue_y == end_y:
            return path
        
        for i in range(4):
            nx = queue_x + dx[i]
            ny = queue_y + dy[i]

            if 0 <= nx < n and 0 <= ny < n:
                if board[nx][ny] == 0:
                    if not (nx, ny) in visited:
                        visited.append((nx, ny))
                        queue.append((nx, ny, path + [(nx, ny)]))

# 2.
# 편의점 도착 -> 해당 편의점에 멈추게 됨.
# 이때부터 다른 사람들은 해당 편의점이 있는 칸을 지나갈 수 없게 됨.

##### 얘 처리를 잘해야겠는걸
# 격자에 있는 사람들이 모두 이동한 뒤에 해당 칸을 지나갈 수 없어지게 됨에 유의함.
# 

# 3.
# 현재 시간 t분, t <= m을 만족한다면 -> t번 사람은 자신이 가고 싶은 편의점과 가장 가까이에 있는 베이스 캠프에 들어감.
# 가장 가까이에 있는것 -> 최단 거리에 해당하는 곳을 의미함.
# 가장 가까운 베이스캠프가 여러 가지인 경우에는 그 중 행이 작은 베이스캠프, 행이 같다면 열이 작은 베이스 캠프로 들어감.
# t번 사람이 베이스 캠프로 이동하는 데에는 시간이 전혀 소요되지 않음.
                   
# basecamp_info       
def player_where_to_go(basecamp_info, market, move_check):
    candidate = []
    distance = 1e9
    for i in range(len(basecamp_info)):
        if move_check[basecamp_info[i][0]][basecamp_info[i][1]] != -1:
            path = shortest_path_2(basecamp_info[i], market, board)
            if len(path) < distance:
                distance = len(path)
                candidate = []
                candidate.append(basecamp_info[i])
            elif len(path) == distance:
                candidate.append(basecamp_info[i])
    candidate = sorted(candidate, key=lambda x: (x[0], x[1]))
    return candidate[0][0], candidate[0][1]

# 이때부터 다른 사람들은 해당 베이스 캠프가 있는 칸을 지나갈 수 없게 됨.
# t번 사람이 편의점을 향해 움직이기 시작했더라도 해당 베이스 캠프는 앞으로 절대 지나갈 수 없음에 유의함.
# 마찬가지로 격자에 있는 사람들이 모두 이동한 뒤에 해당 칸을 지나갈 수 없어짐에 유의함.

# 사람의 수 m
# m개의 줄에 걸쳐 각 사람들이 가고자 하는 편의점 위치의 행 x, 열 y의 정보

# 어떠한 사람이 원하는 편의점에 도달하지 못하게 되는 경우는 절대 발생하지 않음
# 이동하는 도중 동일한 칸에 둘 이상의 사람이 위치하게 되는 경우 역시 가능함에 유의

### 총 몇 분 후에 모두 편의점에 도착하는지를 구하는 프로그램
answer = 0
player_info = [[-1, -1] for i in range(m)]

t = 0
while player_info != market: 
    for i in range(len(player_info)):
        if player_info[i] == market[i]:
            pass
        else:
            if player_info[i] != [-1, -1]:
                start = player_info[i]
                end = market[i]
                path = shortest_path_1(start, end, board, move_check)
                route = path[1]
                route_x, route_y = route[0], route[1]
                player_info[i] = [route_x, route_y]

    if t <= (m - 1):    
        player_x, player_y = player_where_to_go(basecamp_info, market[t], move_check)
        player_info[t] = [player_x, player_y]

    for i in range(len(player_info)):
        if player_info[i] in market or player_info[i] in basecamp_info:
            move_check[player_info[i][0]][player_info[i][1]] = -1
    t += 1

print(t)