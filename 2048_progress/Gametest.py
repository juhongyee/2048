import gym
import Env2048
import numpy as np
env = Env2048.Game2048()

gameover = False

print(env.grid)

while(not gameover):
    print("action을 입력해주세요.")
    print("L : 0, R : 1, U : 2, D : 3")
    action = int(input())
    a,b,c,d = env.step(action)
    print(a)
    