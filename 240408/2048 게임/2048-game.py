from copy import deepcopy

# 90도 회전
def rotate(board):
    # 임시 보드판
    temp = [[0] * n for _ in range(n)]

    for x in range(n):
        for y in range(n):
            temp[y][n - x - 1] = board[x][y]

    # 다시 보드판에 복사하기
    for x in range(n):
        for y in range(n):
            board[x][y] = temp[x][y]


# 최댓값 구하기
def get_max(board):
    num = 0
    for x in range(n):
        for y in range(n):
            if num < board[x][y]:
                num = board[x][y]
    return num


# up 방향
def up(board):
    temp = [[0] * n for _ in range(n)]

    for y in range(n):

        # 이전에 값을 옮겼는지 판단, 지금 가리키고 있는 행
        flag, target = 0, -1
        for x in range(n):

            # 값이 비어있다면 pass
            if board[x][y] == 0:
                continue

            # 현재 값과 이동할 곳의 값이 같으면 합쳐준다
            elif board[x][y] == temp[target][y] and flag == 1:
                temp[target][y] *= 2
                flag = 0

            # 아니면 그냥 이동
            else:
                target += 1
                temp[target][y] = board[x][y]
                flag = 1

    # temp를 다시 board에 복사
    for x in range(n):
        for y in range(n):
            board[x][y] = temp[x][y]


# dfs
def dfs(cur, cnt):
    global max_num

    # 종료 조건
    if cnt == 5:
        candi = get_max(cur)

        if max_num < candi:
            max_num = candi
        return

    # 4방향 탐색(board를 90도씩 4번 회전시킴)
    for i in range(4):
        next = deepcopy(cur)
        up(next)
        dfs(next, cnt + 1)
        # 90도 회전
        rotate(cur)


n = int(input())
board = [list(map(int, input().split())) for _ in range(n)]

max_num = 0
dfs(board, 0)
print(max_num)