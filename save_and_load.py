import Env2048
import numpy as np
from collections import deque
import json
import os

class MC_agent:
    def __init__(self):
        self.env = Env2048.Game2048()
        self.action = ['L','R','U','D'] #좌,우,위,아래
        self.value_list = {}
        self.gamma = 0.95
        self.e = 0.1
        self.memory = deque()
        self.learning_rate = 0.05
    
    def get_action(self,state):
        if np.random.randn() < self.e :
            idx = np.random.choice(len(self.action),1)[0]
        else:
            next_values = np.array([])
            
            #각 이동시 얻을 수 있는 값들 저장
            #up
            next_state = self.env.move_up(1)
            if next_state not in self.value_list:
                self.value_list[next_state] = 0 #value_list에 없으면 0 그 value를 0으로
            next_values = np.append(next_values,self.value_list[next_state])
            
            #down
            next_state = self.env.move_down(1)
            if next_state not in self.value_list:
                self.value_list[next_state] = 0 #value_list에 없으면 0 그 value를 0으로
            next_values = np.append(next_values,self.value_list[next_state])
            
            #left
            next_state = self.env.move_left(1)
            if next_state not in self.value_list:
                self.value_list[next_state] = 0 #value_list에 없으면 0 그 value를 0으로
            next_values = np.append(next_values,self.value_list[next_state])
            
            #right
            next_state = self.env.move_right(1)
            if next_state not in self.value_list:
                self.value_list[next_state] = 0 #value_list에 없으면 0 그 value를 0으로
            next_values = np.append(next_values,self.value_list[next_state])
            
            max_val = max(next_values)
            
            action_list = np.where(next_values == max_val)[0]
            
            if len(action_list) > 1:
                idx = np.random.choice(action_list,1)[0]
            else:
                idx = action_list[0]
            
        action = self.action[idx]
            
        return action

    def update(self):
        G_t = 0
        
        while(deque):
            sample = deque.pop()
            state = sample[1]
            reward = sample[2]
            
            G_t = reward + self.gamma*G_t
            V_t = self.value_list[self.env.grid_to_tuple(state)]
            
            #update Value
            self.value_table = V_t + self.learning_rate*(G_t-V_t)

# 데이터 저장 함수
def save_data(agent, filename):
    data = {
        "value_list": agent.value_list,
    }
    with open(filename, 'w') as f:
        json.dump(data, f)

# 데이터 불러오기 함수
def load_data(agent, filename):
    if not os.path.exists(filename):
        return

    with open(filename, 'r') as f:
        data = json.load(f)

    agent.value_list = data.get("value_list", {})

#main

agent = MC_agent()
num_episodes = 100000
max_reward = 0

for episode in range(num_episodes):
    action_sequence = []
    total_reward = 0
    state = agent.env.reset()
    action = agent.get_action(state)
    done = False
    walk = 0
    
    while True:
        done,next_state,reward = agent.env.step(action)
        
        #경로 기억
        data = (done,state,reward)
        agent.memory.append(data)
        
        #action 기억
        action_sequence.append(action)
        walk += 1
        
        #next and action
        state = next_state
        action = agent.get_action(state)
        
        if not done:
            total_reward = reward
            max_reward = max(total_reward,max_reward)
            
            if episode % 5000 == 0:
                print('finished at', state)
                print('episode :{}, The number of step:{}\n The sequence of action is:\{}\nThe total reward is: {}\nThe Max reward is : {}\n'.format(episode, walk, action_sequence, total_reward,max_reward))
            
            agent.update
            agent.memory.clear()
            break

print('The Max : ', max_reward)