##### Intuition
# 선물 & 벨트 관리
# -> 중요한 것
# (1) 각 벨트의 상태를 유지하는 것
# (2) 선물들 간의 상호관계를 효과적으로 나타내는 것

## 주어진 명령들을 실행할 때마다,
# 벨트와 선물들의 상태를 갱신하며,
# 필요한 정보를 빠르고 정확하게 가져올 수 있어야 함.

# -> 이를 위해,
# 각 선물은 이전 선물과 다음 선물을 가리키는 포인터를 가지며
# 각 벨트는 첫 번째와 마지막 선물을 가리키는 포인터 및 선물의 개수를 기록함.

# 명령에 따라, 선물들을 옮기거나 교체할 때는 이 포인터를 조작하여 벨트의 상태를 갱신하고,
# 선물 정보를 알아낼 때는 포인터를 통해 연결된 선물들을 조사함.


##### Algorithm
# 각 작업을 수행하기 위해 -> 입력받은 명령어의 종류에 따라 분기하여 처리함.

### BuildFactory 함수
# 공장의 초기 설정을 함.
# 벨트 별로 어떤 선물들이 있는지 입력을 받음.
# 각 벨트의 첫번째와 마지막 선물, 선물의 개수를 저장하고, head / tail 포인터를 초기화함.

### Move 함수
# 한 벨트의 모든 선물을 다른 벨트로 옮김.
# 이때, 수신 벨트에 처음 옮기는 상황과 이미 선물이 있어서 연결해야 하는 상황을 구분함.

### Change 함수
# 두 벨트의 첫번째 선물을 교환함.

# RemoveHead 함수를 통해 각 벨트의 Head 선물을 제거함.
# PushHead 함수를 통해 서로 교환하여 넣음.

### Divide 함수
# 한 벨트에서 선물의 절반을 다른 벨트로 옮김.

# RemoveHead를 사용하여 앞에서부터 차례대로 제거함.
# 다른 벨트에는 순서를 유지하기 위해 역순으로 PushHead로 추가함.

### GiftScore 함수 / BeltScore 함수 -> 각각의 선물 정보와 벨트에 대한 정보를 출력함.
# 선물 정보는 이전, 다음 선물을 포인터를 통해 조회함.
# 벨트 정보는 벨트의 head, tail 포인터와 num_gift를 이용해 계산함.

# 각 함수들은 벨트와 선물의 상태를 유지하는 데 중점을 두고 설계되었음.
# 시간복잡도는 O(Q)

##### 시간복잡도를 줄이기 위해,
# 함수 내부의 연산이 주로 포인터 조작과 기본적인 산술 계산으로 이루어짐.
## -> 각 명령의 수행 시간이 매우 빠름.

MAX_N = 100000
MAX_M = 100000

# 변수 선언
# n개의 벨트, m개의 선물
n = -1
m = -1
q = -1

######### 따로 데이터를 저장해서, 계산 복잡도를 줄이려고 하는 것이구나.

# ID에 해당하는 상자의 ntx값과 prv값을 관리함.
# 0이면 없다는 뜻임.
prv = [0] * (MAX_M + 1)
nxt = [0] * (MAX_M + 1)

# 각 벨트별로 head, tail id, 그리고 총 선물 수를 관리함.
# 0이면 없다는 뜻임.
head = [0] * MAX_N
tail = [0] * MAX_N
num_gift = [0] * MAX_N

# 공장 설립
def build_factory(elems):
    # 공장 정보를 입력받음.
    n = elems[1]
    m = elems[2]

    # 벨트 정보를 만들어줌.
    boxes = [[] for i in range(n)]

    for _id in range(1, m + 1):
        b_num = elems[_id + 2]
        b_num -= 1

        boxes[b_num].append(_id)

    # 초기 벨트의 head, tail, nxt, prv 값을 설정해줌.
    for i in range(n):
        # 비어 있는 벨트라면 패스
        if len(boxes[i]) == 0:
            continue

        # head, tail을 설정해줌.
        head[i] = boxes[i][0]
        tail[i] = boxes[i][-1]

        # 벨트 내 선물 총 수를 관리해줌.
        num_gift[i] = len(boxes[i])

        # nxt, prv를 설정해줌.
        for j in range(len(boxes[i]) - 1):
            nxt[boxes[i][j]] = boxes[i][j + 1]
            prv[boxes[i][j + 1]] = boxes[i][j]
    
# 물건을 전부 옮겨줌.
def move(elems):
    m_src = elems[1] - 1
    m_dst = elems[2] - 1

    # m_src에 물건이 없다면
    # 그대로 m_dst 내 물건 수가 답이 됨.
    if num_gift[m_src] == 0:
        print(num_gift[m_dst])
        return
    
    # m_dst에 물건이 없다면
    # 그대로 옮겨줌.
    if num_gift[m_dst] == 0:
        head[m_dst] = head[m_src]
        tail[m_dst] = tail[m_src]
    else:
        orig_head = head[m_dst]

        # m_dst의 head를 교체해줌.
        head[m_dst] = head[m_src]
        
        # m_src의 tail과 기존 m_dst의 head를 연결해줌.
        src_tail = tail[m_src]
        nxt[src_tail] = orig_head
        prv[orig_head] = src_tail
    
    # head, tail을 비워줌.
    head[m_src] = 0
    tail[m_src] = 0

    # 선물 상자 수를 갱신해줌.
    num_gift[m_dst] += num_gift[m_src]
    num_gift[m_src] = 0

    print(num_gift[m_dst])

# 해당 벨트의 head를 제거함.
def remove_head(b_num):
    # 불가능하면 패스함.
    if not num_gift[b_num]:
        return 0
    
    # 노드가 1개라면
    # head, tail 전부 삭제 후 반환함.
    if num_gift[b_num] == 1:
        _id = head[b_num]
        head[b_num] = 0
        tail[b_num] = 0
        return _id
    
    # head를 바꿔줌
    hid = head[b_num]
    next_head = nxt[hid]
    
    nxt[hid] = 0
    prv[next_head] = 0

    num_gift[b_num] -= 1
    head[b_num] = next_head

    return hid

# 해당 벨트에 head를 추가함.
def push_head(b_num, hid):
    # 불가능한 경우에는 진행하지 않음.
    if hid == 0:
        return
    
    # 비어 있었다면
    # head, tail이 동시에 추가됨.
    if not num_gift[b_num]:
        head[b_num] = hid
        tail[b_num] = hid

        num_gift[b_num] = 1
    
    # 그렇지 않다면
    # head만 교체됨.
    else:
        orig_head = head[b_num]
        nxt[hid] = orig_head
        prv[orig_head] = hid
        head[b_num] = hid
        num_gift[b_num] += 1
    
# 앞 물건을 교체해줌.
def change(elems):
    m_src = elems[1] - 1
    m_dst = elems[2] - 1

    src_head = remove_head(m_src)
    dst_head = remove_head(m_dst)

    push_head(m_dst, src_head)
    push_head(m_src, dst_head)

    print(num_gift[m_dst])

# 물건을 나눠옮김.
def divide(elems):
    m_src = elems[1] - 1
    m_dst = elems[2] - 1

    # 순서대로 src에서 박스들을 빼줌.
    cnt = num_gift[m_src]
    box_ids = []
    
    for i in range(cnt // 2):
        box_ids.append(remove_head(m_src))

    # 거꾸로 뒤집어서 하나씩 dst에 박스들을 넣어줌.
    for i in range(len(box_ids) - 1, -1, -1):
        push_head(m_dst, box_ids[i])
    
    print(num_gift[m_dst])

# 선물 점수를 얻음.
def gift_score(elems):
    p_num = elems[1]

    if prv[p_num] != 0:
        a = prv[p_num]
    else:
        a = -1

    if nxt[p_num] != 0:
        b = nxt[p_num]
    else:
        b = -1
    
    print(a + 2 * b)

# 벨트 정보를 얻음.
def belt_score(elems):
    b_num = elems[1] - 1

    if head[b_num] != 0:
        a = head[b_num]
    else:
        a = -1

    if tail[b_num] != 0:
        b = tail[b_num]
    else:
        b = -1
    
    c = num_gift[b_num]
    
    print(a + 2 * b + 3 * c)

# 입력
q = int(input())

for i in range(q):
    elems = list(map(int, input().split()))
    q_type = elems[0]

    if q_type == 100:
        build_factory(elems)
    elif q_type == 200:
        move(elems)
    elif q_type == 300:
        change(elems)
    elif q_type == 400:
        divide(elems)
    elif q_type == 500:
        gift_score(elems)
    else:
        belt_score(elems)