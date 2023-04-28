## 다른 파일에서 board의 크기 n 과 블록 값들의 리스트인 board를 가져온다.
from <FILE> import n, board

isPrint = True

# board 사용 예시
if isPrint:
    for i in range(n):
        for j in range(n):
            print(board[i][j], end=' ')
    

# board의 현재 상태를 score로 평가하는 함수
## 현재 빈 블록의 수로 state 평가
def getScore(board):
    # 빈 블록의 수 세기
    score = sum(row.count(0) for row in board)

    return score
