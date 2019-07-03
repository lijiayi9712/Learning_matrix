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

route_list = []

def init():
    netconvert_cmd = [
        'netconvert',
        '--node-files=data/diamond.nod.xml',
        '--edge-files=data/diamond.edg.xml',
        '--type-files=data/diamond.type.xml',
        '--output-file=data/diamond.net.xml'
    ]
    subprocess.run(netconvert_cmd)
    sumoBinary = checkBinary('sumo')
    traci.start([
        sumoBinary,
        '-c', 'data/diamond.sumocfg',
        '--tripinfo-output', 'data/tripinfo.xml'
    ])


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
        '4to_out'
    ]
    while route[-1] != '4to_out':
        probs = trans_matrix[
            node_index*len(edge_list):(node_index+1)*len(edge_list)]
        next_edge = np.random.choice(edge_list, 1, p=probs)[0]
        route.append(next_edge)
        node_index = edge_list.index(next_edge)
    route_id = '>'.join(route)
    if route_id not in route_list:
        route_list.append(route_id)
        traci.route.add(route_id, route)
    return route_id


def add_vehicle(veh_index, route_id):
    traci.vehicle.addFull(vehID='veh{:06}'.format(veh_index), typeID='vehicle', route=route_id)


def step(veh_index, trans_matrix):
    route_id = gen_route(trans_matrix)
    add_vehicle(veh_indx, route_idx)
    traci.simulationStep()


def close():
    traci.close()
    sys.stdout.flush()


if __name__ == '__main__':
    init()
    p_12 = 0.5
    p_13 = 0.5
    p_23 = 0.3
    p_24 = 0.7
    p_35 = 1
    p_54 = 1
    default_trans_matrix = np.array([
        [0.0, p_12, p_13, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, p_23, p_24, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, p_35, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, p_35, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, p_54, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    ]).flatten()

    duration = 3600  # number of steps
    for t in range(duration):
        step(t, default_trans_matrix)

    close()
