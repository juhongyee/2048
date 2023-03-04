import random

BOARD_SIZE = 4

class Game2048:
    def __init__(self):
        self.grid = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()

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
                if self.grid[i][j] == self.grid[i][j-1] and self.grid[i][j] != 0:
                    self.grid[i][j-1] *= 2
                    self.grid[i][j] = 0
                    self.score += self.grid[i][j-1]

    def move_right(self):
        for i in range(BOARD_SIZE):
            # move tiles to the right
            for j in range(2, -1, -1):
                if self.grid[i][j] != 0:
                    k = j
                    while k < 3 and self.grid[i][k+1] == 0:
                        self.grid[i][k+1], self.grid[i][k] = self.grid[i][k], self.grid[i][k+1]
                        k += 1
            # merge adjacent tiles
            for j in range(2, -1, -1):
                if self.grid[i][j] == self.grid[i][j+1] and self.grid[i][j] != 0:
                    self.grid[i][j+1] *= 2
                    self.grid[i][j] = 0
                    self.score += self.grid[i][j+1]

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
                if self.grid[i][j] == self.grid[i-1][j] and self.grid[i][j] != 0:
                    self.grid[i-1][j] *= 2
                    self.grid[i][j] = 0
                    self.score += self.grid[i-1][j]

    def move_down(self):
        for j in range(BOARD_SIZE):
            # move tiles down
            for i in range(2, -1, -1):
                if self.grid[i][j] != 0:
                    k = i
                    while k < 3 and self.grid[k+1][j] == 0:
                        self.grid[k+1][j], self.grid[k][j] = self.grid[k][j], self.grid[k+1][j]
                        k += 1
            # merge adjacent tiles
            for i in range(2, -1, -1):
                if self.grid[i][j] == self.grid[i+1][j] and self.grid[i][j] != 0:
                    self.grid[i+1][j] *= 2
                    self.grid[i][j] = 0
                    self.score += self.grid[i+1][j]

    def print_score(self):
        print("score:", self.score)

    def game_over_message(self):
        print("Game Over!")
        self.print_score()

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

if __name__ == "__main__":
    print("2048 게임을 시작합니다!!\n")
    game = Game2048()
    game.print_grid()
    
    print("\n이동할 방향을 숫자로 입력해주세요: up = 1 down = 2 left = 3 right = 4 exit = 5")

    while True:
        # 명령 입력
        while True:
            try:
                value = int(input("1, 2, 3, 4, 5(종료) 중 하나를 입력하세요: "))
                if value not in [1, 2, 3, 4, 5]:
                    raise ValueError
                break
            except ValueError:
                print("잘못된 입력입니다.")
        
        # 입력에 따라 tile을 한 방향으로 움직인다.
        if value == 1:
            game.move_up()
        elif value == 2:
            game.move_down()
        elif value == 3:
            game.move_left()
        elif value == 4:
            game.move_right()
        else: # value = 5
            game.game_over_message()
            break
        
        # 새로운 tile을 생성할 수 없으면 최종 점수를 출력하고 종료한다.
        isGameOver = game.add_new_tile()
        if isGameOver == False:
            game.game_over_message()
            break

        # 움직인 상태의 game board를 출력한다.
        game.print_grid()

