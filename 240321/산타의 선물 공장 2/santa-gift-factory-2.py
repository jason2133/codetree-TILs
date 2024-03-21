MAX_N = 100000
MAX_M = 100000

# 변수 선언
n, m, q = -1, -1, -1

# id에 해당하는 상자의 nxt값과 prv값을 관리합니다.
# 0이면 없다는 뜻입니다.
prv, nxt = [0] * (MAX_M + 1), [0] * (MAX_M + 1)

# 각 벨트별로 head, tail id, 그리고 총 선물 수를 관리합니다.
# 0이면 없다는 뜻입니다.
head, tail, num_gift = [0] * MAX_N, [0] * MAX_N, [0] * MAX_N


# 공장 설립
def build_factory(elems):
    # 공장 정보를 입력받습니다.
    n, m = elems[1], elems[2]
    
    # 벨트 정보를 만들어줍니다.
    boxes = [[] for _ in range(n)]
    for _id in range(1, m + 1):
        b_num = elems[_id + 2]
        b_num -= 1
        
        boxes[b_num].append(_id)

    # 초기 벨트의 head, tail, nxt, prv값을 설정해줍니다.
    for i in range(n):
        # 비어있는 벨트라면 패스합니다.
        if len(boxes[i]) == 0:
            continue
        
        # head, tail을 설정해줍니다.
        head[i] = boxes[i][0]
        tail[i] = boxes[i][-1]

        # 벨트 내 선물 총 수를 관리해줍니다.
        num_gift[i] = len(boxes[i])

        # nxt, prv를 설정해줍니다.
        for j in range(len(boxes[i]) - 1):
            nxt[boxes[i][j]] = boxes[i][j + 1]
            prv[boxes[i][j + 1]] = boxes[i][j]


# 물건을 전부 옮겨줍니다.
def move(elems):
    m_src, m_dst = elems[1] - 1, elems[2] - 1

    # m_src에 물건이 없다면
    # 그대로 m_dst내 물건 수가 답이 됩니다.
    if num_gift[m_src] == 0:
        print(num_gift[m_dst])
        return

    # m_dst에 물건이 없다면
    # 그대로 옮겨줍니다.
    if num_gift[m_dst] == 0:
        head[m_dst] = head[m_src]
        tail[m_dst] = tail[m_src]
    else:
        orig_head = head[m_dst]
        # m_dst의 head를 교체해줍니다.
        head[m_dst] = head[m_src]
        # m_src의 tail과 기존 m_dst의 head를 연결해줍니다.
        src_tail = tail[m_src]
        nxt[src_tail] = orig_head
        prv[orig_head] = src_tail

    # head, tail을 비워줍니다.
    head[m_src] = tail[m_src] = 0

    # 선물 상자 수를 갱신해줍니다.
    num_gift[m_dst] += num_gift[m_src]
    num_gift[m_src] = 0

    print(num_gift[m_dst])


# 해당 벨트의 head를 제거합니다.
def remove_head(b_num):
    # 불가능하면 패스합니다.
    if not num_gift[b_num]:
        return 0
    
    # 노드가 1개라면
    # head, tail 전부 삭제 후
    # 반환합니다.
    if num_gift[b_num] == 1:
        _id = head[b_num]
        head[b_num] = tail[b_num] = 0
        num_gift[b_num] = 0
        return _id

    # head를 바꿔줍니다.
    hid = head[b_num]
    next_head = nxt[hid]
    nxt[hid] = prv[next_head] = 0
    num_gift[b_num] -= 1
    head[b_num] = next_head

    return hid


# 해당 밸트에 head를 추가합니다.
def push_head(b_num, hid):
    # 불가능한 경우는 진행하지 않습니다.
    if hid == 0:
        return

    # 비어있었다면
    # head, tail이 동시에 추가됩니다.
    if not num_gift[b_num]:
        head[b_num] = tail[b_num] = hid
        num_gift[b_num] = 1
    # 그렇지 않다면
    # head만 교체됩니다.
    else:
        orig_head = head[b_num]
        nxt[hid] = orig_head
        prv[orig_head] = hid
        head[b_num] = hid
        num_gift[b_num] += 1


# 앞 물건을 교체해줍니다.
def change(elems):
    m_src, m_dst = elems[1] - 1, elems[2] - 1
    
    src_head = remove_head(m_src)
    dst_head = remove_head(m_dst)
    push_head(m_dst, src_head)
    push_head(m_src, dst_head)
    
    print(num_gift[m_dst])


# 물건을 나눠옮겨줍니다.
def divide(elems):
    m_src, m_dst = elems[1] - 1, elems[2] - 1

    # 순서대로 src에서 박스들을 빼줍니다.
    cnt = num_gift[m_src]
    box_ids = []
    for _ in range(cnt // 2):
        box_ids.append(remove_head(m_src))
    
    # 거꾸로 뒤집어서 하나씩 dst에 박스들을 넣어줍니다.
    for i in range(len(box_ids) - 1, -1, -1):
        push_head(m_dst, box_ids[i])

    print(num_gift[m_dst])


# 선물 점수를 얻습니다.
def gift_score(elems):
    p_num = elems[1]

    a = prv[p_num] if prv[p_num] != 0 else -1
    b = nxt[p_num] if nxt[p_num] != 0 else -1

    print(a + 2 * b)
 

# 벨트 정보를 얻습니다.
def belt_score(elems):
    b_num = elems[1] - 1

    a = head[b_num] if head[b_num] != 0 else -1
    b = tail[b_num] if tail[b_num] != 0 else -1
    c = num_gift[b_num]

    print(a + 2 * b + 3 * c)


# 입력:
q = int(input())
for _ in range(q):
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