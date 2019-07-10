from gym.envs.registration import register

register(
    id='Diamond-v0',
    entry_point='gym_diamond.envs:DiamondEnv',
)
