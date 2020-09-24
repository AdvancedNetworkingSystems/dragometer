#!/usr/bin/env python

import os
import sys
import csv

from utils import add_platooning_vehicle, start_sumo, running

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

import traci
from plexe import Plexe, ACC, CACC, SPEED, ACCELERATION, RADAR_DISTANCE

from dragometer.dragometer import Dragometer

# target inter-vehicle gap
GAP = 1
# initial cruising speed
CRUISING_SPEED = 130 / 3.6

fieldnames = ['nodeId', 'time', 'acceleration', 'speed', 'distance', 'cd', 'battery', 'energy']


def log_data(csv, position, time, acc, speed, distance, cd, battery, energy):
    csv.writerow({
        "nodeId": position,
        "time": time,
        "acceleration": acc,
        "speed": speed,
        "distance": distance,
        "cd": cd,
        "battery": battery,
        "energy": energy
    })


def add_vehicles(plexe: Plexe, names: list, gaps: list, has_slipstream_device: list):
    # The example uses only a vehicle type, called "car"
    # (see cfg/freeway.rou.xml), which has a length of 4.971 m.
    length = 4.971

    # To avoid interferences, vehicles must be added from the first to the last.
    for i in range(len(names)):
        add_platooning_vehicle(plexe, names[i], sum(gaps[i:]) + (len(names) - i) * length, 0,
                               CRUISING_SPEED, GAP, False, vtype='car')
        traci.vehicle.setSpeedMode(names[i], 0)
        plexe.set_fixed_lane(names[i], 0, safe=False)
        plexe.use_controller_acceleration(names[i], False)
        if i == 0:
            plexe.set_active_controller(names[i], ACC)
        else:
            plexe.set_active_controller(names[i], CACC)
            plexe.enable_auto_feed(names[i], True, names[0], names[i - 1])
        if has_slipstream_device[i]:
            traci.vehicle.setParameter(names[i], 'has.slipstream.device', 'true')


def run_simulation(api: Dragometer, fileName: str,
                   names: list, gaps: list, has_slipstream_device: list, track: int,
                   use_gui: False):
    """
    :param names: The names of the vehicles, ordered from the first to the last.
    :param gaps: The initial inter-vehicle gaps. The first is the gap between the first and the second vehicle.
    :param has_slipstream_device: Whether to equip each vehicles with the slipstream device.
    """
    assert len(names) >= 2
    assert len(gaps) == len(names) - 1
    assert len(names) == len(has_slipstream_device)
    if True in has_slipstream_device:
        assert has_slipstream_device[names.index(track)]

    start_sumo("cfg/freeway.sumo.cfg", False, use_gui)
    plexe = Plexe()
    traci.addStepListener(plexe)

    outfile = open(fileName, "w")
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    step = 0
    while running(False, step, 4000):
        traci.simulationStep()
        if step == 0:
            add_vehicles(plexe, names, gaps, has_slipstream_device)
            if use_gui:
                traci.gui.trackVehicle("View #0", 'v0')
                traci.gui.setZoom("View #0", 100000)
        else:
            # The example uses only a vehicle type, called "car"
            # (see cfg/freeway.rou.xml), which has a drag coefficient of 0.24
            cd = 0.24
            if True in has_slipstream_device:
                cd = traci.vehicle.getParameter(track, 'device.slipstream.actualDragCoefficient')
            charge = traci.vehicle.getParameter(track, 'device.battery.actualBatteryCapacity')
            if api is not None:
                if True not in has_slipstream_device:
                    api.plot('1', step, float(cd), subplotIndex=0)
                    api.plot('2', step, float(charge), subplotIndex=0)
                else:
                    api.plot('1', step, float(cd), subplotIndex=1)
                    api.plot('2', step, float(charge), subplotIndex=1)
            energy = traci.vehicle.getParameter(track, 'device.battery.energyConsumed')
            data = plexe.get_vehicle_data(track)
            radar = plexe.get_radar_data(track)
            log_data(writer, 1, step, data[ACCELERATION], data[SPEED], radar[RADAR_DISTANCE], cd, charge, energy)
        step += 1

    traci.close()


def main(api: Dragometer = None):
    if api is not None:
        api.add_plot('1')
        api.set_x_max('1', 4000)
        # api.set_y_max('1', 0.30)
        # api.set_y_min('1', 0.20)
        api.set_subplots('1', 2)
        api.set_title('1', 'Vehicle 1')
        api.set_x_axis_title('1', 'Timestep')
        api.set_y_axis_title('1', 'Drag coefficient')

        api.add_plot('2')
        api.set_x_max('2', 4000)
        # api.set_y_max('2', 43000)
        # api.set_y_min('2', 41000)
        api.set_subplots('2', 2)
        api.set_title('2', 'Vehicle 1')
        api.set_x_axis_title('2', 'Timestep')
        api.set_y_axis_title('2', 'Battery capacity (Wh)')

    names = ['v0', 'v1', 'v2', 'v3']
    gaps = [10, 15, 20]
    track = 'v1'

    print('Run simulation without device')
    run_simulation(api, 'nodrag.csv', names, gaps, [False, False, False, False], track, False)
    print('Run simulation with device')
    run_simulation(api, 'withdrag.csv', names, gaps, [False, True, False, False], track, True)

    if __name__ == "__main__":
        main()
