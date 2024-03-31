from collections import deque

N = int(input())
pan = [ list(map(int, input().split())) for _ in range(N) ]

dx, dy = [0, 0, -1, 1], [-1, 1, 0, 0]
def group_search(x, y): # 그룹별로 번호를 매겨주는 함수.

    visited[x][y] = True
    q = deque([(x, y)])

    while q:
        px, py = q.popleft()

        for k in range(4):
            mx = px + dx[k]
            my = py + dy[k]

            if 0 <= mx < N and 0 <= my < N:
                if pan[mx][my] == pan[px][py] and not visited[mx][my]:
                    visited[mx][my] = True
                    group[mx][my] = group_num
                    group_cnt[group_num] += 1
                    q.append((mx, my))


def art_score(): # 예술 점수를 구해주는 함수.

    value = 0

    for i in range(N):
        for j in range(N):
            for k in range(4):
                mx = i + dx[k]
                my = j + dy[k]

                if 0 <= mx < N and 0 <= my < N:
                    if group[mx][my] != group[i][j]:
                        g_x, g_y = group[i][j], group[mx][my] # 번호가 다른 칸들의 좌표
                        g_x_num, g_y_num = pan[i][j], pan[mx][my] # 번호가 다른 칸들의 숫자
                        g_x_cnt, g_y_cnt = group_cnt[g_x], group_cnt[g_y] # 번호가 다른 칸들의 좌표를 활용한 그룹 번호 개수
                        value += (g_x_cnt + g_y_cnt) * g_x_num * g_y_num

    return value // 2 # 한 경우에 대해 2번 계산하게 되므로 2로 나누어 줌.


def plus_rotate(): # 십자가 모양 반시계 방향 회전

    for i in range(N):
        for j in range(N):
            if i == half:
                arr[i][j] = pan[j][i]
            if j == half:
                arr[i][j] = pan[N-j-1][N-i-1]


def square_rotate(x, y, l): # 정사각형 모양 시계 방향 회전

    for i in range(x, x+l):
        for j in range(y, y+l):
            ox, oy = i - x, j - y # (0, 0)으로 변환

            rx, ry = oy, l - ox - 1 # 시계 방향 회전 공식

            arr[rx + x][ry + y] = pan[i][j] # 모든 좌표에 적용할 수 있도록 인자(x, y)를 더해줌.


answer = 0
for _ in range(4):

    group = [[0] * N for _ in range(N)] # 그룹을 분리하기 위해 만든 2차원 배열
    group_cnt = [0] * (N * N + 1) # 그룹별로 개수를 세기위한 배열
    group_num = 0 # 그룹 번호
    visited = [ [False] * N for _ in range(N) ]

    for i in range(N):
        for j in range(N):
            if not visited[i][j]:
                group_num += 1
                group[i][j] = group_num
                group_cnt[group_num] += 1
                group_search(i, j)

    # print("초기 그룹판의 모습")
    # for i in group:
    #     print(i)
    # print(group_cnt)
    # print(group_num)


    answer += art_score()

    # print("예술 점수 합", answer)

    arr = [ [0] * N for _ in range(N) ] # 배열 회전하기 위해 만든 빈 배열
    half = N // 2

    plus_rotate()

    # print()
    # print("십자가 반시계 회전")
    # for i in arr:
    #     print(i)

    square_rotate(0, 0, half)
    square_rotate(0, half+1, half)
    square_rotate(half+1, 0, half)
    square_rotate(half+1, half+1, half)

    for i in range(N):
        for j in range(N):
            pan[i][j] = arr[i][j]

    # print("정사각형 시계방향 회전")
    # for i in arr:
    #     print(i)
    # print("끝")

print(answer)