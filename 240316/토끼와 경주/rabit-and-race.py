# 1. 경주 시작 준비
# 2. 경주 진행
# 3. 이동거리 변경
# 4. 최고의 토끼 선정

# 명령의 수
Q = int(input())

# 100 경주 시작 준비
num_100 = tuple(map(int, input().split()))

# num_100 = [100, 3, 5, 2, 10, 2, 20, 5]

N, M = num_100[1], num_100[2]
P = num_100[3]

board = [[[] for i in range(M)] for j in range(N)]
# for i in board:
#     print(i)

# 처음 토끼들은 전부 (1행, 1열)에 있음.

rabbit_info = []
for i in range(P):
    # 토끼의 고유번호 pid_i, 이동해야 하는 거리 d_i
    # 토끼의 고유번호 pid_i, 이동해야 하는 거리 d_i, 행 위치, 열 위치, 총 점프 횟수, 토끼의 점수, 이번 턴에 뽑혔나요?
    rabbit_info.append([num_100[4 + 2 * i], num_100[4 + 1 + 2 * i], 0, 0, 0, 0, 100])

# for i in rabbit_info:
#     print(i)

# 200 경주 진행
# 200 K S
# K번의 턴 진행, 우선순위가 가장 높은 토끼에 대하여 점수 S점을 더해줌.
# 우선순위는 순서대로 (현재까지의 총 점프 횟수가 적은 토끼, 현재 서있는 행 번호 + 열 번호가 작은 토끼, 행 번호가 작은 토끼, 열 번호가 작은 토끼, 고유번호가 작은 토끼) 순

# K번의 턴이 모두 진행된 직후에는
# (현재 서있는 행 번호 + 열 번호가 큰 토끼, 행 번호가 큰 토끼, 열 번호가 큰 토끼, 고유번호가 큰 토끼) 순으로 우선순위를 두었을 때 가장 우선순위가 높은 토끼를 골라 점수 S를 더해주게 됨.
# 단, 이 경우에는 K번의 턴 동안 한번이라도 뽑혔던 적이 있던 토끼 중 가장 우선순위가 높은 토끼를 골라야만 함에 꼭 유의
def num_200(K, S, rabbit_info):
    # 상 하 좌 우
    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]

    # 이번 턴에 뽑혔는지, 이거 초기화
    for j in range(len(rabbit_info)):
        rabbit_info[j][-1] = 100

    # K번의 턴 진행
    for i in range(K):
        # 우선순위 정렬
        # 토끼의 고유번호 pid_i, 이동해야 하는 거리 d_i, 행 위치, 열 위치, 총 점프 횟수, 토끼의 점수, 이번 턴에 뽑혔나요?
        rabbit_info = sorted(rabbit_info, key=lambda x: (x[4], (x[2] + x[3]), x[2], x[3], x[0]))
        select_rabbit = rabbit_info[0]
        # print(f'select_rabbit', select_rabbit)
        # print(f'nx {select_rabbit[2]}, ny {select_rabbit[3]}, distance {select_rabbit[1]}')
        select_rabbit_position = []

        # 이동거리
        distance = select_rabbit[1]

        # 이때 이동하는 도중 그 다음 칸이 격자를 벗어나게 된다면 방향을 반대로 바꿔 한 칸 이동
        for j in range(4):

            # # 상
            # if j == 0:
            #     distance_num = distance
            #     nx = select_rabbit[2]
            #     ny = select_rabbit[3]
            #     while distance_num != 0:
            #         if nx + dx[j] >= 0:
            #             nx += dx[j]
            #             ny += dy[j]
            #         else:
            #             nx -= dx[j]
            #             ny -= dy[j]
            #         distance_num -= 1
            #     select_rabbit_position.append([nx, ny])

            # 상
            if j == 0:
                distance_num = distance
                # nx = select_rabbit[2]
                # ny = select_rabbit[3]
                # k = 1
                # while distance_num != 0:
                #     # if nx + dx[j] >= 0:
                #     if nx + (dx[j] * k) >= 0 and nx + (dx[j] * k) <= (N-1):
                #         nx += (dx[j] * k)
                #         ny += (dy[j] * k)
                #     else:
                #         k = k * (-1)
                #         nx += (dx[j] * k)
                #         ny += (dy[j] * k)
                #     distance_num -= 1
                nx = (select_rabbit[2] + distance_num) % (2 * (N-1))
                ny = select_rabbit[3]
                if nx >= N:
                    nx = 2 * (N - 1) - nx
                select_rabbit_position.append([nx, ny])
            
            # 하
            if j == 1:
                distance_num = distance
                # nx = select_rabbit[2]
                # ny = select_rabbit[3]
                # k = 1
                # while distance_num != 0:
                #     # if nx + dx[j] <= (N - 1):
                #     if nx + (dx[j] * k) >= 0 and nx + (dx[j] * k) <= (N-1):    
                #         nx += (dx[j] * k)
                #         ny += (dy[j] * k)
                #     else:
                #         k = k * (-1)
                #         nx += (dx[j] * k)
                #         ny += (dy[j] * k)
                #     distance_num -= 1
                nx = (select_rabbit[2] - distance_num) % (2 * (N-1))
                ny = select_rabbit[3]
                if nx >= N:
                    nx = 2 * (N - 1) - nx

                select_rabbit_position.append([nx, ny])
        
            # 좌
            if j == 2:
                distance_num = distance
                # nx = select_rabbit[2]
                # ny = select_rabbit[3]
                # k = 1
                # while distance_num != 0:
                #     # if ny + dy[j] >= 0:
                #     if ny + (dy[j] * k) >= 0 and ny + (dy[j] * k) <= (M-1):
                #         nx += (dx[j] * k)
                #         ny += (dy[j] * k)
                #     else:
                #         k = k * (-1)
                #         nx += (dx[j] * k)
                #         ny += (dy[j] * k)
                #     distance_num -= 1
                nx = select_rabbit[2]
                ny = (select_rabbit[3] + distance_num) % (2 * (M - 1))
                if ny >= M:
                    ny = 2 * (M - 1) - ny
                select_rabbit_position.append([nx, ny])
            
            # 우
            if j == 3:
                distance_num = distance
                # nx = select_rabbit[2]
                # ny = select_rabbit[3]
                # k = 1
                # while distance_num != 0:
                #     # if nx + dx[j] <= (M - 1):
                #     if ny + (dy[j] * k) >= 0 and ny + (dy[j] * k) <= (M-1):
                #         nx += (dx[j] * k)
                #         ny += (dy[j] * k)
                #     else:
                #         k = k * (-1)
                #         nx += (dx[j] * k)
                #         ny += (dy[j] * k)
                #     distance_num -= 1
                nx = select_rabbit[2]
                ny = (select_rabbit[3] - distance_num) % (2 * (M - 1))
                if ny >= M:
                    ny = 2 * (M - 1) - ny 
                select_rabbit_position.append([nx, ny])

        select_rabbit_position = sorted(select_rabbit_position, key=lambda x: (-(x[0] + x[1]), -x[0], -x[1]))
        # print(f'Turn {i + 1} select_rabbit_position', select_rabbit_position)
        select_rabbit_position_confirm = select_rabbit_position[0]
        rabbit_info[0][2] = select_rabbit_position_confirm[0]
        rabbit_info[0][3] = select_rabbit_position_confirm[1]
        rabbit_info[0][4] += 1
        rabbit_info[0][-1] = 1

        for k in range(1, len(rabbit_info)):
            rabbit_info[k][-2] += (select_rabbit_position_confirm[0] + 1 + select_rabbit_position_confirm[1] + 1)
        # print(f'Turn {i + 1} rabbit info', rabbit_info)
    # K번의 턴이 모두 진행된 직후에는 
    # (현재 서있는 행 번호 + 열 번호가 큰 토끼, 행 번호가 큰 토끼, 열 번호가 큰 토끼, 고유번호가 큰 토끼) 순으로 우선순위를 두었을 때 
    # 가장 우선순위가 높은 토끼를 골라 점수 S를 더해주게 됩니다.
    # 단, 이 경우에는 K번의 턴 동안 한번이라도 뽑혔던 적이 있던 토끼 중 가장 우선순위가 높은 토끼를 골라야만 함에 꼭 유의
    
    # 토끼의 고유번호 pid_i, 이동해야 하는 거리 d_i, 행 위치, 열 위치, 총 점프 횟수, 토끼의 점수, 이번 턴에 뽑혔나요?
    rabbit_info = sorted(rabbit_info, key=lambda x: (x[-1], -(x[2] + x[3]), -x[2], -x[3], -x[0]))
    if rabbit_info[0][-1] == 1:
        rabbit_info[0][-2] += S
    return rabbit_info

# 300 pid_t L
def num_300(pid_t, L, rabbit_info):
    for i in range(len(rabbit_info)):
        if rabbit_info[i][0] == pid_t:
            rabbit_info[i][1] = rabbit_info[i][1] * L
            break
    return rabbit_info

# 400
def num_400(rabbit_info):
    answer = 0
    for i in range(len(rabbit_info)):
        if rabbit_info[i][-2] >= answer:
            answer = rabbit_info[i][-2]
    return answer

# num_200(K, S, rabbit_info, board)
# 토끼의 고유번호 pid_i, 이동해야 하는 거리 d_i, 행 위치, 열 위치, 총 점프 횟수, 토끼의 점수, 이번 턴에 뽑혔나요?
# print(num_200(6, 100, rabbit_info))

for i in range(Q-1):
    input_data = tuple(map(int, input().split()))

    if input_data[0] == 200:
        rabbit_info = num_200(input_data[1], input_data[2], rabbit_info)
    elif input_data[0] == 300:
        rabbit_info = num_300(input_data[1], input_data[2], rabbit_info)
    elif input_data[0] == 400:
        answer = num_400(rabbit_info)
print(answer)