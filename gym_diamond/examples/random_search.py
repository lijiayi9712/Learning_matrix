import gym
import gym_diamond
import numpy as np
import argparse


def compute_reward(p12, p23, category='out'):
    rewards = []
    for _ in range(sample_number):
        env.reset()
        _rewards = []
        for t in range(args.duration):
            obs, _, _, _ = env.step([p12, p23])
            if t > 949:
                _rewards.append(env.get_reward(obs, category=category))
        rewards.append(np.mean(_rewards))
    return np.mean(rewards)


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
    iteration = 50
    sample_number = 10
    np.random.seed(seed)
    env = gym.make('diamond-v0')
    results = []
    for _ in range(iteration):
        p23 = np.random.uniform(0, 1)
        p12 = np.random.uniform(0, 1)
        reward = compute_reward(p12, p23, category='out')
        results.append(p23)
        results.append(p12)
        results.append(reward)
        p23 = np.random.uniform(0, 1)
        p12 = np.random.uniform(0, 1)
        reward = compute_reward(p12, p23, category='sum')
        results.append(p23)
        results.append(p12)
        results.append(reward)
        p23 = np.random.uniform(0, 1)
        p12 = np.random.uniform(0, 1)
        reward = compute_reward(p12, p23, category='nas')
        results.append(p23)
        results.append(p12)
        results.append(reward)

    results = np.asarray(results).reshape(iteration, 3, 3)

    trajs = []
    for i in range(iteration):
        for x in range(3):
            x_pos = results[i, x, 0]
            y_pos = results[i, x, 1]
            if i < results.shape[0] - 1:
                x_dir = results[i+1, x, 0] - x_pos
                y_dir = results[i+1, x, 1] - y_pos
            else:
                opt_idx = np.argmax(results[:, x, 2])
                x_dir = results[opt_idx, x, 0] - x_pos
                y_dir = results[opt_idx, x, 1] - y_pos
            trajs.append(x_pos)
            trajs.append(y_pos)
            trajs.append(x_dir)
            trajs.append(y_dir)
    trajs = np.asarray(trajs).reshape(iteration, 3, 4)

    np.save('trajs_random_search.npy', trajs)

