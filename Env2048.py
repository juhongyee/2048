import random
import copy

BOARD_SIZE = 4

class Game2048:
    def __init__(self):
        self.grid = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()

    def reset(self):
        self.grid = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
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
    
    #for dictionary
    def grid_to_tuple(self,board):
        for i in range(BOARD_SIZE):
            board[i] = tuple(board[i])
        board = tuple(board)
        
        return board
        
    def move_left(self,simulation):
        if not (simulation==1):
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
                    if self.grid[i][j] == self.grid[i][j-1] and self.grid[i][j] != 0:
                        self.grid[i][j-1] *= 2
                        self.grid[i][j] = 0
                        self.score += self.grid[i][j-1]
        else:
            grid = copy.deepcopy(self.grid)
            score = self.score
            for i in range(BOARD_SIZE):
                # move tiles to the left
                for j in range(1, BOARD_SIZE):
                    if grid[i][j] != 0:
                        k = j
                        while k > 0 and grid[i][k-1] == 0:
                            grid[i][k-1], grid[i][k] = grid[i][k], grid[i][k-1]
                            k -= 1
                            
                # merge adjacent tiles
                for j in range(1, BOARD_SIZE):
                    if grid[i][j] == grid[i][j-1] and grid[i][j] != 0:
                        grid[i][j-1] *= 2
                        grid[i][j] = 0
                        score += grid[i][j-1]
            grid = self.grid_to_tuple(grid)
            return grid
            

    def move_right(self,simulation):
        if simulation != 1:
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
                    if self.grid[i][j] == self.grid[i][j+1] and self.grid[i][j] != 0:
                        self.grid[i][j+1] *= 2
                        self.grid[i][j] = 0
                        self.score += self.grid[i][j+1]
        else:
            grid = copy.deepcopy(self.grid)
            score = self.score
            for i in range(BOARD_SIZE):
                # move tiles to the right
                for j in range(BOARD_SIZE-2, -1, -1):
                    if grid[i][j] != 0:
                        k = j
                        while k < BOARD_SIZE-1 and grid[i][k+1] == 0:
                            grid[i][k+1], grid[i][k] = grid[i][k], grid[i][k+1]
                            k += 1
                # merge adjacent tiles
                for j in range(BOARD_SIZE-2, -1, -1):
                    if grid[i][j] == grid[i][j+1] and grid[i][j] != 0:
                        grid[i][j+1] *= 2
                        grid[i][j] = 0
                        score += grid[i][j+1]
            grid = self.grid_to_tuple(grid)
            return grid
        
    def move_up(self,simulation):
        if simulation != 1:
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
                    if self.grid[i][j] == self.grid[i-1][j] and self.grid[i][j] != 0:
                        self.grid[i-1][j] *= 2
                        self.grid[i][j] = 0
                        self.score += self.grid[i-1][j]
        else:
            grid = copy.deepcopy(self.grid)
            score = self.score
            for j in range(BOARD_SIZE):
                # move tiles up
                for i in range(1, BOARD_SIZE):
                    if grid[i][j] != 0:
                        k = i
                        while k > 0 and grid[k-1][j] == 0:
                            grid[k-1][j], grid[k][j] = grid[k][j], grid[k-1][j]
                            k -= 1
                # merge adjacent tiles
                for i in range(1, BOARD_SIZE):
                    if grid[i][j] == grid[i-1][j] and grid[i][j] != 0:
                        grid[i-1][j] *= 2
                        grid[i][j] = 0
                        score += grid[i-1][j]
                        
            grid = self.grid_to_tuple(grid)
            return grid

    def move_down(self,simulation):
        if simulation != 1:
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
                    if self.grid[i][j] == self.grid[i+1][j] and self.grid[i][j] != 0:
                        self.grid[i+1][j] *= 2
                        self.grid[i][j] = 0
                        self.score += self.grid[i+1][j]
        else:
            grid = copy.deepcopy(self.grid)
            score = self.score
            for j in range(BOARD_SIZE):
                # move tiles down
                for i in range(2, -1, -1):
                    if grid[i][j] != 0:
                        k = i
                        while k < BOARD_SIZE-1 and grid[k+1][j] == 0:
                            grid[k+1][j], grid[k][j] = grid[k][j], grid[k+1][j]
                            k += 1
                # merge adjacent tiles
                for i in range(2, -1, -1):
                    if grid[i][j] == grid[i+1][j] and grid[i][j] != 0:
                        grid[i+1][j] *= 2
                        grid[i][j] = 0
                        score += grid[i+1][j]
            grid = self.grid_to_tuple(grid)
            return grid
    
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
    
    def step(self,action):
        if action == 'L':
            self.move_left(0)
        
        elif action == 'R':
            self.move_right(0)
        
        elif action == 'U':
            self.move_up(0)
        
        elif action == 'D':
            self.move_down(0)
        
        Flag = self.add_new_tile()
        
        #Terminal
        if not Flag:
            return (False,self.grid,self.score)
        
        else:
            return (True,self.grid,self.score)
        
        