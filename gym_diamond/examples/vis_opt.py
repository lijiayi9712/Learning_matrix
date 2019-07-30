import gym
import gym_diamond
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import argparse


plt.rcParams["font.family"] = "Arial"


def show_traj(rewards, trajs, t=975):
    fig = plt.figure(figsize=(12, 2.5))

    for x in range(rewards.shape[-1]):
        ax = fig.add_subplot(
            1,
            rewards.shape[-1],
            x + 1
        )
        ticks = np.linspace(0, rewards.shape[0]-1, 11)
        ticklabels = [
            '{:.2f}'.format(i/(10))
            for i in range(11)
        ]
        ax.set_xticks(ticks)
        ax.set_xticklabels(ticklabels, rotation=45, ha='center')
        ax.set_yticks(ticks)
        ax.set_yticklabels(ticklabels)
        div = make_axes_locatable(ax)
        cax = div.append_axes('right', size='5%', pad=0.05)
        im = ax.imshow(
            rewards[:, :, t-25:t+25, x].mean(axis=-1),
            vmin=0,
            vmax=rewards[:, :, :, x].mean() + rewards[:, :, :, x].std(),
            cmap='RdYlGn'
        )
        cbar = plt.colorbar(
            im,
            cax=cax,
            orientation='vertical',
            # format='%.2e'
        )
        ax.quiver(
            trajs[:, x, 0] * 10,
            trajs[:, x, 1] * 10,
            trajs[:, x, 2] * 10,
            trajs[:, x, 3] * 10,
            scale_units='xy',
            angles='xy',
            scale=1,
            linewidths=3
        )
        ax.scatter(
            [trajs[0, x, 0] * 10],
            [trajs[0, x, 1] * 10],
            marker='o',
            s=25,
            color='m'
        )
        ax.scatter(
            [(trajs[-1, x, 0] + trajs[-1, x, 2]) * 10],
            [(trajs[-1, x, 1] + trajs[-1, x, 3]) * 10],
            marker='*',
            s=75,
            color='m'
        )
        if x == 0:
            cbar.set_label(
                'Avg OF (veh/s) at t = {} s'.
                    format(t*env.step_size),
                rotation=270,
                labelpad=10
            )
        elif x == 1:
            cbar.set_label(
                'Inverted TT (1/s) at t = {} s'.
                    format(t*env.step_size),
                rotation=270,
                labelpad=10
            )
        else:
            cbar.set_label(
                'Nash Eq (1/s) at t = {} s'.
                    format(t*env.step_size),
                rotation=270,
                labelpad=10
            )
        ax.set_xlabel('p23')
        ax.set_ylabel('p12')

    plt.tight_layout()
    plt.savefig('{}.png'.format(args.optimizer))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d',
        '--duration',
        help='Specify test duration in number of steps.',
        type=int,
        default=1000
    )
    parser.add_argument(
        '-o',
        '--optimizer',
        help='Specify optimizer of trajectories.',
        type=str,
        default='random_search'
    )
    args = parser.parse_args()
    if args.optimizer not in ['random_search', 'gradient_ascent']:
        raise ValueError(
            'Optmizer must be one of the following: ' +
            '"random_search" or "gradient_ascent".')

    env = gym.make('diamond-v0')

    trajs = np.load('trajs_{}.npy'.format(args.optimizer))
    rewards = []
    for seed in range(10):
        _rewards = np.load(
            'rewards_{}step_seed{:02d}.npy'.
                format(args.duration, seed)
        )
        rewards.append(_rewards)
    rewards = np.asarray(rewards).mean(axis=0)

    show_traj(rewards, trajs, t=975)
