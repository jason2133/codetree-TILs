# 산타의 선물 공장 2
# 각 벨트의 정보와 선물의 정보를 조회할 수 있는 기능들을 추가 -> 새로운 공장을 만듦.

# 1. 공장 설립
# n개의 벨트, m개의 물건
# m개의 선물 위치 -> 공백을 사이에 두고 주어짐.
# 선물의 번호는 오름차순으로 벨트에 쌓임.

# 2. 물건 모두 옮기기
# m_src번째 밸트에 있는 선물 -> 모두 m_dst번째 벨트의 선물들로 옮김.
# 옮겨진 선물들은 m_dst 벨트 앞에 위치함.
# 만약 m_src번째 벨트에 선물이 존재하지 않다면 아무것도 옮기지 않아도 됨.
# 옮긴 뒤에 m_dst번째 벨트에 있는 선물들의 개수를 출력함.

# 3. 앞 물건만 교체하기
# m_src번째 벨트에 있는 선물 중 가장 앞에 있는 선물을 m_dst번째 벨트의 선물들 중 가장 앞에 있는 선물과 교체함.
# 둘 중 하나의 벨트에 선물이 아예 존재하지 않다면 교체하지 않고, 해당 벨트로 선물을 옮기기만 하면 됨.
# 옮긴 뒤에 m_dst번째 벨트에 있는 선물들의 개수를 출력함.

# 4. 물건 나누기
# m_src번째 벨트에 있는 선물들의 개수 -> n
# 가장 앞에서 floor(n / 2) 번째까지 있는 선물들을 m_dst 번째 벨트에 있는 앞으로 옮김.
# m_src번째 벨트에 선물이 1개인 경우에는 선물을 옮기지 않음.
# 옮긴 뒤에 m_dst번째 벨트에 있는 선물들의 개수를 출력함.

# 5. 선물 정보 얻기
# 선물 번호 p_num
# -> 해당 선물의 앞 선물의 번호 a와 뒤 선물의 번호 b라고 할 때 -> a + 2 * b를 출력함.
# 만약 앞 선물이 없는 경우 a = -1, 뒤 선물이 없는 경우 b = -1을 넣어줌.

# 6. 벨트 정보 얻기
# 벨트 번호 b_num
# -> 해당 벨트의 맨 앞에 있는 선물의 번호 a, 맨 뒤에 있는 선물의 번호를 b, 해당 벨트에 있는 선물의 개수를 c라고 할 때 -> a + 2 * b + 3 * c 출력
# 선물이 없는 벨트의 경우, a와 b 모두 -1이 됨.

############################################################################

from collections import deque

# 명령의 수 q
q = int(input())

# 공장 설립
num_100 = tuple(map(int, input().split()))

# 100 4 6 1 2 2 2 1 4
# 100 n m B_NUM1 B_NUM2 ... B_NUMm

# n개의 벨트, m개의 선물
n = num_100[1]
m = num_100[2]

# 1. 공장 설립
# n개의 벨트, m개의 물건
# m개의 선물 위치 -> 공백을 사이에 두고 주어짐.
# 선물의 번호는 오름차순으로 벨트에 쌓임.
# belt_element = deque([])
belt_info = [deque([]) for i in range(n)]

for i in range(m):
    present_info = num_100[i + 3]
    belt_info[present_info - 1].append(i + 1)

# for i in belt_info:
#     print(i)


# 2. 물건 모두 옮기기
# 200 m_src m_dst 
# 진행 이후 m_dst의 선물의 총 수를 출력함.

# m_src번째 밸트에 있는 선물 -> 모두 m_dst번째 벨트의 선물들로 옮김.
# 옮겨진 선물들은 m_dst 벨트 앞에 위치함.
# 만약 m_src번째 벨트에 선물이 존재하지 않다면 아무것도 옮기지 않아도 됨.
# 옮긴 뒤에 m_dst번째 벨트에 있는 선물들의 개수를 출력함.

# 200 2 4
def num_200(m_src, m_dst, belt_info):
    # move_before_belt = belt_info[m_src - 1]
    # move_after_belt = belt_info[m_dst - 1]

    for i in range(len(belt_info[m_src - 1])):
        # move_data = belt_info[m_src - 1].pop(-1)
        move_data = belt_info[m_src - 1].pop()
        belt_info[m_dst - 1].insert(0, move_data)
    return len(belt_info[m_dst - 1]), belt_info

# print(num_200(2, 4, belt_info))

# answer, belt_info = num_200(2, 4, belt_info)
# print(answer, belt_info)

# 3. 앞 물건만 교체하기
# 300 m_src m_dst
# 진행 이후 m_dst의 선물의 총 수를 출력함.

# m_src번째 벨트에 있는 선물 중 가장 앞에 있는 선물을 m_dst번째 벨트의 선물들 중 가장 앞에 있는 선물과 교체함.
# 둘 중 하나의 벨트에 선물이 아예 존재하지 않다면 교체하지 않고, 해당 벨트로 선물을 옮기기만 하면 됨.
# 옮긴 뒤에 m_dst번째 벨트에 있는 선물들의 개수를 출력함.

# 300 2 4
def num_300(m_src, m_dst, belt_info):
    # move_before_belt = belt_info[m_src - 1]
    # move_after_belt = belt_info[m_dst - 1]

    # 둘 다 0개일 경우
    if belt_info[m_src - 1] == deque([]) and belt_info[m_dst - 1] == deque([]):
        return 0, belt_info
    # before가 아예 없을 경우
    elif belt_info[m_src - 1] == deque([]) and len(belt_info[m_dst -1]) >= 1:
        # data = belt_info[m_dst - 1].pop(0)
        data = belt_info[m_dst - 1].popleft()
        belt_info[m_src - 1].append(data)
        return len(belt_info[m_dst - 1]), belt_info

    # after가 아예 없을 경우
    elif len(belt_info[m_src - 1]) >= 1 and belt_info[m_dst - 1] == deque([]):
        # data = belt_info[m_src - 1].pop(0)
        data = belt_info[m_src - 1].popleft()
        belt_info[m_dst - 1].append(data)
        return len(belt_info[m_dst - 1]), belt_info

    # 둘 다 내용물이 있을 경우
    # elif len(belt_info[m_src - 1]) >= 1 and len(belt_info[m_dst -1]) >= 1:
    else:
        belt_info[m_src - 1][0], belt_info[m_dst - 1][0] = belt_info[m_dst - 1][0], belt_info[m_src - 1][0]
        return len(belt_info[m_dst - 1]), belt_info

# answer, belt_info = num_300(2, 4, belt_info)
# print(answer, belt_info)

# 4. 물건 나누기
# 400 m_src m_dst
# m_dst의 선물의 총 수를 출력
# 최대 100번까지 주어지는 명령임

# m_src번째 벨트에 있는 선물들의 개수 -> n
# 가장 앞에서 floor(n / 2) 번째까지 있는 선물들을 m_dst 번째 벨트에 있는 앞으로 옮김.
# m_src번째 벨트에 선물이 1개인 경우에는 선물을 옮기지 않음.
# 옮긴 뒤에 m_dst번째 벨트에 있는 선물들의 개수를 출력함.

# 400 4 2
def num_400(m_src, m_dst, belt_info):
    # 만약 m_src 벨트에 선물이 1개인 경우에는 선물을 옮기지 않음.
    if belt_info[m_src - 1] == deque([]) or len(belt_info[m_src - 1]) == 1:
        if belt_info[m_dst - 1] == deque([]):
            return 0, belt_info
        else:
            return len(belt_info[m_dst - 1]), belt_info
    
    # m_src번째 벨트에 있는 선물들의 개수를 n
    num = len(belt_info[m_src - 1])
    # move_list = []
    move_list = deque([])
    for i in range(num // 2):
        # data = belt_info[m_src - 1].pop(0)
        data = belt_info[m_src - 1].popleft()
        move_list.append(data)
    # move_list = move_list[::-1]
    move_list.reverse()
    belt_info[m_dst - 1] = move_list + belt_info[m_dst - 1]
    return len(belt_info[m_dst - 1]), belt_info

# answer, belt_info = num_400(4, 2, belt_info)
# print(answer, belt_info)

# 5. 선물 정보 얻기
# 500 p_num
#  앞 선물의 번호 a과 뒤 선물의 번호 b라 할 때 a + 2 * b를 출력
# 없는 경우 각각 -1을 대입
def num_500(p_num, belt_info):
    for i in range(len(belt_info)):
        if p_num in belt_info[i]:
            num_index = belt_info[i].index(p_num)
            if num_index == 0:
                a = -1
            else:
                a = belt_info[i][num_index - 1]

            if num_index == (len(belt_info[i]) - 1):
                b = -1
            else:
                b = belt_info[i][num_index + 1]
            
            return (a + 2 * b), belt_info

# # 500 6
# answer, belt_info = num_500(6, belt_info)
# print(answer, belt_info)

# # 500 5
# answer, belt_info = num_500(5, belt_info)
# print(answer, belt_info)

# 6. 벨트 정보 얻기
# 600 b_num

# 벨트 번호 b_num
# -> 해당 벨트의 맨 앞에 있는 선물의 번호 a, 맨 뒤에 있는 선물의 번호를 b, 해당 벨트에 있는 선물의 개수를 c라고 할 때 
# -> a + 2 * b + 3 * c 출력
# 선물이 없는 벨트의 경우, a와 b 모두 -1이 됨.

def num_600(b_num, belt_info):
    belt_go = belt_info[b_num - 1]
    if belt_go == deque([]):
        a = -1
        b = -1
        c = 0
    else:
        a = belt_go[0]
        b = belt_go[-1]
        c = len(belt_go)
    return (a + 2 * b + 3 * c), belt_info

# # 600 1
# answer, belt_info = num_600(1, belt_info)
# print(answer, belt_info)

# # 600 3
# answer, belt_info = num_600(3, belt_info)
# print(answer, belt_info)

###################################################
## 200
# answer, belt_info = num_200(2, 4, belt_info)
# print(answer, belt_info)

## 300
# answer, belt_info = num_300(2, 4, belt_info)
# print(answer, belt_info)

## 400
# answer, belt_info = num_400(4, 2, belt_info)
# print(answer, belt_info)

## 500
# answer, belt_info = num_500(6, belt_info)
# print(answer, belt_info)

## 600
# answer, belt_info = num_600(3, belt_info)
# print(answer, belt_info)

for i in range(q - 1):
    input_data = tuple(map(int, input().split()))

    if input_data[0] == 200:
        answer, belt_info = num_200(input_data[1], input_data[2], belt_info)
        print(answer)
    
    elif input_data[0] == 300:
        answer, belt_info = num_300(input_data[1], input_data[2], belt_info)
        print(answer)
    
    elif input_data[0] == 400:
        answer, belt_info = num_400(input_data[1], input_data[2], belt_info)
        print(answer)

    elif input_data[0] == 500:
        answer, belt_info = num_500(input_data[1], belt_info)
        print(answer)
    
    elif input_data[0] == 600:
        answer, belt_info = num_600(input_data[1], belt_info)
        print(answer)