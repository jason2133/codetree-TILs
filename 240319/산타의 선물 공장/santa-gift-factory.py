# 산타의 선물 공장

# 명령의 수
q = int(input())

# 1번째 줄 : 공장 설립
# 100 n m ID1 ID2 ... IDn W1 W2 ... Wn 형태로 공백을 사이에 두고 주어짐.

# m개의 벨트, n개의 선물 -> 공장
# 선물을 주어진 순서대로 n/m개씩 잘라 1번 벨트부터 m번 벨트까지 올려줌.

num_100 = list(map(int, input().split()))
n = num_100[1]
m = num_100[2]

# 벨트 고장 여부 체크
belt_correct_check = [False for i in range(m)]

# n개의 선물 / m개의 벨트
things_per_line = n // m

# belt_info = [[[] for i in range(things_per_line)] for j in range(m)]
belt_info = [[] for j in range(m)]

belt_prev_info = []
for i in range(n):
    id_and_w = [num_100[3 + i], num_100[3 + n + i]]
    belt_prev_info.append(id_and_w)

for i in range(m):
    for j in range(things_per_line):
        data = belt_prev_info.pop(0)
        # belt_info[i][j].append(data)
        belt_info[i].append(data)
        # belt_info[i].append(belt_prev_info[0])
        # belt_prev_info.pop(0)

### Belf Info 딱 저장되어 있음.
        
# ## 2. 물건 하차
# 200 w_max 형태
# ## 하차된 상자 무게의 총 합을 출력해야 함.
# ID랑 무게 형태로 저장되어 있음.
def num_200(belt_info, w_max, belt_correct_check):
    hacha_box_weight = 0
    for i in range(len(belt_info)):
        if belt_correct_check[i] == True:
            pass
        else:
            if belt_info[i] == []:
                pass
            else: 
                if belt_info[i][0][1] <= w_max:
                    hacha_box_weight += belt_info[i][0][1]
                    belt_info[i].pop(0)
                else:
                    belt_info[i].append(belt_info[i][0])
                    belt_info[i].pop(0)
    return belt_info, hacha_box_weight

# 3. 물건 제거
# 300 r_id 형태
# 이 명령에서는 그러한 상자가 있는 경우 r_id값을, 없다면 -1을 출력
# 해당 고유 번호에 해당하는 상자가 놓여있는 벨트가 있다면, 
# 해당 벨트에서 상자를 제거하고 이에 따라 뒤에 있던 상자들은 앞으로 한 칸씩 내려오게 됨.
# ID랑 무게 형태

def num_300(belt_info, r_id, belt_correct_check):
    for i in range(len(belt_info)):
        if belt_correct_check[i] == True:
            pass
        else:
            for j in range(len(belt_info[i])):
                if belt_info[i][j][0] == r_id:
                    belt_info[i].remove(belt_info[i][j])
                    return r_id, belt_info, belt_correct_check
    return -1, belt_info, belt_correct_check

# 4. 물건 확인
# 400 f_id
# 그러한 상자가 있는 경우 f_id값을, 없다면 -1을 출력
# 해당 고유 번호에 해당하는 상자가 놓여있는 벨트가 있다면 해당 벨트의 번호를 출력하고, 없다면 -1을 출력

def num_400(belt_info, f_id, belt_correct_check):
    for i in range(len(belt_info)):
        if belt_correct_check[i] == True:
            pass
        else:
            for j in range(len(belt_info[i])):
                if belt_info[i][j][0] == f_id:
                    # 단, 상자가 있는 경우, 해당 상자 위에 있는 모든 상자를 전부 앞으로 가져옴.
                    # 가져올 시 순서는 그대로 유지가 되어야 함에 유의
                    added_info = []
                    for k in range(len(belt_info[i]), j-1, -1):
                        added_info.append(belt_info[i][-1])
                        belt_info[i].pop()
                    belt_info[i] = added_info + belt_info[i]
                    return i + 1, belt_info, belt_correct_check
    return -1, belt_info, belt_correct_check

# 5. 벨트 고장
# 500 b_num
# 이 명령을 수행하기 전 만약 b_num 벨트가 이미 망가져 있었다면 -1
# 그렇지 않았다면 정상적으로 고장을 처리했다는 뜻으로 b_num

# b_num번째 벨트에 고장이 발생하면 해당 벨트는 다시는 사용할 수 없게 됨.
# b_num 벨트의 바로 오른쪽 벨트부터 순서대로 보며 
# 아직 고장이 나지 않은 최초의 벨트 위로 
# b_num 벨트에 놓여 있던 상자들을 아래에서부터 순서대로 하나씩 옮겨줌.

# 최소 하나 이상이 정상 상태
# 모든 벨트가 망가지는 경우는 없음.

def num_500(belt_info, b_num, belt_correct_check):
    b_num -= 1
    if belt_correct_check[b_num] == True:
        return -1, belt_info, belt_correct_check
    else:
        belt_correct_check[b_num] = True
        for i in range(b_num, b_num + len(belt_info)):
            if i >= len(belt_info):
                i = i % len(belt_info)
            if belt_correct_check[i] == False:
                for j in range(len(belt_info[b_num])):
                    belt_info[i].append(belt_info[b_num][j])
                belt_info[b_num] = []
                return b_num + 1, belt_info, belt_correct_check

for i in range(q-1):
    input_data = list(map(int, input().split()))

    if input_data[0] == 200:
        belt_info, hacha_box_weight = num_200(belt_info, input_data[1], belt_correct_check)
        print(hacha_box_weight)

    elif input_data[0] == 300:
        answer, belt_info, belt_correct_check = num_300(belt_info, input_data[1], belt_correct_check)
        print(answer)
    
    elif input_data[0] == 400:
        answer, belt_info, belt_correct_check = num_400(belt_info, input_data[1], belt_correct_check)
        print(answer)

    elif input_data[0] == 500:
        answer, belt_info, belt_correct_check = num_500(belt_info, input_data[1], belt_correct_check)
        print(answer)