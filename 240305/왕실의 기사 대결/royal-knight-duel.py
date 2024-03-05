# Deque인 큐를 이용하여 연쇄적으로 다른 기사들도 충돌하는지를 확인함.
from collections import deque

# 전역 변수 정의
# N : 기사의 수
MAX_N = 31

# L : 체스판의 크기
MAX_L = 41

# 상 우 하 좌
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

####### 체스판이므로 MAX_L 처리함.
# 체스판 크기만큼 L x L 이렇게 해서 info로 ㄱㄱ
info = [[0 for i in range(MAX_L)] for j in range(MAX_L)]

####### 여기는 싹 다 MAX_N 처리함.
# 기사의 수만큼 bef_k -> 기사의 체력을 지칭함.
bef_k = [0 for i in range(MAX_N)]

# 각 기사의 초기 위치 (r, c)
r = [0 for i in range(MAX_N)]
c = [0 for i in range(MAX_N)]

# 각 기사는 (r, c)를 좌측 상단으로 하며, h x w 크기의 직사각형 형태를 띄고 있음.
h = [0 for i in range(MAX_N)]
w = [0 for i in range(MAX_N)]

# 각 기사의 체력 : k
k = [0 for i in range(MAX_N)]

# 기사가 이동하는 위치를 지칭 (nr, nc)
nr = [0 for i in range(MAX_N)]
nc = [0 for i in range(MAX_N)]

# 기사가 받은 데미지
dmg = [0 for i in range(MAX_N)]

# 기사 이동 여부 - 초기 설정은 다 False
is_moved = [False for i in range(MAX_N)]

####### 일단 저장하는 변수

#### 원본 체스판 데이터
# 1. 체스판
# 2. 기사의 체력 변동 bef_k

#### 5개 형식으로 주어지는 기사에 대한 정보
# 3. 기사의 초기 위치 - (r, c)
# 4. 기사의 직사각형 - (h, w)
# 5. 기사의 체력 k

#### 상호작용하면서 기사 이동하면서 변동하는 정보
# 6. 기시가 이동하는 위치 (nr, nc)
# 7. 기사가 받은 데미지 dmg
# 8. 기사 이동 여부 is_moved

# 움직임 시도
# 큐를 이용하여, 하나의 기사가 이동하였을 때 다른 모든 기사가 상호작용하는지 안하는지 이걸 동시에 체크함.
def try_movement(idx, dir):
    q = deque()

    # 처음 is_pos = True
    # ???
    # is_pos = True
    # ???

    # 초기화 작업
    for i in range(1, n + 1):
        # 데미지는 일단 처음엔 다 0으로 지정
        dmg[i] = 0

        # 이동 여부 : False로 지정
        is_moved[i] = False

        # 이동 위치를 그 기사가 있는 위치로 일단 싹 다 초기화
        nr[i] = r[i]
        nc[i] = c[i]

    # 일단 idx 번호부터 이동해야 하므로, 이걸 Queue에 넣음.
    q.append(idx)

    # 그리고 이 idx 번호는 이동이 True라고 가정함.
    is_moved[idx] = True

    # Queue를 활용해서, 해당 기사와 충돌하는 다른 기사들까지의 이동 가능성을 연쇄적으로 확인
    while q:
        x = q.popleft()

        # idx 번호의 요소에 대하여, dx[dir], dy[dir] 방향으로 이동시킴.
        nr[x] += dx[dir]
        nc[x] += dy[dir]

        # 위치 벗어나느지 체크
        if nr[x] < 1 or nc[x] < 1 or (nr[x] + h[x] - 1) > l or (nc[x] + w[x] - 1) > l:
            return False
        
        # 대상 조각이 다른 조각이나 장애물과 충돌하는지 검사함
        # 0 : 빈칸, 1 : 함정, 2 : 벽
        for i in range(nr[x], nr[x] + h[x]):
            for j in range(nc[x], nc[x] + w[x]):
                # 1 : 함정
                # 직사각형 범위 내 함정 개수만큼 데미지 추가
                if info[i][j] == 1:
                    dmg[x] += 1

                # 2 : 벽
                if info[i][j] == 2:
                    return False
        
        # 다른 조각과 충돌하는 경우, 해당 조각도 같이 이동함.
        for i in range(1, n + 1):
            if is_moved[i] or k[i] <= 0:
                continue

            # 범위 밖에 있으면 continue
            if r[i] > (nr[x] + h[x] - 1) or nr[x] > (r[i] + h[i] - 1):
                continue

            if c[i] > (nc[x] + w[x] - 1) or nc[x] > (c[i] + w[i] - 1):
                continue

            is_moved[i] = True
            q.append(i)
    
    dmg[idx] = 0
    return True

# 특정 조각을 지정된 방향으로 이동시키는 함수
def move_piece(idx, move_dir):
    if k[idx] <= 0:
        return
    
    if try_movement(idx, move_dir):
        for i in range(1, n + 1):
            r[i] = nr[i]
            c[i] = nc[i]
            k[i] -= dmg[i]

l, n, q = map(int, input().split())
for i in range(1, l + 1):
    info[i][1:] = map(int, input().split())

for i in range(1, n + 1):
    r[i], c[i], h[i], w[i], k[i] = map(int, input().split())
    bef_k[i] = k[i]

for i in range(q):
    idx, d = map(int, input().split())
    move_piece(idx, d)

ans = sum([bef_k[i] - k[i] for i in range(1, n + 1) if k[i] > 0])
print(ans)