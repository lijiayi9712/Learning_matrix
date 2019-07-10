import gym
import gym_diamond

env = gym.make('diamond-v0')

for _ in range(100):
    action= [0.5, 0.7]
    env.step(action)

env.reset()
for _ in range(100):
    action= [0.5, 0.7]
    env.step(action)

