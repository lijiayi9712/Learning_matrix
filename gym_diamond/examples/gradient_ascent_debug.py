import numpy as np


def compute_gradient(
    x, y, seed=204, sample_number=10, sigma=0.1, alpha=0.1):

    results = []
    for _ in range(sample_number):
        epsilon_x = sigma * np.random.normal()
        epsilon_y = sigma * np.random.normal()
        next_x = x + epsilon_x
        next_y = y + epsilon_y
        rewards = -(next_x - 1)**2 - (next_y - 2)**2
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
    seed = 204
    iteration = 100
    sample_number = 10
    np.random.seed(seed)

    x = np.random.uniform(low=0, high=1)
    y = np.random.uniform(low=0, high=1)

    trajs = []
    for i in range(iteration):
        delta_x_out, delta_y_out = \
            compute_gradient(
                x,
                y,
                alpha=0.05,
                sigma=0.1
            )
        x_pos = x
        y_pos = y
        x_dir = delta_x
        y_dir = delta_y
        trajs.append(x_pos)
        trajs.append(y_pos)
        trajs.append(x_dir)
        trajs.append(y_dir)
        x += delta_x_out
        y += delta_y_out
    trajs = np.asarray(trajs).reshape(iteration, 4)

