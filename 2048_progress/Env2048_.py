import random
import gym
from gym import logger, spaces
from gym.envs.classic_control import utils
from gym.error import DependencyNotInstalled
from typing import Optional
import numpy as np

BOARD_SIZE = 4

class Game2048(gym.Env[np.ndarray,int]):
    def __init__(self):
        self.grid = np.array([[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)])
        
        low = np.array([
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]],dtype=np.int16
        )
        high = np.array([
            [65536,65536,65536,65536],
            [65536,65536,65536,65536],
            [65536,65536,65536,65536],
            [65536,65536,65536,65536]],dtype=np.int16
        )
        
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=low,high = high,dtype=np.int16)
        
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()
        

    def reset(self,seed: Optional[int] = None,options:Optional[dict] = None,):
        super().reset(seed=seed)
        self.grid = np.array([[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)])
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()
        
        return self.grid
    
    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if self.grid[i][j] == 0]
        if not empty_cells:
            return False
        i, j = random.choice(empty_cells)
        if random.random() < 0.9:
            self.grid[i][j] = 2
        else:
            self.grid[i][j] = 4

        return True
    
    
    # 요구사항 
    # 1. np.array
    # 2. step함수 input 숫자로 받을 수 있게
    # 3. 각 type별 hint를 적으면 좋을 것 같아요
    # 4. move함수 고치기
    # ##
    # get grid, score, gameover
    def get_game_state(self):
        state = self.getGrid()
        score = self.getScore()
        game_over = self.isGameover()
        
        return state, score, game_over
    
    # grid를 반환
    def getGrid(self):
        return self.grid
    
    # score를 반환
    def getScore(self):
        return self.score
    
    # gameover 여부를 반환
    def isGameover(self):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.grid[i][j] == 0:
                    return False
                if j != BOARD_SIZE - 1 and self.grid[i][j] == self.grid[i][j+1]:
                    return False
                if i != BOARD_SIZE - 1 and self.grid[i][j] == self.grid[i+1][j]:
                    return False
        return True
    
    def OneHotEncoding(self):
        one_hot = np.zeros((BOARD_SIZE,BOARD_SIZE,16))
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.grid[i][j] != 0:
                    index_to_exp = int(np.log2(self.grid[i][j]))
                    if index_to_exp <= 15:
                        one_hot[i][j][index_to_exp] = 1
                    else:
                        one_hot[i][j][15] = 1
                        print("수치 초과 에러")
        return one_hot
    
    def move_left(self):
        isMove = False
        for i in range(BOARD_SIZE):
            idx = 0
            for j in range(BOARD_SIZE):
                if self.grid[i][j] > 0:
                    if(j != idx):
                        self.grid[i][j], self.grid[i][idx] = self.grid[i][idx], self.grid[i][j]
                        isMove = True
                        # debug: 현재 타일 출력
                        # print(self.grid)
                        
                    idx += 1

        # debug
        # print("move_left : ",isMove)          
        return isMove
    
    def move_right(self):
        isMove = False
        for i in range(BOARD_SIZE):
            idx = BOARD_SIZE-1
            for j in range(BOARD_SIZE-1, -1, -1):
                if self.grid[i][j] > 0:
                    if(j != idx):
                        self.grid[i][j], self.grid[i][idx] = self.grid[i][idx], self.grid[i][j]
                        isMove = True
                        # debug: 현재 타일 출력
                        # print(self.grid)
                    idx -= 1
        
        # debug
        # print("move_right : ",isMove)            
        return isMove
    
    def move_up(self):
        isMove = False
        for j in range(BOARD_SIZE):
            idx = 0
            for i in range(BOARD_SIZE):
                if self.grid[i][j] > 0:
                    if(i != idx):
                        self.grid[i][j], self.grid[idx][j] = self.grid[idx][j], self.grid[i][j]
                        isMove = True
                        # debug: 현재 타일 출력
                        # print(self.grid)
                    idx += 1
        
        # debug
        # print("move_up : ",isMove)            
        return isMove
    
    def move_down(self):
        isMove = False
        for j in range(BOARD_SIZE):
            idx = BOARD_SIZE-1
            for i in range(BOARD_SIZE-1, -1, -1):
                if self.grid[i][j] > 0:
                    if(i != idx):
                        self.grid[i][j], self.grid[idx][j] = self.grid[idx][j], self.grid[i][j]
                        isMove = True
                        # debug: 현재 타일 출력
                        # print(self.grid)
                    idx -= 1
        
        # debug
        # print("move_down : ",isMove)            
        return isMove

    def merge_left(self):
        isMove = False
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE - 1):
                if self.grid[i][j] == self.grid[i][j+1] and self.grid[i][j] != 0:
                    self.grid[i][j] *= 2
                    self.grid[i][j+1] = 0
                    self.score += self.grid[i][j]
                    isMove = True
                    # debug: 현재 타일 출력
                    # print(self.grid)
        
        # debug
        # print("merge_left : ",isMove)
        return isMove
    
    def merge_right(self):
        isMove = False
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE - 1, 0, -1):
                if self.grid[i][j] == self.grid[i][j-1] and self.grid[i][j] != 0:
                    self.grid[i][j] *= 2
                    self.grid[i][j-1] = 0
                    self.score += self.grid[i][j]
                    isMove = True
                    # debug: 현재 타일 출력
                    # print(self.grid)
        
        # debug: 함수 실행 여부
        # print("merge_right : ",isMove)
        return isMove
    
    def merge_up(self):
        isMove = False
        for j in range(BOARD_SIZE):
            for i in range(BOARD_SIZE - 1):
                if self.grid[i][j] == self.grid[i+1][j] and self.grid[i][j] != 0:
                    self.grid[i][j] *= 2
                    self.grid[i+1][j] = 0
                    self.score += self.grid[i][j]
                    isMove = True
                    # debug: 현재 타일 출력
                    # print(self.grid)
        
        # debug
        # print("merge_up : ",isMove)
        return isMove
    
    def merge_down(self):
        isMove = False
        for j in range(BOARD_SIZE):
            for i in range(BOARD_SIZE - 1, 0, -1):
                if self.grid[i][j] == self.grid[i-1][j] and self.grid[i][j] != 0:
                    self.grid[i][j] *= 2
                    self.grid[i-1][j] = 0
                    self.score += self.grid[i][j]
                    isMove = True
                    # debug: 현재 타일 출력
                    # print(self.grid)
        
        # debug
        # print("merge_down : ",isMove)
        return isMove

    def left(self):
        bool1 = self.move_left()
        bool2 = self.merge_left()
        bool3 = self.move_left()

        return bool1 or bool2 or bool3
            
    def right(self):
        bool1 = self.move_right()
        bool2 = self.merge_right()
        bool3 = self.move_right()

        return bool1 or bool2 or bool3
        
    def up(self):
        bool1 = self.move_up()
        bool2 = self.merge_up()
        bool3 = self.move_up()

        return bool1 or bool2 or bool3

    def down(self):
        bool1 = self.move_down()
        bool2 = self.merge_down()
        bool3 = self.move_down()

        return bool1 or bool2 or bool3
    
    def print_grid(self):
        print('+------' * BOARD_SIZE + '+')
        for i in range(BOARD_SIZE):
            print('|', end='')
            for j in range(BOARD_SIZE):
                if self.grid[i][j] == 0:
                    print('{:^6}'.format(''), end='|')
                else:
                    print('{:^6}'.format(str(self.grid[i][j])), end='|')
            print()
            print('+------' * BOARD_SIZE + '+')
    
    #L : 0, R : 1, U : 2, D : 3
    def step(self,action):
        lastscore = self.score

        if action == 0:
            isMove = self.left()
        
        elif action == 1:
            isMove = self.right()
        
        elif action == 2:
            isMove = self.up()
        
        elif action == 3:
            isMove = self.down()

        if isMove:
            Flag = self.add_new_tile()

        # dqn 기준 Flag = True 일 시에 reward = -5, isMove = False일 시 reward = -1  
            #Terminal
            if not Flag:
                return (self.OneHotEncoding(),-5,False)
            
            else:
                return (self.OneHotEncoding(),self.score-lastscore,True)
            
        return (self.OneHotEncoding(),-1,True)
    
