import gym
from gym import error, spaces, utils
from gym.utils import seeding
from gym.spaces.box import Box
import traci
import sumolib
from sumolib import checkBinary
import numpy as np
np.random.seed(42)
import subprocess
import os
import sys
import time
import atexit


class DiamondEnv(gym.Env):
    def __init__(self, extra_config):
        print('Initializing diamond environment...')
        path = os.path.dirname(__file__)
        self.extra_config = extra_config

        if 'SUMO_HOME' in os.environ:
            tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
            sys.path.append(tools)
        else:
            sys.exit('please declare environment variable "SUMO_HOME"')

        netconvert_cmd = [
            'netconvert',
		    '--node-files={}/data/diamond.nod.xml'.format(path),
		    '--edge-files={}/data/diamond.edg.xml'.format(path),
		    '--type-files={}/data/diamond.type.xml'.format(path),
		    '--output-file={}/data/diamond.net.xml'.format(path)
		]
        subprocess.run(netconvert_cmd)
        sumoBinary = checkBinary('sumo')
        self.config = [
	        sumoBinary,
	        '-c', '{}/data/diamond.sumocfg'.format(path)
	    ]
        traci.start(self.config)

        self.edge_list = [
            'in_to1',
            '1to2',
            '1to3',
            '2to3',
            '2to4',
            '3to5',
            '5to4',
            '4to6',
            '6to_out'
        ]
        self.route_list = []

        self.observation_space = self.get_observation_space()
        self.action_space = self.get_action_space()
        self.step_count = 0
        self.state = self.get_state()
        self.observation = self.get_observation(self.state)
        self.reward = self.get_reward(self.observation)
        self.done = False
        self.additional = {}

        atexit.register(self.close)

    def step(self, action):
        p_1 = action[0]
        p_2 = action[1]
        trans_matrix = np.array([
            [0.0, p_1, 1-p_1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, p_2, 1-p_2, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        ]).flatten()
        self.step_count += 1

        route_id = self._gen_route(trans_matrix)
        veh_index = self.step_count
        self._add_vehicle(veh_index, route_id)
        traci.simulationStep()

        self.state = self.get_state()
        self.observation = self.get_observation(self.state)
        self.reward = self.get_reward(self.observation)

        return self.observation, self.reward, self.done, self.additional

    def get_observation_space(self):
        return Box(
            low=0,
            high=100, # This is arbitary
            shape=(18,),
            dtype=np.float32
        )

    def get_action_space(self):
        return Box(
            low=0,
            high=1,
            shape=(2,),
            dtype=np.float32
        )

    def get_state(self):
        state = []
        for edge_id in self.edge_list:
            state.append(traci.edge.getLastStepVehicleNumber(edge_id))
            state.append(traci.edge.getLastStepMeanSpeed(edge_id))
        return np.asarray(state)

    def get_observation(self, state):
        # State is fully observable
        return state

    def get_reward(self, observation):
        return traci.edge.getLastStepMeanSpeed('6to_out')

    def reset(self):
        traci.load(self.config[1:])
        self.route_list = []
        self.step_count = 0
        self.state = self.get_state()
        self.observation = self.get_observation(self.state)
        self.reward = self.get_reward(self.observation)
        self.done = False
        self.additional = {}
        return self.observation

    def render(self):
        raise NotImplementedError

    def close(self):
        traci.close()
        print('\nEnvironment closed. Goodbye <コ:彡')

    def _gen_route(self, trans_matrix):
	    route = ['in_to1']
	    node_index = 0
	    while route[-1] != '6to_out':
	        probs = trans_matrix[
	            node_index*len(self.edge_list):\
                (node_index+1)*len(self.edge_list)
            ]
	        next_edge = np.random.choice(self.edge_list, 1, p=probs)[0]
	        route.append(next_edge)
	        node_index = self.edge_list.index(next_edge)
	    route_id = '>'.join(route)
	    if route_id not in self.route_list:
	        self.route_list.append(route_id)
	        traci.route.add(route_id, route)
	    return route_id

    def _add_vehicle(self, veh_index, route_id):
	    traci.vehicle.addFull(
	        vehID='veh{:06}'.format(veh_index),
	        routeID=route_id,
	        typeID='vehicle',
	        departSpeed=10,
	    )
