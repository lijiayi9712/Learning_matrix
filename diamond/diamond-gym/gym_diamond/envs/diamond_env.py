import gym
from gym import error, spaces, utils
from gym.utils import seeding
PATH = '/Users/LiJiayi/sumo/Learning_matrix/data'


"""
======================
imports from runner.py
======================
"""

import subprocess
import numpy as np
import os
import sys
np.random.seed(42)  # make tests reproducible (TODO: check if this is indeed effective)

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit('please declare environment variable "SUMO_HOME"')

from sumolib import checkBinary
import traci
import sumolib





class DiamondEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    def __init__(self):
        netconvert_cmd = [
            'netconvert',
		    '--node-files=' + PATH + '/diamond.nod.xml',
		    '--edge-files=' + PATH + '/diamond.edg.xml',
		    '--type-files=' + PATH + '/diamond.type.xml',
		    '--output-file=' + PATH + '/diamond.net.xml'
		]
        subprocess.run(netconvert_cmd)
        sumoBinary = checkBinary('sumo-gui')
        traci.start([
	        sumoBinary,
	        '-c', PATH+'/diamond.sumocfg',
	        '--tripinfo-output', PATH +'/tripinfo.xml'
	    ])
        self.reward=1
        self.next_state=1
        self.done=1
        self.additional=1
        self.route_list=[]

  #def step(self, action):
  
    def gen_route(trans_matrix):
	    route = ['in_to1']
	    node_index = 0
	    edge_list = [
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
	    while route[-1] != '6to_out':
	        probs = trans_matrix[
	            node_index*len(edge_list):(node_index+1)*len(edge_list)]
	        next_edge = np.random.choice(edge_list, 1, p=probs)[0]
	        route.append(next_edge)
	        node_index = edge_list.index(next_edge)
	    route_id = '>'.join(route)
	    if route_id not in self.route_list:
	        self.route_list.append(route_id)
	        traci.route.add(route_id, route)
	    return route_id


    def add_vehicle(veh_index, route_id):
	    traci.vehicle.addFull(
	        vehID='veh{:06}'.format(veh_index),
	        routeID=route_id,
	        typeID='vehicle',
	        departSpeed=10,
	    )

    def step(self, veh_index, trans_matrix):
        route_id = gen_route(trans_matrix)
        add_vehicle(veh_index, route_id)
        traci.simulationStep()
        return [self.next_state, self.reward, self.done, self.additional]
		#TODO: return the next state, 
				#the reward for the current state, 
				# a boolean representing whether the current episode of our model is done 
				# some additional info on our problem
	

    def reset(self):
        traci.load()
  # def render(self, mode='human', close=False):
  #   ...





