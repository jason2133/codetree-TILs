from collections import deque

def select_weakest(k):
    temp = [[board[i][j][0], board[i][j][1], i+j, j, i] for i in range(N) for j in range(M) if board[i][j][0] != 0]
    temp = sorted(temp, key=lambda x:(x[0],-x[1],-x[2],-x[3]))
    board[temp[0][4]][temp[0][3]][0] += (N+M) # 핸디캡
    board[temp[0][4]][temp[0][3]][1] = k # 턴수
    return [temp[0][4], temp[0][3]] # 행, 열

def select_strongest(start):
    temp = [[board[i][j][0], board[i][j][1], i + j, j, i] for i in range(N) for j in range(M) if board[i][j][0] != 0 and [i,j]!=start]
    temp = sorted(temp, key=lambda x: (-x[0], x[1], x[2], x[3]))
    return [temp[0][4], temp[0][3]] # 행, 열

def attack(start, end):
    dr = [0, 1, 0, -1]  # 우 하 좌 상
    dc = [1, 0, -1, 0]

    queue = deque()
    queue.append(start)
    visited = [[False for _ in range(M)] for _ in range(N)]
    visited[start[0]][start[1]] = True
    flag = False
    path = [[[0,0] for _ in range(M)] for _ in range(N)] # 최단경로
    path[start[0]][start[1]] = start

    # 최단경로 찾기
    while queue:
        nr, nc = queue.popleft()
        if nr == end[0] and nc == end[1]:
            flag = True
            break
        for i in range(4):
            nextr = nr + dr[i]
            nextc = nc + dc[i]
            # 범위 조정
            if nextr < 0: # 위로 벗어남
                nextr = N-1
            if nextr >= N: # 아래로 벗어남
                nextr = 0
            if nextc < 0: # 왼쪽으로 벗어남
                nextc = M-1
            if nextc >= M: # 오른쪽으로 벗어남
                nextc = 0
            # 부서진 포탑은 지날 수 없음
            if board[nextr][nextc][0] == 0:
                continue
            if visited[nextr][nextc] == False: # 아직 방문 X
                queue.append([nextr, nextc])
                visited[nextr][nextc] = True
                path[nextr][nextc] = [nr, nc]

    damage = board[start[0]][start[1]][0]
    attacked = [start, end]
    board[end[0]][end[1]][0] -= damage  # 공격
    if board[end[0]][end[1]][0] < 0:
        board[end[0]][end[1]][0] = 0
    if flag:
        # 레이저 공격
        tempr, tempc = path[end[0]][end[1]]
        while (tempr, tempc) != (start[0], start[1]):
            # print(tempr, tempc)
            board[tempr][tempc][0] -= damage//2 # 절반 피해
            if board[tempr][tempc][0] < 0:
                board[tempr][tempc][0] = 0
            attacked.append([tempr,tempc])
            tempr, tempc = path[tempr][tempc]
    else:
        # 포탄 공격
        dr = [-1,0,1]
        dc = [-1,0,1]
        for i in range(3):
            for j in range(3):
                nextr, nextc = end[0]+dr[i], end[1]+dc[j]
                if nextr < 0:  # 위로 벗어남
                    nextr = N - 1
                if nextr >= N:  # 아래로 벗어남
                    nextr = 0
                if nextc < 0:  # 왼쪽으로 벗어남
                    nextc = M - 1
                if nextc >= M:  # 오른쪽으로 벗어남
                    nextc = 0
                if board[nextr][nextc][0] == 0 or [dr[i],dc[j]] == [0,0] or [nextr,nextc]==start: # 부서진 포탄은 X
                    continue
                board[nextr][nextc][0] -= damage // 2  # 절반 피해
                if board[nextr][nextc][0] < 0:
                    board[nextr][nextc][0] = 0
                attacked.append([nextr,nextc])

    return attacked

def maintain(attacked):
    for i in range(N):
        for j in range(M):
            if board[i][j][0] > 0 and [i,j] not in attacked:
                board[i][j][0] += 1
    return

def check():
    count = 0
    for i in range(N):
        for j in range(M):
            if board[i][j][0] > 0:
                count += 1
    if count == 1:
        return True
    return False

N, M, K = map(int, input().split())
board = []
INF = 1e8
for _ in range(N):
    row = list(map(int, input().split()))
    b = []
    for r in row:
        b.append([r,0])
    board.append(b)

for k in range(K):
    # 1. 가장 약한 포탑 고르기
    s = select_weakest(k+1) # k턴, 시작점 좌표 반환

    # 2. 가장 강한 포탑 고르기
    e = select_strongest(s) # 시작점 제외, 끝점 좌표 반환

    # 3. 공격하기
    attacked = attack(s,e) # 공격과 상관있는 포탑 반환

    # 4. 정비하기
    maintain(attacked) # 공격과 상관없는 포탑 공격력 + 1

    # for b in board:
    #     print(b)

    # 5. 종료여부 확인하기 (부서지지 않은 포탑 개수=1)
    if check():
        break

# 가장 강한 포탑 찾기
answer = -1
for i in range(N):
    for j in range(M):
        if board[i][j][0] > answer:
            answer = board[i][j][0]

print(answer)