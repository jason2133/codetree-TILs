# 술래잡기 고무줄 놀이

# n x n 크기의 격자
# -> 술래 : 처음 정중앙에 서있음.

# m명의 도망자
# -> 도망자 : 처음 지정된 곳에 서있음. (중앙 X)
# 도망자의 종류
## 1. 좌우로만 움직이는 유형 (항상 오른쪽을 보고 시작)
## 2. 상하로만 움직이는 유형 (항상 아래쪽을 보고 시작)

# h개의 나무
# 나무가 도망자와 초기에 겹쳐서 주어지는 것 역시 가능함.

# 총 k번 반복
# m명의 도망자가 먼저 동시에 움직임
# 그 다음 술래가 움직임
# 도망자가 움직임
# 술래가 움직임
# 도망자가 1턴 -> 술래가 1턴 이런식으로 반복

### 도망자가 움직일 때, 현재 술래와의 거리가 3 이하인 도망자만 움직임
# 거리는 |x1 - x2| + |y1 - y2|로 정의

### 거리 3 이하인 도망자는 1턴동안 다음 규칙에 따라 움직이게 됨.
# 1. 현재 바라보고 있는 방향으로 1칸 움직인다고 했을 때 격자를 벗어나지 않는 경우
# 움직이려는 칸에 술래가 있는 경우라면 움직이지 않음.
# 움직이려는 칸에 술래가 있지 않다면 해당 칸으로 이동함. 해당 칸에 나무가 있어도 괜찮음.

# 2. 현재 바라보고 있는 방향으로 1칸 움직인다 했을 때 격자를 벗어나는 경우
# 먼저 방향을 반대로 틀어줌.
# 바라보고 있는 방향으로 1칸 움직인다 했을 때, 해당 위치에 술래가 없다면 1칸 앞으로 이동함. (술래가 있다면 이동 X)

### 술래가 움직이는 경우
# 달팽이 모양으로 움직임
# 만약 끝에 도달하게 되면, 다시 거꾸로 중심으로 이동함
# 다시 중심에 오게 되면, 처음처럼 위 방향으로 시작하여 시계 방향으로 도는 것
### -> k턴에 걸쳐 반복함.

# 술래는 1번의 턴 동안 정확히 한 칸 해당하는 방향으로 이동하게 됨.
# 이동 후의 위치가 만약 이동방향이 틀어지는 지점이라면, 방향으로 바로 틀어줌.
###### 만약 이동을 통해 양끝에 해당하는 위치인 (1행, 1열) 혹은 정중앙에 도달하게 된다면 이 경우 역시 방향을 바로 틀어줘야 함에 유의함.

# 이동 직후 술래는 턴을 넘기기 전에 시야 내에 있는 도망자를 잡게 됨.
# 술래의 시야는 현재 바라보고 있는 방향을 기준으로 현재 칸을 포함하여 총 3칸
###### 격자 크기에 상관 없이 술래의 시야는 항상 3칸임에 유의함.

# 하지만 만약 나무가 놓여 있는 칸이라면,
# 해당 칸에 있는 도망자는 나무에 가려져 보이지 않게 됨.

# 잡힌 도망자는 사라지게 되고, 
# 술래는 현재 턴을 t번째 턴이라고 했을 때 t x 현재 턴에서 잡힌 도망자의 수만큼의 점수를 얻게됨.

# 다시 도망자의 턴이 진행되고, 이어서 술래의 턴이 진행되는 것을 총 k번에 걸쳐 반복하게 됨.

##### k번에 걸쳐 술래잡기를 진행하는 동안 술래가 총 얻게된 점수를 출력하는 프로그램을 작성

#####################################
# n, m, h, k
# n x n 크기의 격자
# m명의 도망자
# h개의 나무
# k개의 턴

n, m, h, k = tuple(map(int, input().split()))

# -> 술래 : 처음 정중앙에 서있음.
soolae_info = [n // 2, n // 2, 0, 0]

# 단, 이동 도중 도망자들의 위치는 겹칠 수 있음에 유의
board = [[[] for i in range(n)] for j in range(n)]

# m개의 줄 : 도망자의 위치 (x, y) / 이동 방법 d
# d : 1 => 좌우로 움직임
# d : 2 => 상하로 움직임
### 진짜 방향 (좌우 / 상하)

domang_people_info = []
for i in range(m):
    input_data = list(map(int, input().split()))
    input_data[0] -= 1
    input_data[1] -= 1
    input_data.append(0)
    domang_people_info.append(input_data)

# 좌우로 움직이는 사람 -> 항상 오른쪽을 보고 시작함.
dx_1 = [0, 0]
dy_1 = [1, -1]

# 상하로 움직이는 사람 -> 항상 아래쪽을 보고 시작함.
dx_2 = [1, -1]
dy_2 = [0, 0]

# h개의 줄 : 나무의 위치 (x, y) 주어짐.
tree_info = []
for i in range(h):
    input_data = list(map(int, input().split()))
    tree_info.append(input_data)

# 5 3 1 1

### 도망자의 위치
# 2 4 1
# 1 4 2
# 4 2 1

### 나무의 위치
# 2 4

answer = 0

# 도망자와 술래 사이의 거리를 구하는 함수
def distance_between_domang_and_soolae(domang, soolae):
    domang_x, domang_y, type, dir = domang
    soolae_x, soolae_y, dir, up_or_down = soolae
    distance = abs(domang_x - soolae_x) + abs(domang_y - soolae_y)
    return distance

# 도망자 이동하는 함수
def domang_move(domang, soolae):
    domang_x, domang_y, type, dir = domang

    # 이동 방법 d가 1인 경우 좌우로 움직임
    # 좌우로 움직이는 사람은 항상 오른쪽을 보고 시작
    if type == 1:
        nx = domang_x + dx_1[dir]
        ny = domang_y + dy_1[dir]

        # 범위 안에 있을 경우
        if 0 <= nx < n and 0 <= ny < n:
            # 움직이려는 칸에 술래가 있지 않은 경우
            if nx != soolae[0] and ny != soolae[1]:
                domang_x = nx
                domang_y = ny
                domang = [domang_x, domang_y, type, dir]
                return domang
            # 움직이려는 칸에 술래가 있는 경우
            else:
                domang = [domang_x, domang_y, type, dir]
                return domang
    
        # 범위 안에 없는 경우
        else:
            if dir == 0:
                dir = 1
                nx = domang_x + dx_1[dir]
                ny = domang_y + dy_1[dir]

                # 움직이려는 칸에 술래가 있지 않은 경우
                if nx != soolae[0] and ny != soolae[1]:
                    domang_x = nx
                    domang_y = ny
                    domang = [domang_x, domang_y, type, dir]
                    return domang
                else:
                    domang = [domang_x, domang_y, type, dir]
                    return domang
            
            elif dir == 1:
                dir = 0
                nx = domang_x + dx_1[dir]
                ny = domang_y + dy_1[dir]

                # 움직이려는 칸에 술래가 있지 않은 경우
                if nx != soolae[0] and ny != soolae[1]:
                    domang_x = nx
                    domang_y = ny
                    domang = [domang_x, domang_y, type, dir]
                    return domang
                else:
                    domang = [domang_x, domang_y, type, dir]
                    return domang

    # 2인 경우 상하로만 움직임
    # 상하로 움직이는 사람은 항상 아래쪽을 보고 시작
    elif type == 2:
        nx = domang_x + dx_2[dir]
        ny = domang_y + dy_2[dir]

        # 범위 안에 있을 경우
        if 0 <= nx < n and 0 <= ny < n:
            # 움직이려는 칸에 술래가 있지 않은 경우
            if nx != soolae[0] and ny != soolae[1]:
                domang_x = nx
                domang_y = ny
                domang = [domang_x, domang_y, type, dir]
                return domang
            # 움직이려는 칸에 술래가 있는 경우
            else:
                domang = [domang_x, domang_y, type, dir]
                return domang
    
        # 범위 안에 없는 경우
        else:
            if dir == 0:
                dir = 1
                nx = domang_x + dx_2[dir]
                ny = domang_y + dy_2[dir]

                # 움직이려는 칸에 술래가 있지 않은 경우
                if nx != soolae[0] and ny != soolae[1]:
                    domang_x = nx
                    domang_y = ny
                    domang = [domang_x, domang_y, type, dir]
                    return domang
                else:
                    domang = [domang_x, domang_y, type, dir]
                    return domang
            
            elif dir == 1:
                dir = 0
                nx = domang_x + dx_2[dir]
                ny = domang_y + dy_2[dir]

                # 움직이려는 칸에 술래가 있지 않은 경우
                if nx != soolae[0] and ny != soolae[1]:
                    domang_x = nx
                    domang_y = ny
                    domang = [domang_x, domang_y, type, dir]
                    return domang
                else:
                    domang = [domang_x, domang_y, type, dir]
                    return domang

soolae_move_dx = []
soolae_move_dy = []

for i in range(1, n):
    # 홀수인 경우
    if i % 2 == 1:
        for j in range(i):
            soolae_move_dx.append(-1)
            soolae_move_dy.append(0)
        for j in range(i):
            soolae_move_dx.append(0)
            soolae_move_dy.append(1)
    # 짝수인 경우
    else:
        for j in range(i):
            soolae_move_dx.append(1)
            soolae_move_dy.append(0)
        for j in range(i):
            soolae_move_dx.append(0)
            soolae_move_dy.append(-1)
    
# 마지막인 경우
for i in range(n-1):
    if (n-1) % 2 == 0:
        soolae_move_dx.append(-1)
        soolae_move_dy.append(0)
    else:
        soolae_move_dx.append(0)
        soolae_move_dy.append(1)

# print(soolae_move_dx)
# print(soolae_move_dy)
        
soolae_move_dx_2 = soolae_move_dx[::-1]
soolae_move_dy_2 = soolae_move_dy[::-1]
for i in range(len(soolae_move_dx_2)):
    soolae_move_dx_2[i] *= (-1)
    soolae_move_dy_2[i] *= (-1)

dx = [0, 0, 1, -1]
dy = [1, -1, 0, 0]

# # 술래가 움직이는 함수
# def soolae_move(soolae):
#     soolae_x, soolae_y, soolae_index, soolae_up_or_down = soolae

#     if soolae_up_or_down == 0:
#         if soolae_index < len(soolae_move_dx):
#             nx = soolae_x + soolae_move_dx[soolae_index]
#             ny = soolae_y + soolae_move_dy[soolae_index]
#             soolae_index += 1
#             soolae = [nx, ny, soolae_index, soolae_up_or_down]
#             # soolae_dir_x = soolae_move_dx[soolae_index]
#             # soolae_dir_y = soolae_move_dy[soolae_index]
#             return soolae
#         else:
#             soolae_up_or_down = 1
#             soolae_index = 0
#             nx = soolae_x + soolae_move_dx_2[soolae_index]
#             ny = soolae_y + soolae_move_dy_2[soolae_index]
#             soolae = [nx, ny, soolae_index, soolae_up_or_down]
#             return soolae
    
#     elif soolae_up_or_down == 1:
#         if soolae_index < len(soolae_move_dx):
#             nx = soolae_x + soolae_move_dx_2[soolae_index]
#             ny = soolae_y + soolae_move_dy_2[soolae_index]
#             soolae_index += 1
#             soolae = [nx, ny, soolae_index, soolae_up_or_down]
#             return soolae
#         else:
#             soolae_up_or_down = 0
#             soolae_index = 0
#             nx = soolae_x + soolae_move_dx[soolae_index]
#             ny = soolae_y + soolae_move_dy[soolae_index]
#             soolae = [nx, ny, soolae_index, soolae_up_or_down]
#             return soolae

# 술래가 움직이는 함수
def soolae_move(soolae):
    soolae_x, soolae_y, soolae_index, soolae_up_or_down = soolae

    if soolae_up_or_down == 0:
        if soolae_index < len(soolae_move_dx):
            nx = soolae_x + soolae_move_dx[soolae_index]
            ny = soolae_y + soolae_move_dy[soolae_index]
            soolae_index += 1
            soolae = [nx, ny, soolae_index, soolae_up_or_down]
            if soolae_index < len(soolae_move_dx):
                soolae_dir_x = soolae_move_dx[soolae_index]
                soolae_dir_y = soolae_move_dy[soolae_index]
                return soolae, soolae_dir_x, soolae_dir_y
            else:
                soolae_dir_x = soolae_move_dx_2[0]
                soolae_dir_y = soolae_move_dy_2[0]
                return soolae, soolae_dir_x, soolae_dir_y
            # soolae_dir_x = soolae_move_dx[soolae_index]
            # soolae_dir_y = soolae_move_dy[soolae_index]
            # return soolae
        else:
            soolae_up_or_down = 1
            soolae_index = 0
            nx = soolae_x + soolae_move_dx_2[soolae_index]
            ny = soolae_y + soolae_move_dy_2[soolae_index]
            soolae = [nx, ny, soolae_index, soolae_up_or_down]
            soolae_dir_x = soolae_move_dx_2[1]
            soolae_dir_y = soolae_move_dy_2[1]
            return soolae, soolae_dir_x, soolae_dir_y
    
    elif soolae_up_or_down == 1:
        if soolae_index < len(soolae_move_dx):
            nx = soolae_x + soolae_move_dx_2[soolae_index]
            ny = soolae_y + soolae_move_dy_2[soolae_index]
            soolae_index += 1
            soolae = [nx, ny, soolae_index, soolae_up_or_down]
            if soolae_index < len(soolae_move_dx):
                soolae_dir_x = soolae_move_dx_2[soolae_index]
                soolae_dir_y = soolae_move_dy_2[soolae_index]
                return soolae, soolae_dir_x, soolae_dir_y
            else:
                soolae_dir_x = soolae_move_dx[0]
                soolae_dir_y = soolae_move_dy[0]
                return soolae, soolae_dir_x, soolae_dir_y
            # return soolae
        else:
            soolae_up_or_down = 0
            soolae_index = 0
            nx = soolae_x + soolae_move_dx[soolae_index]
            ny = soolae_y + soolae_move_dy[soolae_index]
            soolae = [nx, ny, soolae_index, soolae_up_or_down]
            soolae_dir_x = soolae_move_dx[1]
            soolae_dir_y = soolae_move_dy[1]
            return soolae, soolae_dir_x, soolae_dir_y
            # return soolae

# 술래가 도망자 잡는것
# 술래의 시야는 현재 바라보고 있는 방향을 기준으로 현재 칸을 포함하여 총 3칸입니다. 격자 크기에 상관없이 술래의 시야는 항상 3칸임에 유의
def soolae_catch_domang(soolae, soolae_dir_x, soolae_dir_y, domang_info, t):
    catch_num = 0
    soolae_x = soolae[0]
    soolae_y = soolae[1]

    soolae_range = [[soolae_x, soolae_y]]
    for i in range(1, 3):
        nx = soolae_x + soolae_dir_x * i
        ny = soolae_y + soolae_dir_y * i
        if 0 <= nx < n and 0 <= ny < n:
            soolae_range.append([nx, ny])
    
    for i in range(len(domang_info)):
        if domang_info[i] != [-1, -1]:
            if domang_info[i] in soolae_range:
                domang_info[i] = [-1, -1]
                catch_num += 1
    answer_go = catch_num * t
    return answer_go

##### 구현한 함수
# 도망자와 술래 사이의 거리를 구하는 함수
# def distance_between_domang_and_soolae(domang, soolae):
# return distance

# 도망자 이동하는 함수
# def domang_move(domang, soolae):
# domang = [domang_x, domang_y, type, dir]
# return domang

# 술래가 움직이는 함수
# def soolae_move(soolae):
# return soolae, soolae_dir_x, soolae_dir_y

# # 술래가 도망자 잡는것
# # 술래의 시야는 현재 바라보고 있는 방향을 기준으로 현재 칸을 포함하여 총 3칸입니다. 격자 크기에 상관없이 술래의 시야는 항상 3칸임에 유의
# def soolae_catch_domang(soolae, soolae_dir_x, soolae_dir_y, domang_info, t):
# return catch_num

for turn in range(1, k + 1):
    for i in range(len(domang_people_info)):
        if domang_people_info[i] != [-1, -1]:
            distance = distance_between_domang_and_soolae(domang_people_info[i], soolae_info)
            if distance <= 3:
                domang_people_info[i] = domang_move(domang_people_info[i], soolae_info)
    
    soolae, soolae_dir_x, soolae_dir_y = soolae_move(soolae_info)
    catch_num = soolae_catch_domang(soolae, soolae_dir_x, soolae_dir_y, domang_people_info, turn)
    answer += catch_num

print(answer)