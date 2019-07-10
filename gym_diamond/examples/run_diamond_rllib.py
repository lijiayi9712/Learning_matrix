"""Example of a custom gym environment and model. Run this for a demo.
This example shows:
  - using a custom environment
  - using a custom model
  - using Tune for grid search
You can visualize experiment results in ~/ray_results using TensorBoard.
"""

import numpy as np
import gym
import gym_diamond
from gym_diamond.envs.diamond_env import DiamondEnv
from ray.rllib.models import FullyConnectedNetwork, Model, ModelCatalog

import ray
from ray import tune


class CustomModel(Model):
    """Example of a custom model.
    This model just delegates to the built-in fcnet.
    """

    def _build_layers_v2(self, input_dict, num_outputs, options):
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Building custom model...')
        self.obs_in = input_dict["obs"]
        self.fcnet = FullyConnectedNetwork(input_dict, self.obs_space,
                                           self.action_space, num_outputs,
                                           options)
        return self.fcnet.outputs, self.fcnet.last_layer


if __name__ == "__main__":
    # Can also register the env creator function explicitly with:
    # register_env("corridor", lambda config: SimpleCorridor(config))
    ray.init()
    # ModelCatalog.register_custom_model("my_model", CustomModel)
    tune.run(
        "PPO",
        stop={
            "timesteps_total": 1e4,
        },
        config={
            "env": DiamondEnv,
            # "model": {
            #     "custom_model": "my_model",
            # },
            "lr": 1e-2,
            "num_workers": 1,
        },
    )
