import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import argparse


plt.rcParams["font.family"] = "Arial"
timestamps = [99, 499, 999, 4999, 9999]

def vis_tests(duration, seed):
    rewards = np.load(
        'rewards_{}step_seed{:02d}.npy'.
        format(duration, seed))[:, :, timestamps, :]
    fig = plt.figure(figsize=(12, 2.5*rewards.shape[-2]))

    for t in range(rewards.shape[-2]):
        for x in range(rewards.shape[-1]):
            ax = fig.add_subplot(
                rewards.shape[-2],
                rewards.shape[-1],
                t * rewards.shape[-1] + x + 1
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
                rewards[:, :, t, x],
                vmin=rewards[:, :, :, x].min(),
                vmax=rewards[:, :, :, x].max()
            )
            cbar = plt.colorbar(
                im,
                cax=cax,
                orientation='vertical',
                format='%.2e'
            )
            if x == 0:
                cbar.set_label(
                    'Outflow t = {}'.format(timestamps[t]),
                    rotation=270,
                    labelpad=10
                )
            elif x == 1:
                cbar.set_label(
                    'Weighted Sum t = {}'.format(timestamps[t]),
                    rotation=270,
                    labelpad=10
                )
            else:
                cbar.set_label(
                    'Nash t = {}'.format(timestamps[t]),
                    rotation=270,
                    labelpad=10
                )
            ax.set_xlabel('p23')
            ax.set_ylabel('p12')

    plt.tight_layout()
    plt.savefig('rewards_{}step_seed{:02d}.png'.format(duration, seed))


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
        '-s',
        '--seed',
        help='Specify random seed between 0 and 99.',
        type=int,
        default=0
    )
    args = parser.parse_args()
    if args.seed > 99 or args.seed < 0:
        raise ValueError('Seed must be an integer between 0 and 99.')

    vis_tests(args.duration, args.seed)


