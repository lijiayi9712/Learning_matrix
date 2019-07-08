import logging
from gym.envs.registration import register

logger = logging.getLogger(__name__)

register(
    id='Diamond-v0',
    entry_point='gym_diamond.envs:DiamondEnv',
)