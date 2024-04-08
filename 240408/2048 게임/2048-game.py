board = [[0, 1, 0], [1, 0, 1], [0, 1, 0], [0, 0, 1], [0, 1, 0]]

for i in board:
    print(i)

print('-'*30)

# n-1 m 파이 와 변 피
for i in range(len(board)-1):
    for j in range(len(board[0])):
        p = i
        while 0 <= p and board[p][j] == 1 and board[p+1][j] == 0:
            board[p][j], board[p+1][j] = board[p+1][j], board[p][j]
            p -= 1
for i in board:
    print(i)