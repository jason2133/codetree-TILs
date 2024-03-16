# 힙을 이용해서 계산 복잡도 줄이기
import heapq
import sys
def input():
    return sys.stdin.readline().rstrip()

dx = [0, -1, 0, 1]
dy = [-1, 0, 1, 0]

Q = int(input())
N, M = -1, -1

# pid : [d, score]
rabbit = dict()

#움직이는 토끼 선택용 [[총 점프 횟수, 행번호+열번호, 행번호, 열번호, pid] ... ]
prior_global = []

def start_200(K, S):
    # 마지막 점수 주는 토끼 선택용
    prior_local = []

    for k in range(K):
        tjcnt, _, x, y, pid = heapq.heappop(prior_global)
        d = rabbit[pid][0]
        tmp = []

        # d가 1,000,000,000인거 고려하기
        nx, ny = x, y

        # 상
        nx = (x + d) % (2 * (N - 1))
        if nx >= N:
            nx = 2 * (N - 1) - nx
        # 최대 힙
        heapq.heappush(tmp, [-(nx + y), -nx, -y])
        
        # 하
        nx = (x - d) % (2 * (N - 1))
        if nx >= N:
            nx = 2 * (N - 1) - nx
        # 최대 힙
        heapq.heappush(tmp, [-(nx + y), -nx, -y])

        # 좌
        ny = (y + d) % (2 * (M - 1))
        if ny >= M:
            ny = 2 * (M - 1) - ny
        # 최대 힙
        heapq.heappush(tmp, [-(x + ny), -x, -ny])

        # 우
        ny = (y - d) % (2 * (M - 1))
        if ny >= M:
            ny = 2 * (M - 1) - ny
        # 최대 힙
        heapq.heappush(tmp, [-(x + ny), -x, -ny])

        _, nx, ny = tmp[0]
        nx, ny = -nx, -ny

        for key, value in rabbit.items():
            if key != pid:
                rabbit[key][1] += (nx + ny + 2)
        
        heapq.heappush(prior_global, [tjcnt + 1, nx + ny, nx, ny, pid])
        
        # 최대 힙
        heapq.heappush(prior_local, [-(nx + ny), -nx, -ny, -pid])

    _, x, y, pid = heapq.heappop(prior_local)
    x, y, pid = -x, -y, -pid
    rabbit[pid][1] += S

def changeDist_300(pid, L):
    rabbit[pid][0] *= L

def best_400():
    max_s = -1
    for key, value in rabbit.items():
        s = value[1]
        max_s = max(max_s, s)
    print(max_s)

for q in range(Q):
    cmd = list(map(int, input().split()))
    
    # 경주 시작 준비
    if cmd [0] == 100:
        N = cmd[1]
        M = cmd[2]
        P = cmd[3]
        cmd = cmd[4:]

        for i in range(0, len(cmd), 2):
            pid, d = int(cmd[i]), int(cmd[i+1])
            rabbit[pid] = [d, 0]
            heapq.heappush(prior_global, [0, 0, 0, 0, pid])
    
    # 경주 진행
    elif cmd[0] == 200:
        K, S = cmd[1], cmd[2]
        start_200(K, S)
    
    # 이동거리 변경
    elif cmd[0] == 300:
        pid, L = cmd[1], cmd[2]
        changeDist_300(pid, L)
    
    # 최고의 토끼 선정
    elif cmd[0] == 400:
        best_400()