import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import argparse


plt.rcParams["font.family"] = "Arial"
timestamps = [99, 499, 999, 4999, 9999]



def concat():
    concat_rewards = []
    for seed in np.arange(0, 10, 1):
        rewards = np.load(
        'rewards_{}step_seed{:02d}.npy'.
        format(10000, seed))[:, :, :, :]
        if concat_rewards != []:
            concat_rewards = np.concatenate((concat_rewards,rewards[np.newaxis,:,:,:,:]),axis=0)
        else:
            concat_rewards = rewards[np.newaxis,:,:,:,:]
    return np.average(concat_rewards, axis=0)

def average_over_time(reward_frame):
    for t in reversed(range(10, 10000)):
        reward_frame[:, :, t, :] = np.average(reward_frame[:, :, (t-10):t, :], axis=2)
    return reward_frame


def vis_continuous():
    concatenated = concat()
    rewards_time_avg = average_over_time(concatenated)
    for timestep in np.arange(2000, 5000, 10):
        rewards = rewards_time_avg[:, :, timestep, :]
        #fig = plt.figure(figsize=(30, 5))
        fig = plt.figure(figsize=(12, 2.5))
        for x in range(rewards_time_avg.shape[-1]):
            t = 0
            ax = fig.add_subplot(
                1,
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
            if x != 2:
                mean_val = np.mean(rewards_time_avg[:, :, :, x])
                sd_val = np.std(rewards_time_avg[:, :, :, x])  
            else:
                mean_val = np.ma.mean(np.ma.masked_invalid(rewards_time_avg[:, :, :, x]))
                sd_val = np.ma.std(np.ma.masked_invalid(rewards_time_avg[:, :, :, x]))  
            
            
            v_min = max(0, mean_val - 2 * sd_val)
            v_max = mean_val + 2 * sd_val

            if x == 2:
                v_min = 0
                v_max = 1e4

            X = np.linspace(0.0, 1.0, 21)
            Y = np.linspace(0.0, 1.0, 21)

            X, Y = np.meshgrid(X, Y)
            
            Z = rewards_time_avg[:, :, timestep, x] #rewards[:, :, x]
            contours = ax.contour(X, Y, Z, 3, colors='black')
            
            plt.clabel(contours, inline=True, fontsize=4)
            #plt.imshow(Z, extent=[0, 1, 0, 1], origin='lower', cmap='RdGy', alpha=0.5)
            im = ax.imshow(
                Z, 
                extent=[0, 1, 0, 1], 
                vmin = v_min,
                vmax = v_max, 
                cmap='RdGy',
                alpha=0.5
            )
            cbar = plt.colorbar(
                im,
                cax=cax,
                orientation='vertical',
                format='%.2e'
            )

            if x == 0:
                cbar.set_label(
                    'Outflow t = {}'.format(timestep),
                    rotation=270,
                    labelpad=10
                )
            elif x == 1:
                cbar.set_label(
                    'Weighted Sum t = {}'.format(timestep),
                    rotation=270,
                    labelpad=10
                )
            else:
                cbar.set_label(
                    'Nash t = {}'.format(timestep),
                    rotation=270,
                    labelpad=10
                )
            ax.set_xlabel('p23')
            ax.set_ylabel('p12')
        plt.tight_layout()
        plt.savefig('pics/rewards_10000step_{:05d}_seed_average_overtime.png'.format(timestep))

def vis_tests(duration, seed):
    concatenated = concat()
    rewards = average_over_time(concatenated)
    rewards = rewards[:, :, timestamps, :]
    # rewards = np.load(
    #     'rewards_{}step_seed{:02d}.npy'.
    #     format(duration, seed))[:, :, timestamps, :]
    
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
    #plt.savefig('rewards_{}step_seed{:02d}.png'.format(duration, seed))
    plt.savefig('rewards_{}step_seed_average_overtime.png'.format(duration))
    


if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     '-d',
    #     '--duration',
    #     help='Specify test duration in number of steps.',
    #     type=int,
    #     default=10000
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
    #vis_tests(args.duration, args.seed)
    vis_continuous()


