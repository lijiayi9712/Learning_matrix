import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import argparse


plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 14


d = 10
g = np.array([[0, 0, 1, 1, 0.1, 0, 0, 0],
              [1, 0, 2, 2, 0, 0, 0, 0],
              [2, 1, 2, 0.25, 0, 0, 0, 0],
              [3, 1, 3, 2, 0, 0, 0, 0],
              [4, 2, 3, 1, 0.1, 0, 0, 0]])


def travel_time(f):
    return g[:, 3] + g[:, 4] * f + g[:, 5] * (f ** 2) + g[:, 6] * (f ** 3) + g[:, 7] * (f ** 4)


delta = np.array([[1, 0, 1, 0, 1],
                  [1, 0, 0, 1, 0],
                  [0, 1, 0, 0, 1]])


def flow(pAB, pBC):
    path_flow = d * np.array([pAB * pBC, pAB * (1 - pBC), (1 - pAB)])
    return delta.T @ path_flow


def outflow(pAB, pBC):
    return d


def total_travel_time(pAB, pBC):
    f = flow(pAB, pBC)
    tt = travel_time(f)
    return tt.T @ f


def regret(pAB, pBC):
    f = flow(pAB, pBC)
    tt = travel_time(f)
    return max([tt.T @ (f - d * delta[i]) for i in range(3)])


if __name__ == '__main__':
    n = 21
    rewards1 = np.asarray([
        [-outflow(j / n, i / n) for i in range(n)]
        for j in range(n)
    ])
    rewards2 = np.asarray([
        [-total_travel_time(j / n, i / n) for i in range(n)]
        for j in range(n)
    ])
    rewards3 = np.asarray([
        [-regret(j / n, i / n) for i in range(n)]
        for j in range(n)
    ])
    rewards = [rewards1, rewards2, rewards3]

    fig = plt.figure(figsize=(12, 3.25))

    for x in range(3):
        ax = fig.add_subplot(
            1,
            3,
            x + 1
        )
        ticks = np.linspace(0, n-1, 6)
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
            rewards[x],
            vmin=rewards[x].mean() - rewards[x].std(),
            vmax=rewards[x].mean() + rewards[x].std(),
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
                'Reward (veh/s) at equilibrium',
                rotation=270,
                labelpad=10
            )
            ax.set_title('Average Outflow')
        elif x == 1:
            cbar.set_label(
                'Reward (1/s) at equilibrium',
                rotation=270,
                labelpad=10
            )
            ax.set_title('Inverse Travel Time')
        else:
            cbar.set_label(
                'Reward (1/s) at equilibrium',
                rotation=270,
                labelpad=10
            )
            ax.set_title('Nash Distance')
        ax.set_xlabel(r'$p_{BC}$')
        ax.set_ylabel(r'$p_{AB}$')

    plt.tight_layout()
    plt.savefig('figures/static_traffic_assignment.pdf')

