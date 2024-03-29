import subprocess
import os
import sys
import atexit
import gym
from gym.spaces.box import Box
import traci
import sumolib
from sumolib import checkBinary
import numpy as np
# np.random.seed(42)

class DiamondEnv(gym.Env):
    def __init__(self): #, extra_config
        print('Initializing diamond environment...')
        path = os.path.dirname(__file__)
        #self.extra_config = extra_confi

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
            '-c', '{}/data/diamond.sumocfg'.format(path),
            '--step-length', '0.1',
            '--no-step-log'
        ]
        traci.start(self.config)

        self.edge_list = [
            'E1',
            '12',
            '13',
            '23',
            '24',
            '35',
            '54',
            '46',
            '6X'
        ]
        self.route_list = []
        self.net = sumolib.net.readNet('{}/data/diamond.net.xml'.format(path))
        self.observation_space = self.get_observation_space()
        self.action_space = self.get_action_space()
        self.step_count = 0
        self.state = self.get_state()
        self.observation = self.get_observation(self.state)
        self.reward = self.get_reward(self.observation)
        self.done = False
        self.additional = {}

        atexit.register(self.close)

    def step(self, action, reward_category='out'):
        p12 = action[0]
        p13 = 1 - p12
        p23 = action[1]
        p24 = 1 - p23
        trans_matrix = np.array([
            # E1   12   13   23   24   35   54   46   6X
            [0.0, p12, p13, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # E1
            [0.0, 0.0, 0.0, p23, p24, 0.0, 0.0, 0.0, 0.0],  # 12
            [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],  # 13
            [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],  # 23
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],  # 24
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0],  # 35
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],  # 54
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0],  # 46
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]   # 6X
        ]).flatten()
        self.step_count += 1

        if np.random.random() > 0.5:
            route_id = self._gen_route(trans_matrix)
            veh_index = self.step_count
            self._add_vehicle(veh_index, route_id)

        traci.simulationStep()

        self.state = self.get_state()
        self.observation = self.get_observation(self.state)
        self.reward = self.get_reward(
            self.observation, category=reward_category)

        return self.observation, self.reward, self.done, self.additional

    def get_observation_space(self):
        return Box(
            low=0,
            high=1000, # This is arbitary
            shape=(27,),
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
            state.append(self.net.getEdge(edge_id).getLength())
            state.append(traci.edge.getLastStepVehicleNumber(edge_id))
            state.append(traci.edge.getLastStepMeanSpeed(edge_id))
        return np.asarray(state)

    def get_observation(self, state):
        # State is fully observable
        return state

    def get_reward(self, observation, category='out'):
        epsilon = 0.0001
        if category == 'out':
            return observation[-1]
        elif category == 'sum':
            sum_over = 0
            for i in range(len(self.edge_list)):
                div = (observation[i*3+2] * \
                    observation[i*3+1])
                if div == 0:
                    continue
                sum_over += observation[i*3] / div
            if sum_over != 0:
                return 1/sum_over
            else:
                return sum_over
        elif category == 'nas':

            upper = observation[1*3]/(observation[1*3+2]+epsilon) + \
                observation[4*3]/(observation[4*3+2]+epsilon)
            lower = observation[2*3]/(observation[2*3+2]+epsilon) + \
                observation[6*3]/(observation[6*3+2] + epsilon)
            short_cut = observation[1*3]/(observation[1*3+2]+epsilon) + \
                observation[3*3]/(observation[3*3+2]+epsilon) + \
                observation[6*3]/(epsilon + observation[6*3+2])
            nash_val = (upper - lower) * (upper - lower) + \
                (short_cut - upper) * (short_cut - upper)
            return nash_val
        else:
            raise ValueError(
                'Reward can only be one of the following: "out", "sum", "nas".')

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

    def render(self, mode):
        raise NotImplementedError

    def close(self):
        traci.close()
        print('Environment closed. Goodbye <コ:彡')

    def _gen_route(self, trans_matrix):
        route = ['E1']
        node_index = 0
        while route[-1] != '6X':
            probs = trans_matrix[
                node_index*len(self.edge_list):
                (node_index+1)*len(self.edge_list)
            ]
            next_edge = np.random.choice(self.edge_list, p=probs)
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
