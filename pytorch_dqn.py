import torch
import torch.nn as nn
import torch.optim as optim
import gym
import random
from collections import deque

# 하이퍼파라미터
BATCH_SIZE = 32
GAMMA = 0.99
EPS_START = 1.0
EPS_END = 0.01
EPS_DECAY = 10000
TARGET_UPDATE = 10

# 에이전트 클래스
class DQNAgent:
    def __init__(self, state_dim, action_dim):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.action_dim = action_dim
        self.policy_net = self.build_model(state_dim, action_dim).to(self.device)
        self.target_net = self.build_model(state_dim, action_dim).to(self.device)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()
        self.optimizer = optim.RMSprop(self.policy_net.parameters())
        self.memory = deque(maxlen=10000)
        self.steps_done = 0
        self.episode_rewards = []

    # 신경망 구성 함수
    def build_model(self, state_dim, action_dim):
        model = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, action_dim)
        )
        return model

    # Epsilon-Greedy 정책
    def select_action(self, state, eps):
        self.steps_done += 1
        if random.random() > eps:
            with torch.no_grad():
                state = torch.FloatTensor(state).unsqueeze(0).to(self.device)
                q_values = self.policy_net(state)
                action = q_values.max(1)[1].item()
        else:
            action = random.randrange(self.action_dim)
        return action

    # 메모리에 데이터 추가
    def add_to_memory(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    # 학습 함수
    def learn(self):
        if len(self.memory) < BATCH_SIZE:
            return
        batch = random.sample(self.memory, BATCH_SIZE)
        state_batch, action_batch, reward_batch, next_state_batch, done_batch = zip(*batch)
        state_batch = torch.FloatTensor(state_batch).to(self.device)
        action_batch = torch.LongTensor(action_batch).unsqueeze(1).to(self.device)
        reward_batch = torch.FloatTensor(reward_batch).unsqueeze(1).to(self.device)
        next_state_batch = torch.FloatTensor(next_state_batch).to(self.device)
        done_batch = torch.FloatTensor(done_batch).unsqueeze(1).to(self.device)
        q_values = self.policy_net(state_batch).gather(1, action_batch)
        next
