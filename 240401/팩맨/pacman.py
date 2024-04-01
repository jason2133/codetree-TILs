MAX_T = 25
MAX_N = 4
DIR_NUM = 8
P_DIR_NUM = 4
MAX_DECAY = 2

# 변수 선언 및 입력
n = 4
m, t = tuple(map(int, input().split()))

# 팩맨의 위치를 저장합니다.
px, py = tuple(map(int, input().split()))
px -= 1; py -= 1

# map의 상태를 뜻합니다.
# t번째 턴에 (x, y) 위치에 방향 move_dir를 바라보고 있는
# 몬스터의 수를 뜻합니다.
monster = [
	[
		[	
			[0] * DIR_NUM
			for _ in range(n)
		]
		for _ in range(n)
	]
	for _ in range(MAX_T + 1)
]

# 시체를 관리하기 위한 배열입니다.
# 좀 더 자세하게는,
# (x, y)위치에서
# 썩기 t초 전인 시체가
# 몇 개 있는지를 의미합니다.
dead = [
	[
		[0] * (MAX_DECAY + 1)
		for _ in range(n)
	]
	for _ in range(n)
]

# 문제에서 주어지는 방향 순서대로
# dx, dy 값들을 정의합니다. 
# 몬스터를 위한 방향입니다.
dxs = [-1, -1,  0,  1, 1, 1, 0, -1]
dys = [ 0, -1, -1, -1, 0, 1, 1,  1]

# 팩맨을 위한
# dx, dy를 따로 정의합니다.
# 우선순위에 맞춰
# 상좌하우 순으로 적어줍니다.
p_dxs = [-1,  0, 1, 0]
p_dys = [ 0, -1, 0, 1]

# 현재 몇 번째 턴인지를 저장합니다.
t_num = 1


# 영역 내에 있는지를 확인합니다.
def in_range(x, y):
    return 0 <= x and x < n and 0 <= y and y < n


# 나아가려고 하는 위치가 영역 내에 있으며 
# 몬스터 시체가 없고, 팩맨도 없다면
# 이동이 가능합니다.
def can_go(x, y):
	return in_range(x, y) and dead[x][y][0] == 0 and dead[x][y][1] == 0 \
	   and (x, y) != (px, py)


def get_next_pos(x, y, move_dir):
    # 현재 위치에서부터
    # 반시계방향으로 45'씩 회전해보며
    # 가능한 곳이 보이면 바로 이동합니다.
    for c_dir in range(DIR_NUM):
        n_dir = (move_dir + c_dir + DIR_NUM) % DIR_NUM
        nx, ny = x + dxs[n_dir], y + dys[n_dir]
        if can_go(nx, ny):
            return (nx, ny, n_dir)

    # 이동이 불가능하다면, 움직이지 않고 기존 상태 그대로 반환합니다.
    return (x, y, move_dir)


def move_m():
    # 각 (i, j)칸에 k 방향을 바라보고 있는 몬스터들이
    # 그 다음으로 이동해야할 위치 및 방향을 구해
    # 전부 (칸, 방향) 단위로 이동시켜 줍니다.
    # 일일이 몬스터 마다 위치를 구해 이동시키면 시간초과가 발생합니다.
    for i in range(n):
        for j in range(n):
            for k in range(DIR_NUM):
                x, y, next_dir = get_next_pos(i, j, k)
                monster[t_num][x][y][next_dir] += monster[t_num - 1][i][j][k]

				
def get_killed_num(dir1, dir2, dir3):
    x, y = px, py
    killed_num = 0

    # 방문한적이 있는지를 기록합니다.
    v_pos = []

    for move_dir in [dir1, dir2, dir3]:
        nx, ny = x + p_dxs[move_dir], y + p_dys[move_dir]
        # 움직이는 도중에 격자를 벗어나는 경우라면, 선택되면 안됩니다.
        if not in_range(nx, ny):
            return -1
		# 이미 계산한 곳에 대해서는, 중복 계산하지 않습니다.
        if (nx, ny) not in v_pos:
            killed_num += sum(monster[t_num][nx][ny])
            v_pos.append((nx, ny))
        
        x, y = nx, ny
		
    return killed_num


def do_kill(best_route):
    global px, py
    
    dir1, dir2, dir3 = best_route
	
	# 정해진 dir1, dir2, dir3 순서에 맞춰 이동하며
	# 몬스터를 잡습니다.
    for move_dir in [dir1, dir2, dir3]:
        nx, ny = px + p_dxs[move_dir], py + p_dys[move_dir]
        
        for i in range(DIR_NUM):
            dead[nx][ny][MAX_DECAY] += monster[t_num][nx][ny][i]
            monster[t_num][nx][ny][i] = 0
            
        px, py = nx, ny
    
	
def move_p():
    max_cnt = -1
    best_route = (-1, -1, -1)

    # 우선순위 순서대로 수행합니다.
    for i in range(P_DIR_NUM):
        for j in range(P_DIR_NUM):
            for k in range(P_DIR_NUM):
                m_cnt = get_killed_num(i, j, k)
                # 가장 많은 수의 몬스터를 잡을 수 있는 경우 중
				# 우선순위가 가장 높은 것을 고릅니다.
                if m_cnt > max_cnt:
                    max_cnt = m_cnt
                    best_route = (i, j, k)
    
    # 최선의 루트에 따라 
    # 실제 죽이는 것을 진행합니다.
    do_kill(best_route)


def decay_m():
	# decay를 진행합니다. 턴을 하나씩 깎아주면 됩니다.
    for i in range(n):
        for j in range(n):
            for k in range(MAX_DECAY):
                dead[i][j][k] = dead[i][j][k + 1]
            dead[i][j][MAX_DECAY] = 0
        

def add_m():
	# 몬스터가 복제됩니다.
    for i in range(n):
        for j in range(n):
            for k in range(DIR_NUM):
                monster[t_num][i][j][k] += monster[t_num - 1][i][j][k]

				
def simulate():
    # 매 초마다 기록하기 때문에 굳이 copy를 진행할 필요는 없습니다.
    
    # 각 칸에 있는 몬스터를 이동시킵니다.
    move_m()

    # 팩맨을 이동시킵니다.
    move_p()

    # 시체들이 썩어갑니다.
    decay_m()

    # 몬스터가 복제됩니다.
    add_m()

	
def count_monster():
	cnt = 0

    # 마지막 턴을 마친 이후의 몬스터 수를 셉니다.
	for i in range(n):
		for j in range(n):
			for k in range(DIR_NUM):
				cnt += monster[t][i][j][k]
				
	return cnt


for _ in range(m):
	mx, my, mdir = tuple(map(int, input().split()))
	# 첫 번째 턴의 상태를 기록합니다.
	monster[0][mx - 1][my - 1][mdir - 1] += 1
    
# t번 시뮬레이션을 진행합니다.
while t_num <= t:
	simulate()
	t_num += 1

print(count_monster())