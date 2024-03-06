from collections import deque

# 초밥 벨트 길이 L, 명령의 수 Q
L, Q = map(int, input().split())

# 초밥
chobob_board = [[] for i in range(L)]

# 1차원 배열 회전을 보았던 것 같은데
# deque으로 rotate를 할 수 있군!
chobob_board_deque = deque(chobob_board)

# 사람
people_board = [[] for i in range(L)]

# 초밥 회전
def chobob_board_rotate(chobob_board_deque):
    chobob_board_deque.rotate(1)
    return chobob_board_deque

# 100 : 주방장의 초밥 만들기
def make_chobob(chobob_board_deque, num_100):
    chobob_board_deque[int(num_100[2])].append(num_100[3])
    return chobob_board_deque

# 200 : 손님 입장
def customer_go(people_board, num_200):
    people_board[int(num_200[2])].append([num_200[3], int(num_200[4])])
    return people_board

# 300 : 사진 촬영 : 사람 수랑 초밥 수 세기
def count_people_chobob(people_board, chobob_board_deque):
    # 사람 수
    people_count = 0
    for i in range(len(people_board)):
        if people_board[i]:
            people_count += len(people_board[i])
    
    # 초밥 수
    chobob_count = 0
    for i in range(len(list(chobob_board_deque))):
        if chobob_board_deque[i]:
            chobob_count += len(chobob_board_deque[i])
    
    return people_count, chobob_count
    
# 초밥 묵어
def eat_chobob(people_board, chobob_board_deque):
    for i in range(len(people_board)):
        if people_board[i]:
            # print(i, people_board[i], people_board[i][0][0])
            if people_board[i][0][0] in chobob_board_deque[i]:
                # print(chobob_board_deque[i])
                # print(people_board[i][0][0], chobob_board_deque[i].count(people_board[i][0][0]))
                # chobob_board_deque[i].count(people_board[i][0][0]) > people_board[i][0][1]
                # print('count comparison', people_board[i][0][1], chobob_board_deque[i].count(people_board[i][0][0]))

                if people_board[i][0][1] > chobob_board_deque[i].count(people_board[i][0][0]):
                    people_board[i][0][1] -= chobob_board_deque[i].count(people_board[i][0][0])
                    for j in range(chobob_board_deque[i].count(people_board[i][0][0])):
                        chobob_board_deque[i].remove(people_board[i][0][0])
                    if people_board[i][0][1] <= 0:
                        people_board[i].pop()
                
                elif people_board[i][0][1] < chobob_board_deque[i].count(people_board[i][0][0]):
                    for j in range(people_board[i][0][1]):
                        chobob_board_deque[i].remove(people_board[i][0][0])
                    people_board[i][0][1] -= chobob_board_deque[i].count(people_board[i][0][0])
                    if people_board[i][0][1] <= 0:
                        people_board[i].pop()
                
                elif people_board[i][0][1] == chobob_board_deque[i].count(people_board[i][0][0]):
                    # print(chobob_board_deque[i])
                    # print(people_board[i])
                    # print('-'*30)
                    chobob_board_deque[i].remove(people_board[i][0][0])
                    people_board[i].pop()
                    # print(chobob_board_deque[i])
                    # print(people_board[i])
                    # print('-'*30)
                    # people_board[i][0][1] -= chobob_board_deque[i].count(people_board[i][0][0])
                    # if people_board[i][0][1] <= 0:
                    #     people_board[i].pop()

                # people_board[i][0][1] -= chobob_board_deque[i].count(people_board[i][0][0])
                # chobob_board_deque[i].remove(people_board[i][0][0])
                # # print(chobob_board_deque[i])
                # if people_board[i][0][1] <= 0:
                #     people_board[i].pop()
    return people_board, chobob_board_deque

# 명령 리스트 ㄱㄱ
myungryung = []
t = 1
for i in range(Q):
    input_data = tuple(input().split())
    # ('100', '1', '1', 'sam')
    if t != input_data[1]:
        for i in range(int(input_data[1]) - t):
            chobob_board_deque = chobob_board_rotate(chobob_board_deque)
            people_board, chobob_board_deque = eat_chobob(people_board, chobob_board_deque)
    t = int(input_data[1])

    # # 100
    if int(input_data[0]) == 100:
        chobob_board_deque = make_chobob(chobob_board_deque, input_data)
        people_board, chobob_board_deque = eat_chobob(people_board, chobob_board_deque)
    
    # 200
    elif int(input_data[0]) == 200:
        people_board = customer_go(people_board, input_data)
        people_board, chobob_board_deque = eat_chobob(people_board, chobob_board_deque)

    # 300
    elif int(input_data[0]) == 300:
        people_count, chobob_count = count_people_chobob(people_board, chobob_board_deque)
        print(people_count, chobob_count)