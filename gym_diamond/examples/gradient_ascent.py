import gym
import gym_diamond
import numpy as np
import copy
import argparse


def compute_gradient(
    x, y, seed=204, sample_number=10, sigma=0.1, category='out', alpha=0.1):
    np.random.seed(seed)
    results = []
    for _ in range(sample_number):
        epsilon_x = sigma * np.random.normal()
        epsilon_y = sigma * np.random.normal()
        next_x = x + epsilon_x
        next_y = y + epsilon_y
        p23 = np.clip(next_x, 0, 1)
        p12 = np.clip(next_y, 0, 1)
        env.reset()
        rewards = []
        for t in range(args.duration):
            obs, _, _, _ = env.step([p12, p23])
            if t > 949:
                rewards.append(env.get_reward(obs, category=category))
        rewards = np.mean(rewards)
        results.append([rewards, epsilon_x, epsilon_y])
    results = np.asarray(results)
    delta_x = \
        alpha * np.dot(results[:, 0], results[:, 1]) / \
        (sample_number * sigma)
    delta_y = \
        alpha * np.dot(results[:, 0], results[:, 2]) / \
        (sample_number * sigma)
    return delta_x, delta_y


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d',
        '--duration',
        help='Specify test duration in number of steps.',
        type=int,
        default=1000
    )
    args = parser.parse_args()

    seed = 204
    iteration = 100
    sample_number = 10
    np.random.seed(seed)
    env = gym.make('diamond-v0')

    x0 = np.random.uniform(0, 1)
    y0 = np.random.uniform(0, 1)
    x_out = copy.deepcopy(x0)
    y_out = copy.deepcopy(y0)
    x_sum = copy.deepcopy(x0)
    y_sum = copy.deepcopy(y0)
    x_nas = copy.deepcopy(x0)
    y_nas = copy.deepcopy(y0)

    trajs = []
    for i in range(iteration):
        delta_x_out, delta_y_out = \
            compute_gradient(
                x_out,
                y_out,
                category='out',
                alpha=0.05,
                sigma=0.1
            )
        x_pos = x_out
        y_pos = y_out
        x_dir = np.clip(x_out+delta_x_out, 0, 1) - x_out
        y_dir = np.clip(y_out+delta_y_out, 0, 1) - y_out
        trajs.append(x_pos)
        trajs.append(y_pos)
        trajs.append(x_dir)
        trajs.append(y_dir)
        x_out = np.clip(x_out+delta_x_out, 0, 1)
        y_out = np.clip(y_out+delta_y_out, 0, 1)

        delta_x_sum, delta_y_sum = \
            compute_gradient(
                x_sum,
                y_sum,
                category='sum',
                alpha=0.5,
                sigma=1
            )
        x_pos = x_sum
        y_pos = y_sum
        x_dir = np.clip(x_sum+delta_x_sum, 0, 1) - x_sum
        y_dir = np.clip(y_sum+delta_y_sum, 0, 1) - y_sum
        trajs.append(x_pos)
        trajs.append(y_pos)
        trajs.append(x_dir)
        trajs.append(y_dir)
        x_sum = np.clip(x_sum+delta_x_sum, 0, 1)
        y_sum = np.clip(y_sum+delta_y_sum, 0, 1)

        delta_x_nas, delta_y_nas = \
            compute_gradient(
                x_nas,
                y_nas,
                category='nas',
                alpha=0.1,
                sigma=0.5
            )
        x_pos = x_nas
        y_pos = y_nas
        x_dir = np.clip(x_nas+delta_x_nas, 0, 1) - x_nas
        y_dir = np.clip(y_nas+delta_y_nas, 0, 1) - y_nas
        trajs.append(x_pos)
        trajs.append(y_pos)
        trajs.append(x_dir)
        trajs.append(y_dir)
        x_nas = np.clip(x_nas+delta_x_nas, 0, 1)
        y_nas = np.clip(y_nas+delta_y_nas, 0, 1)

    trajs = np.asarray(trajs).reshape(iteration, 3, 4)

    np.save('trajs_gradient_ascent.npy', trajs)

