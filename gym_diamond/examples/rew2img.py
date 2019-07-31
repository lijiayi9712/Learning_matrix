import gym
import gym_diamond
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import argparse


plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 14
check_points = [75, 175, 575, 775, 975]
env = gym.make('diamond-v0')


def rew2img(duration, rewards):
    fig = plt.figure(figsize=(12, 3.25*len(check_points)))

    for y, t in enumerate(check_points):
        for x in range(rewards.shape[-1]):
            ax = fig.add_subplot(
                len(check_points),
                rewards.shape[-1],
                y * rewards.shape[-1] + x + 1
            )
            ticks = np.linspace(0, rewards.shape[0]-1, 6)
            ticklabels = [
                '{:.2f}'.format(i/5)
                for i in range(6)
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
            if x == 0:
                cbar.set_label(
                    'Reward (veh/s) at t = {} s'.
                        format(check_points[y]*env.step_size),
                    rotation=270,
                    labelpad=15
                )
                ax.set_title('Average Outflow')
            elif x == 1:
                cbar.set_label(
                    'Reward (1/s) at t = {} s'.
                        format(check_points[y]*env.step_size),
                    rotation=270,
                    labelpad=15
                )
                ax.set_title('Inverse Travel Time')
            else:
                cbar.set_label(
                    'Reward (1/s) at t = {} s'.
                        format(check_points[y]*env.step_size),
                    rotation=270,
                    labelpad=15
                )
                ax.set_title('Inverse Nash Distance')
            ax.set_xlabel(r'$p_{BC}$')
            ax.set_ylabel(r'$p_{AB}$')

    plt.tight_layout()
    plt.savefig(
        'figures/rewards_{}step_average.pdf'.format(duration))


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

    rewards = []
    for seed in range(10):
        _rewards = np.load(
            'rewards_{}step_seed{:02d}.npy'.
                format(args.duration, seed)
        )
        rewards.append(_rewards)
    rewards = np.asarray(rewards).mean(axis=0)
    rew2img(args.duration, rewards)
