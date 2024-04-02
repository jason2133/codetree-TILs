# Sam의 피자 학교
# 시 위 방 횟
# 와 포 넘 이
# 방 1 횟 1

# 밀가루 양이 담긴 배열의 크기 n
# 최댓값과 최솟값의 차이 k
n, k = tuple(map(int, input().split()))

## n개의 밀가루의 양이 공백을 사이에 두고 주어짐.
milgaroo_list = list(map(int, input().split()))

# 1. 밀가루 양이 가장 작은 위치에 밀가루 1만큼 더 넣어줍니다.
# (가장 작은 위치가 여러 개라면 모두 넣기)
def num_1_milgaroo(milgaroo_list):
    min_value = min(milgaroo_list)
    for i in range(len(milgaroo_list)):
        if milgaroo_list[i] == min_value:
            milgaroo_list[i] += 1
    return milgaroo_list

# 2. 도우를 말아줍니다.
# 먼저 맨 처음 위치부터 하나씩 접어서 위로 올려줍니다. 
# 다음 그림과 같은 순서대로 도우를 말아서 올려줍니다.
### 얘가 중요한 정보인듯
# 도우를 말 때 바닥에 있는 밀가루보다 위에 있는 밀가루의 너비가 더 넓으면 중단

# 시 위 방 횟
# 와 포 넘 이
# 방 1 횟 1

def num_2_dow(milgaroo_list):
    board = [[0] * 4 for i in range(3)]

    x, y = 1, 1

    # 상 좌 하 우
    dx = [-1, 0, 1, 0]
    dy = [0, -1, 0, 1]

    move_dir = 0
    move_num = 1
    data_num = 0

    while data_num != len(milgaroo_list) - 1:
        for i in range(move_num):
            board[x][y] = milgaroo_list[data_num]
            x += dx[move_dir]
            y += dy[move_dir]

            data_num += 1

            if data_num == len(milgaroo_list) - 1:
                x += 1
                y += 1
                board[x][y] = milgaroo_list[data_num]
                return board
            
        move_dir = (move_dir + 1) % 4
        if move_dir == 0 or move_dir == 2:
            move_num += 1

# 3. 도우를 꾹 눌러줍니다.
# 각 위치에 상하좌우로 인접한 두 밀가루의 양을 a, b라고 할 때,
# ∣a−b∣를 5로 나눴을 때의 몫을 d
# a와 b 중 크기가 큰 값에 d를 빼주고, 
# 크기가 작은 값에는 d를 더해줌.
### 얘가 중요!!!
# 모든 위치의 밀가루에서 진행되며 이 과정은 동시에 진행됨.

def num_3_dow(board):
    board_data_for_num_3 = [[0] * len(board[0]) for i in range(len(board))]

    # 상 좌 하 우
    dx = [-1, 0, 1, 0]
    dy = [0, -1, 0, 1]

    for k_x in range(len(board)):
        for k_y in range(len(board[0])):        
            for i in range(4):
                for j in range(4):
                    if i > j:
                        pos_1_x = k_x + dx[i]
                        pos_1_y = k_y + dy[i]

                        pos_2_x = k_x + dx[j]
                        pos_2_y = k_y + dy[j]

                        # 범위 안에 있다면
                        if 0 <= pos_1_x < len(board) and 0 <= pos_2_x < len(board):
                            if 0 <= pos_1_y < len(board[0]) and 0 <= pos_2_y < len(board[0]):
                                diff_and_divide = abs(board[pos_1_x][pos_1_y] - board[pos_2_x][pos_2_y]) // 5

                                # a와 b 중 크기가 큰 값에 d를 빼주고, 크기가 작은 값에는 d를 더해줍
                                if board[pos_1_x][pos_1_y] > board[pos_2_x][pos_2_y]:
                                    board_data_for_num_3[pos_1_x][pos_1_y] -= diff_and_divide
                                    board_data_for_num_3[pos_2_x][pos_2_y] += diff_and_divide
                                elif board[pos_1_x][pos_1_y] < board[pos_2_x][pos_2_y]:
                                    board_data_for_num_3[pos_1_x][pos_1_y] += diff_and_divide
                                    board_data_for_num_3[pos_2_x][pos_2_y] -= diff_and_divide
    # for i in range(len(board)):
    #     for j in range(len(board[0])):
    #         board_data_for_num_3[i][j] += board[i][j]

    return board_data_for_num_3


milgaroo_list = num_1_milgaroo(milgaroo_list)
print('1. 밀가루 양이 가장 작은 위치에 밀가루 1만큼 더 넣어줍니다.')
print(milgaroo_list)
print('-'*30)
print('2. 도우를 말아줍니다.')
board = num_2_dow(milgaroo_list)
for i in board:
    print(i)
print('-'*30)
print('3. 도우를 꾹 눌러줍니다.')
board_data_for_num_3 = num_3_dow(board)
for i in board_data_for_num_3:
    print(i)
print('-'*30)