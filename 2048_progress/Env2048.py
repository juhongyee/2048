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
            self.score += 2
        else:
            self.grid[i][j] = 4
            self.score += 4
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
        
    def move_left(self):
        for i in range(BOARD_SIZE):
            # move tiles to the left
            for j in range(1, BOARD_SIZE):
                if self.grid[i][j] != 0:
                    k = j
                    while k > 0 and self.grid[i][k-1] == 0:
                        self.grid[i][k-1], self.grid[i][k] = self.grid[i][k], self.grid[i][k-1]
                        k -= 1
                        
            # merge adjacent tiles
            for j in range(1, BOARD_SIZE):
                k = j-1
                while k > 0 and self.grid[i][k] == 0:
                    self.grid[i][k], self.grid[i][k+1] = self.grid[i][k+1], 0
                    k -= 1
                if self.grid[i][k+1] == self.grid[i][k] and self.grid[i][k+1] != 0:
                    self.grid[i][k] *= 2
                    self.grid[i][k+1] = 0
                    self.score += self.grid[i][k]
       
        return self.grid
            

    def move_right(self):
        for i in range(BOARD_SIZE):
            # move tiles to the right
            for j in range(BOARD_SIZE-2, -1, -1):
                if self.grid[i][j] != 0:
                    k = j
                    while k < BOARD_SIZE-1 and self.grid[i][k+1] == 0:
                        self.grid[i][k+1], self.grid[i][k] = self.grid[i][k], self.grid[i][k+1]
                        k += 1
            # merge adjacent tiles
            for j in range(BOARD_SIZE-2, -1, -1):
                k = j+1
                while k < BOARD_SIZE-1 and self.grid[i][k] == 0:
                    self.grid[i][k], self.grid[i][k-1] = self.grid[i][k-1], 0
                    k += 1
                if self.grid[i][k-1] == self.grid[i][k] and self.grid[i][k-1] != 0:
                    self.grid[i][k] *= 2
                    self.grid[i][k-1] = 0
                    self.score += self.grid[i][k]
                
        return self.grid
        
    def move_up(self):
        for j in range(BOARD_SIZE):
            # move tiles up
            for i in range(1, BOARD_SIZE):
                if self.grid[i][j] != 0:
                    k = i
                    while k > 0 and self.grid[k-1][j] == 0:
                        self.grid[k-1][j], self.grid[k][j] = self.grid[k][j], self.grid[k-1][j]
                        k -= 1
            # merge adjacent tiles
            for i in range(1, BOARD_SIZE):
                k = i-1
                while k > 0 and self.grid[k][j] == 0:
                    self.grid[k][j], self.grid[k+1][j] = self.grid[k+1][j],0
                    k -= 1
                if self.grid[k+1][j] == self.grid[k][j] and self.grid[k+1][j] != 0:
                    self.grid[k][j] *= 2
                    self.grid[k+1][j] = 0
                    self.score += self.grid[k][j]
            
        return self.grid

    def move_down(self):
        for j in range(BOARD_SIZE):
            # move tiles down
            for i in range(BOARD_SIZE-2, -1, -1):
                if self.grid[i][j] != 0:
                    k = i
                    while k < BOARD_SIZE-1 and self.grid[k+1][j] == 0:
                        self.grid[k+1][j], self.grid[k][j] = self.grid[k][j], self.grid[k+1][j]
                        k += 1
                        
            # merge adjacent tiles
            for i in range(BOARD_SIZE-2, -1, -1):
                k = i+1
                while k < BOARD_SIZE-1 and self.grid[k][j] == 0:
                    self.grid[k][j], self.grid[k-1][j] = self.grid[k-1][j], 0
                    k += 1
                if self.grid[k-1][j] == self.grid[k][j] and self.grid[k-1][j] != 0:
                    self.grid[k][j] *= 2
                    self.grid[k-1][j] = 0
                    self.score += self.grid[k][j]
                
        return self.grid
    
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
        before_score = self.score
        if action == 0:
            self.move_left()
        
        elif action == 1:
            self.move_right()
        
        elif action == 2:
            self.move_up()
        
        elif action == 3:
            self.move_down()
        
        Flag = self.add_new_tile()
        
        #Terminal
        if not Flag:
            return (self.grid,self.score-before_score,True,True)
        
        else:
            return (self.grid,self.score-before_score,False,True)