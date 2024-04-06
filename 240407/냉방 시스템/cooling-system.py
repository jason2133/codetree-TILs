# 설계 11분
# 격자크기, 벽의 개수, 원하는 시원함 정도
N, M, K = map(int, input().split())
aircondition = [[] for _ in range(4)]
arr = [[0 for _ in range(N)] for _ in range(N)]

# 사무실
room = []
for i in range(N):
    list_ = list(map(int, input().split()))
    for j in range(N):
        if list_[j] == 1:
            room.append([i, j])
        if list_[j] >= 2:
            aircondition[list_[j] - 2].append([i, j])

# 상하좌우
wall = [[[0 for _ in range(4)] for _ in range(N)] for _ in range(N)]
for i in range(M):
    y, x, s = map(int, input().split())
    y -= 1
    x -= 1
    if s == 1:
        wall[y][x - 1][3] = 1
        wall[y][x][2] = 1
    else:
        wall[y - 1][x][1] = 1
        wall[y][x][0] = 1


def in_range(y, x):
    if 0 <= y < N and 0 <= x < N:
        return True
    return False


def left(arr, ay, ax):
    start = 5
    queue = []
    copy_arr = [[0 for _ in range(N)] for _ in range(N)]
    if wall[ay][ax + 1][2] == 0 and in_range(ay, ax + 1):
        copy_arr[ay][ax + 1] = start
        queue.append([ay, ax + 1, start])
    while len(queue) > 0:
        dy, dx, idx = queue.pop(0)
        if in_range(dy, dx + 1) and wall[dy][dx + 1][2] == 0:
            copy_arr[dy][dx + 1] = idx - 1
            if idx - 1 != 1:
                queue.append([dy, dx + 1, idx - 1])
        if in_range(dy - 1, dx) and in_range(dy - 1, dx + 1) and wall[dy - 1][dx][1] == 0 and wall[dy - 1][dx + 1][
            2] == 0:
            copy_arr[dy - 1][dx + 1] = idx - 1
            if idx - 1 != 1:
                queue.append([dy - 1, dx + 1, idx - 1])
        if in_range(dy + 1, dx) and in_range(dy + 1, dx + 1) and wall[dy + 1][dx + 1][2] == 0 and wall[dy + 1][dx][
            0] == 0:
            copy_arr[dy + 1][dx + 1] = idx - 1
            if idx - 1 != 1:
                queue.append([dy + 1, dx + 1, idx - 1])
    for i in range(N):
        for j in range(N):
            arr[i][j] += copy_arr[i][j]


# 오른쪽에서 쏨
def right(arr, ay, ax):
    start = 5
    queue = []
    copy_arr = [[0 for _ in range(N)] for _ in range(N)]
    if wall[ay][ax - 1][3] == 0 and in_range(ay, ax - 1):
        copy_arr[ay][ax - 1] = start
        queue.append([ay, ax - 1, start])
    while len(queue) > 0:
        dy, dx, idx = queue.pop(0)
        if in_range(dy, dx - 1) and wall[dy][dx - 1][3] == 0:
            copy_arr[dy][dx - 1] = idx - 1
            if idx - 1 != 1:
                queue.append([dy, dx - 1, idx - 1])
        if in_range(dy - 1, dx) and in_range(dy - 1, dx - 1) and wall[dy - 1][dx - 1][3] == 0 and wall[dy - 1][dx][
            1] == 0:
            copy_arr[dy - 1][dx - 1] = idx - 1
            if idx - 1 != 1:
                queue.append([dy - 1, dx - 1, idx - 1])
        if in_range(dy + 1, dx) and in_range(dy + 1, dx - 1) and wall[dy + 1][dx - 1][3] == 0 and wall[dy + 1][dx][
            0] == 0:
            copy_arr[dy + 1][dx - 1] = idx - 1
            if idx - 1 != 1:
                queue.append([dy + 1, dx - 1, idx - 1])
    for i in range(N):
        for j in range(N):
            arr[i][j] += copy_arr[i][j]


# 위에서 쏨
def up(arr, ay, ax):
    start = 5
    queue = []
    copy_arr = [[0 for _ in range(N)] for _ in range(N)]
    if wall[ay + 1][ax][0] == 0 and in_range(ay + 1, ax):
        copy_arr[ay + 1][ax] = start
        queue.append([ay + 1, ax, start])
    while len(queue) > 0:
        dy, dx, idx = queue.pop(0)
        if in_range(dy + 1, dx) and wall[dy + 1][dx][0] == 0:
            copy_arr[dy + 1][dx] = idx - 1
            if idx - 1 != 1:
                queue.append([dy + 1, dx, idx - 1])
        if in_range(dy, dx - 1) and in_range(dy + 1, dx - 1) and wall[dy][dx - 1][3] == 0 and wall[dy + 1][dx - 1][
            0] == 0:
            copy_arr[dy + 1][dx - 1] = idx - 1
            if idx - 1 != 1:
                queue.append([dy + 1, dx - 1, idx - 1])
        if in_range(dy, dx + 1) and in_range(dy + 1, dx + 1) and wall[dy][dx + 1][2] == 0 and wall[dy + 1][dx + 1][
            0] == 0:
            copy_arr[dy + 1][dx + 1] = idx - 1
            if idx - 1 != 1:
                queue.append([dy + 1, dx + 1, idx - 1])
    for i in range(N):
        for j in range(N):
            arr[i][j] += copy_arr[i][j]

# 아래에서 위로 쏨
def down(arr, ay, ax):
    start = 5
    queue = []
    copy_arr = [[0 for _ in range(N)] for _ in range(N)]
    if wall[ay - 1][ax][1] == 0 and in_range(ay - 1, ax):
        copy_arr[ay - 1][ax] = start
        queue.append([ay - 1, ax, start])
    while len(queue) > 0:
        dy, dx, idx = queue.pop(0)
        if in_range(dy - 1, dx) and wall[dy - 1][dx][1] == 0:
            copy_arr[dy - 1][dx] = idx - 1
            if idx - 1 != 1:
                queue.append([dy - 1, dx, idx - 1])
        if in_range(dy, dx - 1) and in_range(dy - 1, dx - 1) and wall[dy][dx - 1][3] == 0 and wall[dy - 1][dx - 1][
            1] == 0:
            copy_arr[dy - 1][dx - 1] = idx - 1
            if idx - 1 != 1:
                queue.append([dy - 1, dx - 1, idx - 1])
        if in_range(dy, dx + 1) and in_range(dy - 1, dx + 1) and wall[dy][dx + 1][2] == 0 and wall[dy - 1][dx + 1][
            1] == 0:
            copy_arr[dy - 1][dx + 1] = idx - 1
            if idx - 1 != 1:
                queue.append([dy - 1, dx + 1, idx - 1])
    for i in range(N):
        for j in range(N):
            arr[i][j] += copy_arr[i][j]


def mix(arr):
    X = [0, 0, -1, 1]
    Y = [-1, 1, 0, 0]
    diff = []
    for i in range(N):
        for j in range(N):
            for _ in range(4):
                dy = i + Y[_]
                dx = j + X[_]
                if not in_range(dy, dx) or arr[i][j] <= arr[dy][dx]: continue
                if wall[i][j][_] == 1: continue
                dif = (arr[i][j] - arr[dy][dx]) // 4
                if dif != 0:
                    diff.append([i, j, -dif])
                    diff.append([dy, dx, dif])
    for i, j, dif in diff:
        arr[i][j] += dif



def main():
    global arr
    time = 0
    while True:
        time += 1
        if time > 100:
            print(-1)
            break
        for i in range(4):
            if aircondition[i]:
                for ay, ax in aircondition[i]:
                    if i == 0:
                        right(arr, ay, ax)
                    elif i == 1:
                        down(arr, ay, ax)
                    elif i == 2:
                        left(arr, ay, ax)
                    else:
                        up(arr, ay, ax)
        # Mix
        mix(arr)
        #외벽 1 감소
        dy = 0
        dx = 1
        while dx < N - 1:
            arr[dy][dx] -= 1
            dx += 1
        while dy < N - 1:
            arr[dy][dx] -= 1
            dy += 1
        while dx > 0:
            arr[dy][dx] -= 1
            dx -= 1
        while dy >= 0:
            arr[dy][dx] -= 1
            dy -= 1

        for i in range(N):
            for j in range(N):
                arr[i][j] = max(0, arr[i][j])

        flag = 0
        for ry, rx in room:
            if arr[ry][rx] < K:
                flag = 1
                break

        if flag == 0:
            print(time)
            break
main()