N, Q = map(int, input().split())

num_100 = list(map(int, input().split()))

parent_chat_num = num_100[1:(N+1)]
origin_power_num = num_100[N+1:]
on_off_check = [0 for i in range(N)]

# 명령 500
def go_500(num_500):
    candidate_list = []
    def get_parent(num, parent_num, on_off_check):
        num -= 1
        if parent_num[num] != 0:
            if on_off_check[num] == 0:
                k = parent_num[num]
                # print(k)
                candidate_list.append(k)
                get_parent(k, parent_num, on_off_check)

    answer_500 = 0
    for i in range(1, N+1):
        candidate_list = []
        get_parent(i, parent_chat_num, on_off_check)
        candidate_list = candidate_list[:origin_power_num[i-1]]
        if num_500 in candidate_list:
            answer_500 += 1
    print(answer_500)   

# 명령 300
def go_300(num_300_1, num_300_2, origin_power_num):
    origin_power_num[num_300_1 - 1] = num_300_2
    return origin_power_num

# 명령 200
def go_200(num_200, on_off_check):
    if on_off_check[num_200 - 1] == 0:
        on_off_check[num_200 - 1] = -1
    elif on_off_check[num_200 - 1] == -1:
        on_off_check[num_200 - 1] = 0
    return on_off_check

# 명령 400
def go_400(num_400_1, num_400_2, parent_chat_num):
    parent_chat_num[num_400_1 - 1], parent_chat_num[num_400_2 - 1] = parent_chat_num[num_400_2 - 1], parent_chat_num[num_400_1 - 1]
    return parent_chat_num

for i in range(Q-1):
    input_data = list(map(int, input().split()))
    if input_data[0] == 500:
        go_500(input_data[1])
    
    elif input_data[0] == 300:
        # print(input_data[1], input_data[2])
        origin_power_num = go_300(input_data[1], input_data[2], origin_power_num)
    
    elif input_data[0] == 200:
        on_off_check = go_200(input_data[1], on_off_check)
    
    elif input_data[0] == 400:
        parent_chat_num = go_400(input_data[1], input_data[2], parent_chat_num)