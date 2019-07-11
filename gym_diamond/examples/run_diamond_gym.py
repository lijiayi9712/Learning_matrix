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

p1_list = np.arange(0, 1.05, 0.1)
p2_list = np.arange(0, 1.05, 0.1)
T = 100000
N = 10
reward_result = np.zeros((len(p1_list), len(p2_list), 10000, N))
for n in range(N):
	for i_1, p_1 in np.ndenumerate(p1_list):
		for i_2, p_2 in np.ndenumerate(p2_list):
			for t in range(T):
				if t % 100 == 0:
					action = [p_1, p_2]
					env.step(action)
					states = env.get_state()
					reward = env.get_reward3(states)
					reward_result[i_1, i_2, np.int(t/100), n] = reward

# print(reward_result[:, :, 0, 1])
# ax = plt.axes(projection='3d')
# x = p1_list
# y = p2_list
# z = reward_result[:, :, 5, :].mean(axis=2)

# ax.contour3D(x, y, z, cmap=cm.coolwarm)
# ax.set_xlabel('x')
# ax.set_ylabel('y')
# ax.set_zlabel('z');



# # plt.matshow(reward_result[:,:,50, 2])
# plt.show()