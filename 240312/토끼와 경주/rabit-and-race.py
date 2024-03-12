# 첫번째 줄
# 명령의 수
Q = 5

# (1) 경주 시작 준비
# 100 N M P pid_1 d_1 pid_2 d_2 ... pid_p d_p 형태로 공백을 사이에 두고 주어짐.
# P 마리의 토끼가 N×M 크기의 격자 위에서 경주를 진행하며 i번 토끼의 고유 번호는 pid_i, 이동해야 하는 거리가 d_i임을 뜻함.
race_start_prepare = [100, 3, 5, 2, 10, 2, 20, 5]

N, M = race_start_prepare[1], race_start_prepare[2]

# P마리의 토끼 -> N x M 크기의 격자 위에서 경주를 진행함.
# 각 토끼 : 고유한 번호
# 한번 움직일 시 꼭 이동해야 할 거리도 정해져 있음.

# i번 토끼의 고유번호 : pid_i
# i번 토끼가 이동해야 하는 거리 : d_i
# -> 처음 토끼들은 전부 (1, 1)에 있음.

board = [[0 for i in range(M)] for j in range(N)]
# for i in board:
#     print(i)
rabbit_num = race_start_prepare[3]
rabbit_info = []
for i in range(rabbit_num):
    # rabbit_info.append([race_start_prepare[4 + 2 * i], race_start_prepare[4 + 1 + 2 * i]])
    rabbit_info.append([race_start_prepare[4 + 2 * i], race_start_prepare[4 + 1 + 2 * i], 0, 0, 0, 0])
# print(rabbit_info)
# [[10, 2], [20, 5]]

# [[10, 2, 0, 0, 0], [20, 5, 0, 0, 0]]
# 토끼 고유번호, 이동해야 하는 거리 / 현재까지의 총 점프 횟수 / 현재 있는 행 번호, 현재 있는 열 번호 / 토끼가 얻은 점수

### (2) 경주 진행
# 가장 우선순위가 높은 토끼를 뽑아 멀리 보내주는 것을 K번 반복함.
# 우선순위는 순서대로 (현재까지의 총 점프 횟수가 적은 토끼, 현재 서있는 행 번호 + 열 번호가 작은 토끼, 행 번호가 작은 토끼, 열 번호가 작은 토끼, 고유번호가 작은 토끼) 순임.
##### => 정렬 필요


# 200 K S
# 우선순위 정렬하기
dx = [-1, 0, 1, 0]
dy = [0, -1, 0, 1]

# 200 6 100
for i in range(6):

    print('Round', i+1)

    rabbit_info = sorted(rabbit_info, key=lambda x: (x[2], (x[3] + x[4]), x[3], x[4], x[0]))
    # print(rabbit_info)
    # 토끼 고유번호, 이동해야 하는 거리 / 현재까지의 총 점프 횟수 / 현재 있는 행 번호, 현재 있는 열 번호 / 토끼가 얻은 점수

    # 가장 우선순위가 높은 토끼가 선정이 되면, 이 토끼 -> i번 토끼
    selected_rabbit = rabbit_info[0]
    # print(selected_rabbit)
    # 토끼 고유번호, 이동해야 하는 거리 / 현재까지의 총 점프 횟수 / 현재 있는 행 번호, 현재 있는 열 번호 / 토끼가 얻은 점수

    # 상하좌우 네 방향으로 각각 d_i만큼 이동했을 때의 위치를 구함.
    # -> 이동하던 도중 그 다음 칸이 격자를 벗어나게 된다면 방향을 반대로 바꿔 한칸 이동하게 됨.

    move_info = []
    for i in range(4):
        # nx = selected_rabbit[3] + dx[i] * selected_rabbit[1]
        # ny = selected_rabbit[4] + dy[i] * selected_rabbit[1]
        nx = selected_rabbit[3] + (dx[i] * selected_rabbit[1])
        ny = selected_rabbit[4] + (dy[i] * selected_rabbit[1])

        print('before', nx, ny)
        # if 0 <= nx < N and 0 <= ny < M:
        #     pass
        # elif 
        # 이동하는 도중 그 다음 칸이 격자를 벗어나게 된다면 방향을 반대로 바꿔 한 칸 이동하게 됨.
        if N <= nx:
            nx = (N-1) - ((dx[i] * selected_rabbit[1]) % N)
        
        if M <= ny:
            ny = (M-1) - ((dy[i] * selected_rabbit[1]) % M)
        
        if nx < 0:
            nx = ((dx[i] * selected_rabbit[1]) % N)
        
        if ny < 0:
            ny = ((dy[i] * selected_rabbit[1]) % M)

        print('revise', nx, ny)
        move_info.append([nx, ny])

    # print(move_info)
    move_info = sorted(move_info, key=lambda x: (-(x[0] + x[1]), -x[0], -x[1]))
    print(move_info)
    move_pos = move_info[0]

    rabbit_info[0][2] += 1
    rabbit_info[0][3] = move_pos[0]
    rabbit_info[0][4] = move_pos[1]

    for i in range(1, rabbit_num):
        rabbit_info[i][-1] += ((move_pos[0] + 1) + (move_pos[1] + 1))

    print(rabbit_info)
    print('-'*30)

print(rabbit_info)






# 이렇게 구해진 4개의 위치 중 (행 번호 + 열 번호가 큰 칸, 행 번호가 큰 칸, 열 번호가 큰 칸) 순으로 우선순위를 두었을 때,
# 가장 우선순위가 높은 칸을 골라, 그 위치로 해당 토끼를 이동시킴.
# -> 이 칸의 위치를 (r_i, c_i)라고 했을 때, i번 토끼를 제외한 나머지 P-1마리의 토끼들은 전부 (r_i + c_i)만큼의 점수를 동시에 얻게 됨.

# K번의 턴 동안 가장 우선순위가 높은 토끼를 뽑아 멀리 보내주는 것을 반복
# 이 과정에서 동일한 토끼가 여러번 선택되는 것 역시 가능

# K번의 턴이 모두 진행된 직후에는 (현재 서있는 행 번호 + 열 번호가 큰 토끼, 행 번호가 큰 토끼, 열 번호가 큰 토끼, 고유번호가 큰 토끼) 순으로 우선순위를 두었을 때
# 가장 우선순위가 높은 토끼를 골라 점수 S를 더해주게 됨.
# -> 이 경우에는, K번의 턴 동안 한번이라도 뽑혔던 적이 있는 토끼 중 가장 우선순위가 높은 토끼를 골라야 함.



# 200 6 100
# 300 10 2
# 200 3 20
# 400

# 토끼 고유번호, 이동해야 하는 거리 / 현재까지의 총 점프 횟수 / 현재 있는 행 번호, 현재 있는 열 번호 / 토끼가 얻은 점수