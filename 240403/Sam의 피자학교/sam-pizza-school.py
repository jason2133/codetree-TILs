# 변수 선언 및 입력
n, k = tuple(map(int, input().split()))

# 밀가루 양을 관리합니다.
arr = list(map(int, input().split()))

# 동시에 일어나는 처리를 깔끔하게 하기 위해 사용되는 배열입니다.
temp = [0] * n

elapsed_time = 0


def add_one():
    # 최솟값을 찾아 전부 1씩 더해줍니다.
    min_val = min(arr)
    
    for i in range(n):
        if arr[i] == min_val:
            arr[i] += 1


# (row_num, col_num)판을 기준으로 
# 시계방향으로 90' 회전한 이후의 위치를 구합니다.
def rotate(flours, row_num, col_num):
    for i, (x, y) in enumerate(flours):
        flours[i] = (y, row_num - x + 1)


# 도우를 말아줍니다.
def roll_up():
    # 말아올려진 후, 각 숫자들의 위치를 구해줍니다.
    flours = [(0, 0)] * n

    # 처음 2개를 놓고 시작합니다.
    flours[0] = (1, 1)
    flours[1] = (2, 1)
    row_num, col_num = 2, 1
    
    s_index = 2
    # 계속 말아 올려질때까지 반복합니다.
    while s_index + row_num <= n:
        # 기존 숫자들은 90' 회전시켜줍니다.
        rotate(flours, row_num, col_num)
        
        # 새롭게 추가되는 숫자들의 위치를 잡아줍니다.
        for i in range(1, row_num + 1):
            flours[s_index] = (col_num + 1, i)
            s_index += 1

        # 말아 올려진 이후의 row, col 개수를 갱신합니다.
        if row_num == col_num + 1:
            col_num += 1
        else:
            row_num += 1

    # 남아있는 부분의 위치를 계산합니다.
    delta = 1
    while s_index < n:
        flours[s_index] = (row_num, col_num + delta)
        s_index += 1
        delta += 1

    return flours


def re_arrange(flours):
    # temp를 초기화해줍니다.
    for i in range(n):
        temp[i] = 0

    # 열은 오름차순, 행은 내림차순이 되도록 정렬한 뒤, temp에 넣어줍니다.
    extended_flours = [
        (y, -x, i)
        for i, (x, y) in enumerate(flours)
    ]
    extended_flours.sort()

    for i, (_, _, prev_index) in enumerate(extended_flours):
        temp[i] = arr[prev_index]

    # temp 값을 다시 arr에 옮겨줍니다.
    for i in range(n):
        arr[i] = temp[i]


# 두 위치가 인접한 곳인지를 판단합니다.
def adjacency(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2) == 1


def press(flours):
    # temp를 초기화해줍니다.
    for i in range(n):
        temp[i] = arr[i]

    # 인접한 쌍끼리 밀가루 양을 서로 옮겨줍니다.
    for i in range(n):
        for j in range(i + 1, n):
            (x1, y1) = flours[i]
            (x2, y2) = flours[j]
            if adjacency(x1, y1, x2, y2):
                if arr[i] > arr[j]:
                    temp[i] -= (arr[i] - arr[j]) // 5
                    temp[j] += (arr[i] - arr[j]) // 5
                else:
                    temp[i] += (arr[j] - arr[i]) // 5
                    temp[j] -= (arr[j] - arr[i]) // 5
                
    # temp 값을 다시 arr에 옮겨줍니다.
    for i in range(n):
        arr[i] = temp[i]

    # 이제 행이 높은 순서대로 다시 펴주는 작업을 합니다.
    re_arrange(flours)


def fold():
    flours = [(0, 0)] * n
    # 한번 접은 후의 위치 구하기
    for i in range(n // 2):
        flours[i] = (1, n // 2 - i)
    for i in range(n // 2, n):
        flours[i] = (2, i - (n // 2) + 1)

    # 두번 접은 후의 위치 구하기
    for i, (x, y) in enumerate(flours):
        # 접었을 때 위로 올라가는 부분
        if y <= n // 4:
            flours[i] = (3 - x, n // 4 - y + 1)
        # 접었을 때 아래에 남아있는 부분
        else:
            flours[i] = (x + 2, y - n // 4)

    return flours


def simulate():
    global elapsed_time

    # Step 1. 가장 작은 숫자를 찾아 전부 1을 증가시켜줍니다.
    add_one()

    # Step 2. 도우를 말아줍니다.
    flours = roll_up()

    # Step 3. 도우를 꾹 눌러줍니다.
    press(flours)

    # Step 4. 도우를 두 번 반으로 접어줍니다.
    flours = fold()

    # Step 5. 도우를 한번 더 꾹 눌러줍니다.
    press(flours)

    # 횟수를 증가시켜줍니다.
    elapsed_time += 1


def end():
    # 전부 차이가 k 이내인지 판단합니다.
    return max(arr) - min(arr) <= k


# 차이가 k보다 크다면 계속 반복합니다.
while not end():
    simulate()

print(elapsed_time)