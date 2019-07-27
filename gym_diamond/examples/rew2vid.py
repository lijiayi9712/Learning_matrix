import gym
import gym_diamond
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np
import argparse
import cv2


plt.rcParams["font.family"] = "Arial"
# check_points = [75, 475, 975, 4975, 9975]
env = gym.make('diamond-v0')


def rew2img(rewards, t=25):
    fig = plt.figure(figsize=(12, 2.5))
    canvas = FigureCanvas(fig)

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
            rewards[:, :, t-25:t+24, x].mean(axis=-1),
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
            ax.set_title('Average Outflow')
            cbar.set_label(
                'Rew (veh/s) at t = {} s'.format(t*env.step_size),
                rotation=270,
                labelpad=10
            )
        elif x == 1:
            ax.set_title('Inverted Travel Time')
            cbar.set_label(
                'Rew (1/s) at t = {} s'.format(t*env.step_size),
                rotation=270,
                labelpad=10
            )
        else:
            ax.set_title('Nash Equilibrium')
            cbar.set_label(
                'Rew (1/s) at t = {} s'.format(t*env.step_size),
                rotation=270,
                labelpad=10
            )
        ax.set_xlabel('p23')
        ax.set_ylabel('p12')

    plt.tight_layout()
    canvas.draw()
    width, height = fig.get_size_inches() * fig.get_dpi()
    img =  np.fromstring(
        canvas.tostring_rgb(), dtype='uint8').\
        reshape(int(height), int(width), 3)
    plt.close()
    return img


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
    print(rewards.shape)
    img = rew2img(rewards, 25)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('vid.mp4', fourcc, 30, (img.shape[1], img.shape[0]))
    for t in range(25, rewards.shape[-2]-24):
        img = rew2img(rewards, t)[:, :, ::-1]
        out.write(img)
        cv2.imshow('Vid', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    out.release()
    cv2.destroyAllWindows()
