import numpy as np
from collections import deque

def rotate(m, d):
    """:input:
       m: 회전하고자 하는 2차원 배열. 입력이 정방형 행렬이라고 가정한다.
       d: 90도씩의 회전 단위. -1: -90도, 1: 90도, 2: 180도, ...
    """
    N = len(m)
    ret = np.array([[0] * N for _ in range(N)])

    if d == 0:
        for r in range(N):
            for c in range(N):
                ret[r][c] = m[r][c]
    elif d == 1:
        for r in range(N):
            for c in range(N):
                ret[c][N-1-r] = m[r][c]
    elif d == 2:
        for r in range(N):
            for c in range(N):
                ret[N-1-r][N-1-c] = m[r][c]
    elif d == 3:
        for r in range(N):
            for c in range(N):
                ret[N-1-c][r] = m[r][c]
    
    elif d == 4:
        for r in range(N):
            for c in range(N):
                ret[r][c] = m[N-r-1][c]
    
    elif d == 5:
        for r in range(N):
            for c in range(N):
                ret[r][c] = m[r][N-1-c]
    
    elif d == 6:
        for r in range(N):
            for c in range(N):
                ret[r][c] = m[N-1-c][N-1-r]
    
    elif d == 7:
        for r in range(N):
            for c in range(N):
                ret[r][c] = m[c][r]

    return ret



"""
Clockwise rotation
0 : 0 degree rotation
1 : 90 degree rotation
2 : 180 degree rotation
3 : 270 degree rotation
4 : Horizontal reflection
5 : Vertical reflection
6 : Diagonal reflection(+)
7 : Diagonal reflection(-)
"""

route = [[(0,0),(0,1),(0,2),(0,3),(1,0),(1,1),(1,2),(1,3),(2,0),(2,1),(2,2),(2,3),(3,0),(3,1),(3,2),(3,3)],
         [(3,0),(2,0),(1,0),(0,0),(3,1),(2,1),(1,1),(0,1),(3,2),(2,2),(1,2),(0,2),(3,3),(2,3),(1,3),(0,3)],
         [(3,3),(3,2),(3,1),(3,0),(2,3),(2,2),(2,1),(2,0),(1,3),(1,2),(1,1),(1,0),(0,3),(0,2),(0,1),(0,0)],
         [(0,3),(1,3),(2,3),(3,3),(0,2),(1,2),(2,2),(3,2),(0,1),(1,1),(2,1),(3,1),(0,0),(1,0),(2,0),(3,0)],
         [(3,0),(3,1),(3,2),(3,3),(2,0),(2,1),(2,2),(2,3),(1,0),(1,1),(1,2),(1,3),(0,0),(0,1),(0,2),(0,3)],
         [(0,3),(0,2),(0,1),(0,0),(1,3),(1,2),(1,1),(1,0),(2,3),(2,2),(2,1),(2,0),(3,3),(3,2),(3,1),(3,0)],
         [(3,3),(2,3),(1,3),(0,3),(3,2),(2,2),(1,2),(0,2),(3,1),(2,1),(1,1),(0,1),(3,0),(2,0),(1,0),(0,0)],
         [(0,0),(1,0),(2,0),(3,0),(0,1),(1,1),(2,1),(3,1),(0,2),(1,2),(2,2),(3,2),(0,3),(1,3),(2,3),(3,3)]]

A_to_B = [[0,1,2,3],
          [3,2,0,1],
          [1,0,3,2],
          [2,3,1,0],
          [0,1,3,2],
          [1,0,2,3],
          [3,2,1,0],
          [2,3,0,1]
          ]

def representative(arr:np.array):
    #(move_idx) in stack
    checked = [True]*len(route)
    stack = deque()
    stack.append(0)
    for idx in range(16): #4X4 matrix
        for move_idx,move in enumerate(route):
            if(checked[move_idx]): #아직 제거되지 않은 move라면
                val_cur = arr[move[idx]]    #현재 move의 val
                val_min = arr[route[stack[-1]][idx]]
                if val_cur>val_min:
                    checked[move_idx] = False
                    continue
                elif val_cur == val_min:
                    stack.append(move_idx)
                else:
                    while(stack):
                        checked[stack.pop()] = False
                    stack.append(move_idx)
                    
        if(len(stack) == 1 or (len(stack)==2 and stack[0]==stack[1])):
            return stack[0]
        
        while(len(stack)!=1):
            stack.pop()
    
    return stack[0]

# L : 0 / R : 1 / U : 2 / D : 3
def action_convert(converted,action):
    return A_to_B[converted][action]

arr = np.array([
            [2,2,0,2],
            [0,0,0,2],
            [0,0,0,2],
            [4,0,0,2]],dtype=np.int16
        )

# perfect_done = True
# for i1 in range(3):
#     for i2 in range(3):
#         for i3 in range(3):
#             for i4 in range(3):
#                 for i5 in range(3):
#                     for i6 in range(3):
#                         for i7 in range(3):
#                             for i8 in range(3):
#                                 for i9 in range(3):
#                                     for i10 in range(3):
#                                         for i11 in range(3):
#                                             for i12 in range(3):
#                                                 for i13 in range(3):
#                                                     for i14 in range(3):
#                                                         for i15 in range(3):
#                                                             for i16 in range(3):
#                                                                 arr_0 = np.array([[i1,i2,i3,i4],[i5,i6,i7,i8],[i9,i10,i11,i12],[i13,i14,i15,i16]])
#                                                                 arr_1 = rotate(arr_0,1)
#                                                                 arr_2 = rotate(arr_0,2)
#                                                                 arr_3 = rotate(arr_0,3)
#                                                                 arr_4 = rotate(arr_0,4)
#                                                                 arr_5 = rotate(arr_0,5)
#                                                                 arr_6 = rotate(arr_0,6)
#                                                                 arr_7 = rotate(arr_0,7)

#                                                                 result = []
#                                                                 result.append(rotate(arr_0,representative(arr_0)))
#                                                                 result.append(rotate(arr_1,representative(arr_1)))
#                                                                 result.append(rotate(arr_2,representative(arr_2)))
#                                                                 result.append(rotate(arr_3,representative(arr_3)))
#                                                                 result.append(rotate(arr_4,representative(arr_4)))
#                                                                 result.append(rotate(arr_5,representative(arr_5)))
#                                                                 result.append(rotate(arr_6,representative(arr_6)))
#                                                                 result.append(rotate(arr_7,representative(arr_7)))

#                                                                 perfect_check = True

#                                                                 N = len(arr_0)
#                                                                 for r in range(N):
#                                                                     for m in range(N):
#                                                                         val = result[0][r][m]
#                                                                         for i in range(1,len(result)):
#                                                                             if(val != result[i][r][m]):
#                                                                                 perfect_check = False

#                                                                 if(perfect_check):
#                                                                     continue
#                                                                 else:
#                                                                     perfect_done = False
#                                                                     print([[i1,i2,i3,i4],[i5,i6,i7,i8],[i9,i10,i11,i12],[i13,i14,i15,i16]])
#                                                                     exit()

# if(perfect_done):
#     print("Perfect")