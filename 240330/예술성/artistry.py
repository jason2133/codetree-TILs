### 예술성

# 문제 원리
# 1. n x n 크기의 격자
# 2. 동일한 그룹이 뭔지 -> 각각의 개수 그룹 만들기
# 3. 그룹 간의 조화로움 점수 구하는 함수 짜기
# 4. 십자모양 -> 반시계 방향 90도 회전하기
# 5. 십자모양 제외 4개의 정사각형 -> 각각 개별적으로 시계 방향 90도 회전하기
###### 이걸 반복해서 초기 예술 점수, 1회전 이후 예술 점수, 2회전 이후 예술 점수, 3회전 이후 예술 점수 구하고 이를 합친걸 정답으로 출력함.

##############################################
########## Instruction
# 그림 -> 조화로운 그룹 찾기 -> 그룹 간 조화로움 점수를 계산하는 것을 목표로 함.
# 그림 -> 그리드 형태로 생각 -> 동일한 숫자로 표현된 인접 칸들을 하나의 그룹으로 묶음
# 각 그룹 쌍 간의 조화로움을 계산 -> 전체 예술 점수를 구함. => 초기 예술 점수
# 회전은 십자 모양과 나머지 정사각형 부분으로 나눠 각기 다른 방향으로 진행 
### 이 과정을 총 3번 더 반복하여 최종 점수를 산출함.

##############################################
########## Algorithm
# 그림의 각 행과 각 열 -> 2차원 배열에 저장
# DFS를 사용하여 각 그룹을 형성 -> 번호를 부여
# 각 그룹의 멤버 수는 별도로 기록하여 저장

# 예술 점수는 정의된 규칙에 따라
# 각 그룹의 멤버 수, 묶인 숫자 값, 인접 변의 수를 사용하여 계산
# 모든 이웃한 칸 쌍을 확인하고 조화로움을 더함으로써 초기 예술 점수를 얻음.

# 그림 회전 함수 구현
# 십자 모양을 반시계 방향으로 90도 회전
# 나머지 정사각형 부분을 각각 시계 방향으로 90도 회전
### 회전한 후의 그림에 대하여 다시 그룹을 형성하고 예술 점수를 계산하는 과정을 반복함.
### 이 과정을 4번 실시하여 예술 점수의 합을 최종 결과값으로 출력함.
##############################################

# 변수 선언 및 입력
n = int(input())

arr = [
    list(map(int, input().split()))
    for i in range(n)
]

next_arr = [
    [0] * n
    for i in range(n)
]

# 그룹의 개수를 관리
group_n = 0

# 각 칸에 그룹 번호를 적어줌
group = [
    [0] * n
    for i in range(n)
]

# 각 그룹마다 칸의 수를 세줌
group_cnt = [0] * (n * n + 1)

# 방문 여부
visited = [
    [False] * n
    for i in range(n)
]

dxs = [1, -1, 0, 0]
dys = [0, 0, 1, -1]

def in_range(x, y):
    return 0 <= x and x < n and 0 <= y and y < n

##### DFS를 돌릴 때, 굳이 append를 생각하지 말고, 별도의 저장 리스트를 만들어서 돌리면 되겠구만.
##### 그룹의 번호랑 그 그룹에 속해 있는 요소의 개수를 별도의 저장 리스트에 투입한 것임. 

# (x, y) 위치에서 DFS를 진행함.
def dfs(x, y):
    for i in range(4):
        nx = x + dxs[i]
        ny = y + dys[i]
        
        # 범위 안에 있으면서
        if in_range(nx, ny):
            # 방문하지 않았으면서
            if not visited[nx][ny]:
                # 숫자가 동일하면
                if arr[nx][ny] == arr[x][y]:
                    visited[nx][ny] = True
                    group[nx][ny] = group_n
                    group_cnt[group_n] += 1
                    dfs(nx, ny)
    
# 그룹을 만들어줌.
def make_group():
    global group_n
    
    group_n = 0
    
    # visited 값을 초기화해줌.
    for i in range(n):
        for j in range(n):
            visited[i][j] = False
    
    # DFS를 이용하여 그룹 묶는 작업을 진행함.
    for i in range(n):
        for j in range(n):
            if not visited[i][j]:
                group_n += 1
                visited[i][j] = True
                group[i][j] = group_n
                group_cnt[group_n] = 1
                dfs(i, j)

def get_art_score():
    art_score = 0
    
    # 특정 변을 사이에 두고
    # 두 칸의 그룹이 다른 경우라면
    # (그룹 a에 속한 칸의 수 + 그룹 b에 속한 칸의 수) x 그룹 a를 이루고 있는 숫자 값 x 그룹 b를 이루고 있는 숫자 값
    # 만큼 예술 점수가 더해집니다.
    for i in range(n):
        for j in range(n):
            for dx, dy in zip(dxs, dys):
                nx, ny = i + dx, j + dy
                if in_range(nx, ny) and arr[i][j] != arr[nx][ny]:
                    g1, g2 = group[i][j], group[nx][ny]
                    num1, num2 = arr[i][j], arr[nx][ny]
                    cnt1, cnt2 = group_cnt[g1], group_cnt[g2]
                    
                    art_score += (cnt1 + cnt2) * num1 * num2
    
    # 중복 계산을 제외해줍니다.
    return art_score // 2

def get_score():
    # Step 1. 그룹을 형성합니다.
    make_group()

    # Step 2. 예술 점수를 계산해줍니다.
    return get_art_score()

def rotate_square(sx, sy, square_n):
    # 정사각형을 시계방향으로 90' 회전합니다.
    for x in range(sx, sx + square_n):
        for y in range(sy, sy + square_n):
            # Step 1. (sx, sy)를 (0, 0)으로 옮겨주는 변환을 진행합니다. 
            ox, oy = x - sx, y - sy
            # Step 2. 변환된 상태에서는 회전 이후의 좌표가 (x, y) -> (y, square_n - x - 1)가 됩니다.
            rx, ry = oy, square_n - ox - 1
            # Step 3. 다시 (sx, sy)를 더해줍니다.
            next_arr[rx + sx][ry + sy] = arr[x][y]


def rotate():
    # Step 1. next arr값을 초기화해줍니다.
    for i in range(n):
        for j in range(n):
            next_arr[i][j] = 0
    
    # Step 2. 회전을 진행합니다.
    
    # Step 2 - 1. 십자 모양에 대한 반시계 회전을 진행합니다.
    for i in range(n):
        for j in range(n):
            # Case 2 - 1. 세로줄에 대해서는 (i, j) -> (j, i)가 됩니다.
            if j == n // 2:
                next_arr[j][i] = arr[i][j]
            # Case 2 - 2. 가로줄에 대해서는 (i, j) -> (n - j - 1, i)가 됩니다.
            elif i == n // 2:
                next_arr[n - j - 1][i] = arr[i][j]

    # Step 2 - 2. 4개의 정사각형에 대해 시계 방향 회전을 진행합니다.
    sqaure_n = n // 2
    rotate_square(0, 0, sqaure_n)
    rotate_square(0, sqaure_n + 1, sqaure_n)
    rotate_square(sqaure_n + 1, 0, sqaure_n)
    rotate_square(sqaure_n + 1, sqaure_n + 1, sqaure_n)
    
    # Step 3. next arr값을 다시 옮겨줍니다.
    for i in range(n):
        for j in range(n):
            arr[i][j] = next_arr[i][j]


# 3회전까지의 예술 점수를 더해줍니다.
ans = 0
for _ in range(4):
    # 현재 예술 점수를 더해줍니다.
    ans += get_score()

    # 회전을 진행합니다.
    rotate()

print(ans)