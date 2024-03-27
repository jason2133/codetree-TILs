# n x n 격자 : 꼬리잡기놀이

# 3명 이상이 한 팀이 됨.

# 모든 사람들 :
# 자신의 앞 사람의 허리르 잡고 움직이게 됨.
# 맨 앞 사람 : 머리 사람 / 맨 뒤 사람 : 꼬리사람

# 각 팀은 게임에서 주어진 이동 선을 따라서만 이동함.
# 각 팀의 이동 선은 끝이 이어져있음.
# 각 팀의 이동 선은 서로 겹치지 않음.

# 한 라운드
# 1. 먼저 각 팀은 머리사람을 따라서 한 칸을 이동함.
# 2. 각 라운드마다 공이 정해진 선을 따라 던져짐. n개의 행, n개의 열 따라서.
# 4n번째 라운드를 넘어가는 경우에는 다시 1번째 라운드의 방향으로 돌아감.

# 3. 공 던져지는 경우 -> 해당 선 사람 있으면 -> 최초에 만나게 되는 사람 only만이 공을 얻음 -> 점수를 얻게 됨.
# 점수 : 해당 사람이 머리 사람을 시작으로 -> 팀 내에서 k번째 사람이라면 k의 제곱만큼 점수를 얻게 됨.
# 아무도 공을 받지 못하는 경우 -> 아무 점수도 획득하지 못함.

# 공을 획득한 팀의 경우 -> 머리사람 / 꼬리사람이 바뀜. 즉, 방향이 바뀌게 됨.

# 4. 다음 라운드
# 4-1. 1라운드 끝난후
# 4-2. 모든 팀 1칸 이동
# 4-3. 공 발사

# 총 격자의 크기
# 각 팀의 위치
# 각 팀의 이동 선
# 총 진행하는 라운드의 수
##### -> 각 팀이 획득한 점수의 총합을 구하는 프로그램 ㄱㄱ

###########################################################################

# 격자의 크기 n
# 팀의 개수 m
# 라운드 수 k
n, m, k  = tuple(map(int, input().split()))

# 각 팀이 획득한 점수
team_score = [0 for i in range(m)]

# n개의 줄
# 각 행에 해당하는 초기 상태의 정보
# 0 : 빈칸
# 1 : 머리사람
# 2 : 머리사람과 꼬리사람이 아닌 나머지
# 3 : 꼬리사람
# 4 : 이동선

board_info = []
for i in range(n):
    input_data = list(map(int, input().split()))
    board_info.append(input_data)

##### 관리해야 할 데이터
# 격자에서 이동선 (4)
# 1, 2, 3 : 머리사람 / 나머지 / 꼬리사람

# 우하좌상
dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]

# BFS
from collections import deque
visited_bfs = [[False for i in range(n)] for j in range(n)]
group = []

# 큐 와 왼 어 투
def move_line_check(board_info, visited_bfs):
    # global list_save
    group_candidate = []
    for i in range(n):
        for j in range(n):
            if board_info[i][j] == 4:
                if visited_bfs[i][j] == False:
                    list_save = [[i, j]]
                    this_pos = deque([(i, j)])
                    while this_pos:
                        this_pos_x, this_pos_y = this_pos.popleft()
                        for k in range(4):
                            nx = this_pos_x + dx[k]
                            ny = this_pos_y + dy[k]

                            # 범위 안에 있고
                            if 0 <= nx < n and 0 <= ny < n:
                                # 방문하지 않은 곳이라면
                                if visited_bfs[nx][ny] == False:
                                    # 0이 아니라면
                                    if board_info[nx][ny] != 0:
                                        visited_bfs[nx][ny] = True
                                        this_pos.append([nx, ny])
                                        list_save.append([nx, ny])
                    list_save = sorted(list_save)
                    ###
                    list_go = []
                    for kkk in range(len(list_save)):
                        if list_save[kkk] not in list_go:
                            list_go.append(list_save[kkk])
                    ###
                    group_candidate.append(list_go)
    return group_candidate

group_candidate = move_line_check(board_info, visited_bfs)

# 격자에서 이동선 재정렬
# 우하좌상
dx = [0, -1, 1, 0]
dy = [1, 0, 0, -1]

# 머리사람 / 중간 사람 / 꼬리사람
# 1 / 2 / 3
people_info = []

for i in range(len(group_candidate)):
    people_data_info = []
    for j in range(len(group_candidate[i])):
        if board_info[group_candidate[i][j][0]][group_candidate[i][j][1]] == 1:
            people_data_info.append([group_candidate[i][j][0], group_candidate[i][j][1]])
    for j in range(len(group_candidate[i])):
        if board_info[group_candidate[i][j][0]][group_candidate[i][j][1]] == 2:
            people_data_info.append([group_candidate[i][j][0], group_candidate[i][j][1]])
    for j in range(len(group_candidate[i])):
        if board_info[group_candidate[i][j][0]][group_candidate[i][j][1]] == 3:
            people_data_info.append([group_candidate[i][j][0], group_candidate[i][j][1]])
    people_info.append(people_data_info)

### Step 1. 각 팀은 머리 사람을 따라서 한 칸 이동함.
def num_1_move(people_info, group_candidate):
    # 머리 사람
    head_people_x, head_people_y = people_info[0][0], people_info[0][1]
    for i in range(4):
        nx = head_people_x + dx[i]
        ny = head_people_y + dy[i]
        if [nx, ny] in group_candidate:
            people_info.insert(0, [nx, ny])
            people_info.pop()
            break
    return people_info

### Step 2. 각 라운드마다 공이 정해진 선을 따라 던져짐. n개의 행, n개의 열 따라서.
# 4n번째 라운드를 넘어가는 경우에는 다시 1번째 라운드의 방향으로 돌아감.
def num_2_ball(people_info, round_num, team_score):
    round_num += 1
    if round_num > (4*n):
        round_num = round_num % (4*n)

    if 1 <= round_num <= n:
        for k in range(len(people_info)):
            for j in range(n):
                if [round_num - 1, j] in people_info[k]:
                    score = people_info[k].index([round_num - 1, j]) + 1
                    score = score ** 2
                    team_score[k] += score
                    # people_info[k].append(people_info[0])
                    people_info[k][0], people_info[k][-1] = people_info[k][-1], people_info[k][0]
                    break
    
    elif n + 1 <= round_num <= 2*n:
        round_num = round_num - (n + 1)
        for k in range(len(people_info)):
            for j in range(n-1, -1, -1):
                if [j, round_num] in people_info[k]:
                    score = people_info[k].index([j, round_num]) + 1
                    score = score ** 2
                    team_score[k] += score
                    # people_info[k].append(people_info[0])
                    people_info[k][0], people_info[k][-1] = people_info[k][-1], people_info[k][0]
                    break
    
    elif (2*n + 1) <= round_num <= (3*n):
        round_num = 3 * n - round_num
        for k in range(len(people_info)):
            for j in range(n-1, -1, -1):
                if [round_num, j] in people_info[k]:
                    score = people_info[k].index([round_num, j]) + 1
                    score = score ** 2
                    team_score[k] += score
                    people_info[k][0], people_info[k][-1] = people_info[k][-1], people_info[k][0]
                    break
    
    elif (3*n + 1) <= round_num <= (4*n):
        round_num = 4 * n - round_num
        for k in range(len(people_info)):
            for j in range(n):
                if [j, round_num] in people_info[k]:
                    score = people_info[k].index([round_num, j]) + 1
                    score = score ** 2
                    team_score[k] += score
                    people_info[k][0], people_info[k][-1] = people_info[k][-1], people_info[k][0]
                    break

for i in range(k):
    # people_info = num_1_move(people_info, group_candidate)
    for j in range(len(people_info)):
        people_info[j] = num_1_move(people_info[j], group_candidate[j])
    num_2_ball(people_info, i, team_score) 

# print(team_score)
print(sum(team_score))