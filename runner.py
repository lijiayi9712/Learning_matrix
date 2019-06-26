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

# we need to import python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  # noqa
import traci  # noqa


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

        <route id="route0" edges="1to2 2toh1 h1toh2 h2to4" />
        
        <route id="route1" edges="1to2 2to4" />

        <route id="route2" edges="1to3 3toh2 h2to4" />
        
        """, file=routes)
        # <route id="route0" edges="1to2 2toh1 h1toh2 h2to4 4to_out" />
        
        # <route id="route1" edges="1to2 2to4 4to_out" />

        # <route id="route2" edges="1to3 3toh2 h2to4 4to_out" />
        # <route id="route0" edges="1to2 2to4 4to_out" />
        
        # <route id="route1" edges="1to2 2to3 3to4 4to_out" />

        # <route id="route2" edges="1to3 3to4 4to_out" /> 

        vehNr = 0
        for i in range(N):
            rand_num = random.uniform(0, 1)
            if rand_num < p_0:
                print('    <vehicle id="route0_%i" type="typeNS" route="route0" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if rand_num >= p_0 and rand_num < p_1:
                print('    <vehicle id="route1_%i" type="typeNS" route="route1" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if rand_num >= p_1:
                print('    <vehicle id="route2_%i" type="typeNS" route="route2" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
        print("</routes>", file=routes)

# The program looks like this
#    <tlLogic id="0" type="static" programID="0" offset="0">
# the locations of the tls are      NESW
#        <phase duration="31" state="GrGr"/>
#        <phase duration="6"  state="yryr"/>
#        <phase duration="31" state="rGrG"/>
#        <phase duration="6"  state="ryry"/>
#    </tlLogic>


def run():
    """execute the TraCI control loop"""
    step = 0
    # we start with phase 2 where EW has green
    #traci.trafficlight.setPhase("0", 2)
    while traci.simulation.getMinExpectedNumber() > 0:
        # traci.vehicle.addFull(...)
        traci.simulationStep()
        # if traci.trafficlight.getPhase("0") == 2:
        #     # we are not already switching
        #     if traci.inductionloop.getLastStepVehicleNumber("0") > 0:
        #         # there is a vehicle from the north, switch
        #         traci.trafficlight.setPhase("0", 3)
        #     else:
        #         # otherwise try to keep green for EW
        #         traci.trafficlight.setPhase("0", 2)

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
