import subprocess
import numpy as np
np.random.seed(42)  # make tests reproducible (TODO: check if this is indeed effective)

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit('please declare environment variable "SUMO_HOME"')

from sumolib import checkBinary
import traci
import sumolib

route_dict = {}

def init():
    netconvert_cmd = [
        'netconvert',
        '--node-files=data/diamond.nod.xml',
        '--edge-files=data/diamond.edg.xml',
        '--type-files=data/diamond.type.xml',
        '--output-file=data/diamond.net.xml'
    ]
    subprocess.run(netconvert_cmd)
    sumoBinary = checkBinary('sumo-gui')
    traci.start([
        sumoBinary,
        '-c', 'data/diamond.sumocfg',
        '--tripinfo-output', 'data/tripinfo.xml'
    ])


def gen_route(trans_matrix):
    route = None #TODO generate a route from transition matrix
    if route is not in route_dict:
        route_id = route.join('>')
        route_dict[route] = route_id
        traci.route.add(route_id, route)
    return route_dict[route]


def add_vehicle(veh_index, route_id):
    traci.vehicle.addFull(vehID='veh{:06}'.format(veh_index), typeID='vehicle', route=route_id)


def step(veh_index, trans_matrix)
    route_id = gen_route(trans_matrix)
    add_vehicle(veh_indx, route_idx)
    traci.simulationStep()


def close():
    traci.close()
    sys.stdout.flush()


if __name__ == '__main__':
    init()
    default_trans_matrix = np.array([
        0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0;
        0.0, 0.0, 0.3, 0.7, 0.0, 0.0, 0.0;
        0.0, 0.0, 0.0, 0.0, 0.6, 0.4, 0.0;
        0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0;
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0;
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    ]).flatten()

    duration = 3600  # number of steps
    for t in range(duration):
        step(t, default_trans_matrix)

    close()
