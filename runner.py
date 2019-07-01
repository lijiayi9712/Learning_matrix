#!/usr/bin/env python
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2009-2019 German Aerospace Center (DLR) and others.
# This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v20.html
# SPDX-License-Identifier: EPL-2.0

# @file    runner.py
# @author  Lena Kalleske
# @author  Daniel Krajzewicz
# @author  Michael Behrisch
# @author  Jakob Erdmann
# @date    2009-03-26
# @version $Id$

from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import random
import numpy as np
transition = np.array([0 0 0 0 0 0 0; 0.3 0 0 0 0 0 0; 0.7 0 0 0 0 0 0; 0 0.6 0 0 0 0 0; 0 0.4 0 0 0 0 0; 0 0 1 1 0 0 0; 0 0 0 0 1 1 0])
transition =  np.transpose(transition)

# we need to import python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  # noqa
import traci  # noqa
import sumolib

# parse the net
net = sumolib.net.readNet('data/sample.net.xml')
nodes = net.getNodes()
edges = net.getEdges()
# retrieve the coordinate of a node based on its ID

lane = {}   #dict mapping each node to the list of edges pointing out of the node
for node in nodes:
    connections = node.getConnections()
    lane[node.getID()] = []
    for connection in connections:
        to_edge = connection.getTo()
        #node_across_edge = node.getID()].append(to_edge.getToNode()
        lane[node.getID()].append(to_edge)

edge_index = {} # assign each edge an index s.t we can name each edge a separate route with proper naming index.

for i, edge in enumerate(edges):
    edge_index{edge} = i


def generate_routefile():
    random.seed(42)  # make tests reproducible
    N = 3600  # number of time steps
    # demand per second from different directions
    # pWE = 1. / 10
    # pEW = 1. / 11
    # pNS = 1. / 30
    p_0 = 0.25
    p_1 = 0.5
    p_2 = 1
    with open("data/sample1.rou.xml", "w") as routes:
        print("""<routes>
        <vType id="typeWE" accel="0.8" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="16.67" \
guiShape="passenger"/>
        <vType id="typeNS" accel="0.8" decel="4.5" sigma="0.5" length="7" minGap="3" maxSpeed="25" guiShape="bus"/>
        """, file=routes)
        print("<route id=route00 edges=in_to1 />", file=routes)
        for (edge, index) in edge_index:
            print("<route id=route" + str(index) + " edges="+ str(edge.getID()) +'/>', file=routes)
        print("</routes>", file=routes)


import geopy.distance

def add_vehicle(veh_index):
    """
    Add a vehicle to the network from the source of the network
    """
    #current_veh = traci.vehicle.getIDList()
    traci.vehicle.addFull(vehID="veh" + str(veh_index), typeID="typeNS", route='route00')

def check_end(veh):
    coords_1 = veh.getPosition()
    edge_id = veh.getRoadID()
    next_node = net.getEdge(edge_id).getToNode()
    coords_2 = next_node.getCoord()
    distance = geopy.distance.vincenty(coords_1, coords_2).m    #getDistance2D(x1, y1, x2, y2, isGeo=False, isDriving=False)
    if distance < 0.5:
        return True
    return False

#def closest_node(veh_id):




def run():
    """execute the TraCI control loop"""
    random.seed(42)  # make tests reproducible
    N = 3600  # number of time steps
    step = 0
    # we start with phase 2 where EW has green
    #traci.trafficlight.setPhase("0", 2)
    For i in range(N):
        random_num = random.uniform(0, 1)
    #while traci.simulation.getMinExpectedNumber() > 0:
        add_vehicle(i)
        traci.simulationStep()
        for veh in traci.getIDList():
            if check_end(veh):
                ###
                if random_num is in []:   #the range for each route 
                    traci.changeTarget(veh.getID(), )

        step += 1
    traci.close()
    sys.stdout.flush()


def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options


# this is the main entry point of this script
if __name__ == "__main__":
    options = get_options()

    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # first, generate the route file for this simulation
    generate_routefile()

    # this is the normal way of using traci. sumo is started as a
    # subprocess and then the python script connects and runs
    traci.start([sumoBinary, "-c", "data/sample.sumocfg",
                             "--tripinfo-output", "tripinfo.xml"])
    run()
