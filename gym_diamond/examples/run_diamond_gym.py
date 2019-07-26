import gym
import gym_diamond
import numpy as np
import argparse


def run_tests(duration, seed):
    np.random.seed(seed)
    env = gym.make('diamond-v0')

    #rewards = []
    observation_stack = []
    search_points = np.linspace(0.0, 1.0, 21)
    for p12 in search_points:
        for p23 in search_points:
            env.reset()
            for t in range(duration):
                obs, _, _, _ = env.step([p12, p23]) 
                observation_stack.append(obs)
                # rewards.append(env.get_reward(obs, category='out'))
                # rewards.append(env.get_reward(obs, category='sum'))
                # rewards.append(env.get_reward(obs, category='nas'))
            print("-", end =" ")
        print('Another round!')
    # rewards = np.asarray(rewards)
    # rewards = rewards.reshape(
    #     len(search_points), len(search_points), duration, 3)

	
    observation_stack = np.vstack(observation_stack)
    np.save('observation_{}step_seed{:02d}.npy'.format(duration, seed), observation_stack)
    print("One Done!")
    #np.save('rewards_{}step_seed{:02d}.npy'.format(duration, seed), rewards)



if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     '-d',
    #     '--duration',
    #     help='Specify test duration in number of steps.',
    #     type=int,
    #     default=1000
    # )
    # parser.add_argument(
    #     '-s',
    #     '--seed',
    #     help='Specify random seed between 0 and 99.',
    #     type=int,
    #     default=0
    # )
    # args = parser.parse_args()
    # if args.seed > 99 or args.seed < 0:
    #     raise ValueError('Seed must be an integer between 0 and 99.')
    for seed in range(5, 10):
    	run_tests(10000, seed)

    #run_tests(args.duration, args.seed)
    

