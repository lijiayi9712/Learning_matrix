from gym.envs.registration import register

register(
    id='diamond-v0',
    entry_point='gym_diamond.envs:DiamondEnv',
)
