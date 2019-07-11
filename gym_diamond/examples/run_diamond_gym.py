import gym
import gym_diamond
import numpy as np
from mpl_toolkits import mplot3d
from matplotlib import cm

env = gym.make('diamond-v0')

# for _ in range(1000):
#     action= [0.5, 0.7]
#     env.step(action)

# env.reset()
# for _ in range(1000):
#     action= [0.5, 0.7]
#     env.step(action)


import matplotlib.pyplot as plt

p1_list = np.arange(0, 1.05, 0.05)
p2_list = np.arange(0, 1.05, 0.05)
T = 100000
N = 5
reward_result = np.zeros((len(p1_list), len(p2_list), 100, N))
# for n in range(N):
# 	for i_1, p_1 in np.ndenumerate(p1_list):
# 		for i_2, p_2 in np.ndenumerate(p2_list):
# 			for t in range(T):
# 				if t % 100 == 0:
# 					action = [p_1, p_2]
# 					env.step(action)
# 					states = env.get_state()
# 					reward = env.get_reward(states)
# 					reward_result[i_1, i_2, np.int(t/100), n] = reward
# 			print("=")


# print("Finished r1")
# np.save('/Users/LiJiayi/sumo/Learning_matrix/gym_diamond/examples/reward_result.npy', reward_result)

# reward_result2 = np.zeros((len(p1_list), len(p2_list), 100, N))
# for n in range(N):
# 	for i_1, p_1 in np.ndenumerate(p1_list):
# 		for i_2, p_2 in np.ndenumerate(p2_list):
# 			for t in range(T):
# 				if t % 100 == 0:
# 					action = [p_1, p_2]
# 					env.step(action)
# 					states = env.get_state()
# 					reward = env.get_reward2(states)
# 					reward_result2[i_1, i_2, np.int(t/100), n] = reward
# 			print("=")

# print("Finished r2")
# np.save('/Users/LiJiayi/sumo/Learning_matrix/gym_diamond/examples/reward_result2.npy', reward_result2)

reward_result3 = np.zeros((len(p1_list), len(p2_list), 100, N))
for n in range(N):
	for i_1, p_1 in np.ndenumerate(p1_list):
		for i_2, p_2 in np.ndenumerate(p2_list):
			for t in range(T):
				if t % 1000 == 0:
					action = [p_1, p_2]
					env.step(action)
					states = env.get_state( )
					reward = env.get_reward3(states)
					reward_result3[i_1, i_2, np.int(t/1000), n] = reward
			print("=========")


print("Finished r3")
np.save('/Users/LiJiayi/sumo/Learning_matrix/gym_diamond/examples/reward_result3.npy', reward_result3)

