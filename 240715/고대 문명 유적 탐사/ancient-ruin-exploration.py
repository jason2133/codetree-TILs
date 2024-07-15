import sys
from collections import deque

K,M = map(int,input().split())
mapss= [ list(map(int,input().split())) for _ in range(5)]
tn_list = map(int,input().split())
tn_list = deque(tn_list)

def rotate(x,y,level,tmaps):
    x-=1
    y-=1
    for lev in range(level):
        temp_map = [[tmaps[i][j] for j in range(5)] for i in range(5)]
        for i in range(3):
            for j in range(3):
                temp_map[j+x][-i+y+3-1] = tmaps[i+x][j+y]
        #print('level:',lev)

        tmaps=[[temp_map[i][j] for j in range(5)] for i in range(5)]

        #for k in tmaps:
        #    print(*k)
        #print()

    return tmaps

dx=[-1,0,1,0]
dy=[0,1,0,-1]

def in_range(x,y):

    return 0<=x<5 and 0<=y<5

def cal_item(mapss):

    visited = [ [0 for _ in range(5)] for _ in range(5)]
    mcount = 0
    for i in range(5):
        for j in range(5):
            queue = deque()
            count = 1
            visited[i][j] = 1
            queue.append((i,j))
            while queue:
                x,y = queue.popleft()
                for num in range(4):
                    nx,ny = x+dx[num],y+dy[num]
                    if in_range(nx,ny) and visited[nx][ny] == 0:
                        n_item = mapss[nx][ny]
                        if mapss[i][j] == n_item:
                            queue.append((nx,ny))
                            visited[nx][ny] = 1
                            count +=1
            if count >= 3 :
                mcount += count

    #print('비지티드',mcount)
    #for k in visited:
    #    print(*k)
    #print()


    return mcount


def insert_item(mapss,in_list):

    visited = [ [0 for _ in range(5)] for _ in range(5)]
    mcount = 0
    real = []
    for i in range(5):
        for j in range(5):
            queue = deque()
            tt = [(i,j)]
            count = 1
            visited[i][j] = 1
            queue.append((i,j))
            while queue:
                x,y = queue.popleft()
                for num in range(4):
                    nx,ny = x+dx[num],y+dy[num]
                    if in_range(nx,ny) and visited[nx][ny] == 0:
                        n_item = mapss[nx][ny]
                        if mapss[i][j] == n_item:
                            queue.append((nx,ny))
                            visited[nx][ny] = 1
                            count +=1
                            tt.append((nx,ny))
            if count >= 3 :
                mcount += count
                real.append(tt)

    if len(real) == 0 :
        return [[0 for _ in range(5)] for _ in range(5)],False
    oh_real = []
    for ttmap in real:
        for tx,ty in ttmap:
            oh_real.append((tx,ty))
    oh_real.sort(key=lambda x: (x[1], -x[0]))

    for zx,zy in oh_real:
        if len(in_list) == 0 :
            return [],False
        tti = in_list.popleft()
        mapss[zx][zy] = tti



    return mapss,True


in_list = tn_list.copy()
for turn in range(K):
    turn_answer = 0
    mx,my=-1,-1
    mitem=-1
    mlevel=-1
    for tx in range(1,4):
        for ty in range(1,4):
            for level in range(1,4):
                #print(tx,ty,level,'체크')
                tmaps = [ [mapss[i][j] for j in range(5)] for i in range(5)]
                test_maps = rotate(tx,ty,level,tmaps)
                items = cal_item(test_maps)
                if (items,-level,-ty,-tx) > (mitem,-mlevel,-my,-mx) :
                    mitem = items
                    mlevel = level
                    mx,my = tx,ty

    tmaps = [ [mapss[i][j] for j in range(5)] for i in range(5)]
    po = True
    turn_answer += mitem
    test_maps = rotate(mx,my,mlevel,tmaps)
    mapss,possi = insert_item(test_maps,in_list)
    if possi:
        while True :
            after_item = cal_item(mapss)
            if after_item >= 3 :
                #print(after_item)
                turn_answer += after_item
                mapss,possi = insert_item(mapss,in_list)
                if possi == False:
                    po = False
                    break
            else :
                break
        if po :
            print(turn_answer,end= ' ')
    else :
        break