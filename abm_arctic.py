from matplotlib.colors import ListedColormap
from random import randint, uniform
from ringedseal import RingedSeal
from matplotlib import gridspec
from polarbear import PolarBear
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.cbook import get_sample_data
import pycxsimulator
from pylab import *
import numpy as np
import matplotlib
import copy as cp
import math

matplotlib.use('TkAgg')
spec = gridspec.GridSpec(ncols=2, nrows=1, width_ratios=[3, 1])
cumulative_population = {'PolarBear': [0], 'RingedSeal': [0]}


def initialize():
    global env, agents
    # env = np.vstack((np.zeros((75, 101)), np.ones((26, 101))))
    env = [[None for j in range(100)]for i in range(100)]
    for i in range(100):
        for j in range(100):
            env[i][j] = i
    agents = []
    parents = {
        'm': "Initialized",
        'f': "Initialized"
    }
    for i in range(PolarBear.initial_population // 2):
        agents.append(PolarBear('m', parents))
        agents.append(PolarBear('f', parents))
    for i in range(RingedSeal.initial_population // 2):
        agents.append(RingedSeal('m', parents))
        agents.append(RingedSeal('f', parents))


spec = gridspec.GridSpec(ncols=2, nrows=1, width_ratios=[3, 1])


def observe():
    global env, agents, img_count, day, spec, cumulative_population
    clf()
    fig = gcf()
    img_count += 1
    day = img_count % 365
    if(day > 183 and day < 304):
        parts = 3
    else:
        parts = 1
    day_axis = list(range(img_count + 1))
    blue = cm.get_cmap('Blues', 100)
    cm.register_cmap(name='ice', cmap=ListedColormap(
        [blue(i) for i in range(3)]+[blue(35)]*(parts)))
    matplotlib.rcParams['image.cmap'] = 'ice'
    # 	mng = plt.get_current_fig_manager()
    # 	mng.window.state('zoomed')
    # imshow(env, origin='upper')
    x = {'PolarBear': [], 'RingedSeal': [], 'PolarBear_child': [],
         'RingedSeal_child': [], 'PolarBearPregnant': [], 'RingedSealPregnant': []}
    y = {'PolarBear': [], 'RingedSeal': [], 'PolarBear_child': [],
         'RingedSeal_child': [], 'PolarBearPregnant': [], 'RingedSealPregnant': []}
    ratio = RingedSeal.count/PolarBear.count
    cumulative_population['RingedSeal'].append(RingedSeal.count)
    cumulative_population['PolarBear'].append(PolarBear.count)
    for i in agents:
        name = type(i).__name__
        if i.isPregnant:
            x[name+'Pregnant'].append(i.x)
            y[name+'Pregnant'].append(i.y)
        elif i.age > i.weaning:
            x[name].append(i.x)
            y[name].append(i.y)
        else:
            x[name + '_child'].append(i.x)
            y[name + '_child'].append(i.y)
    ax1 = fig.add_subplot(spec[0], label="1")
    ax0 = fig.add_subplot(spec[0], label="1", frame_on=False)
    ax2 = fig.add_subplot(spec[1], label="3")
    ax3 = fig.add_subplot(spec[1], label="4", frame_on=False)
    # ax4 = fig.add_subplot(spec[1], label="4", frame_on = False)
    ax1.imshow(env, origin='lower')
    # ax1.set_axis_off()
    ax0.set_axis_off()
    ax1.set_aspect(0.84)
    ax0.plot(x['PolarBear'], y['PolarBear'], 'ro', markersize=8)
    ax0.plot(x['RingedSeal'], y['RingedSeal'], 'yo', markersize=6)
    ax0.plot(x['PolarBear_child'], y['PolarBear_child'], 'ro', markersize=3)
    ax0.plot(x['RingedSeal_child'], y['RingedSeal_child'], 'yo', markersize=3)
    ax0.plot(x['PolarBearPregnant'],
             y['PolarBearPregnant'], 'r^', markersize=8)
    ax0.plot(x['RingedSealPregnant'],
             y['RingedSealPregnant'], 'y^', markersize=6)
    ax0.axis([0, 100, 0, 100])
    ax0.set_title("Step: {st}  Day: {dy}  Ringed Seals: {rs}  Polar Bears: {pb}  Population Ratio: {pr}".format(
        rs=RingedSeal.count, pb=PolarBear.count, st=img_count, pr=ratio, dy=day))
    ax0.set_aspect(0.84)
    l2, = ax2.plot(
        day_axis, cumulative_population['RingedSeal'], color="C1", label="Ringed Seals")
    ax2.tick_params(axis='x', colors="C1")
    ax2.tick_params(axis='y', colors="C1", pad=5)
    ax2.set_xlabel("Day Number")
    ax2.set_ylabel("Ringed Seals")

    l3, = ax3.plot(
        day_axis, cumulative_population['PolarBear'], color="C0", label="Polar Bears")
    ax3.tick_params(axis='x', colors="C0")
    ax3.tick_params(axis='y', colors="C0")
    ax3.yaxis.tick_right()
    ax3.set_xlabel("Day Number")
    ax3.set_ylabel("Polar Bear")
    ax3.yaxis.set_label_position('right')

    ax2.legend([l2, l3], ['Ringed Seals', "Polar Bear"], loc="lower right")
    plt.subplots_adjust(right=0.95)

    # # print(ax0.get_position())
    # pos = ax0.get_position()
    # ax1.set_position([pos.x0 - 0.2, pos.y0, 1, 1])


def update(ag):
    global agents
    name = type(ag).__name__
    neighbours = [nb for nb in agents if type(nb).__name__ != name and
                  (ag.x - nb.x) ** 2 + (ag.y - nb.y) ** 2 < ag.radius_sq]
    same_neighbours = [nb for nb in agents if type(nb).__name__ == name and
                       (ag.x - nb.x) ** 2 + (ag.y - nb.y) ** 2 < ag.radius_sq]
    deaths = ag.check_death(agents, neighbours)
    if deaths != False:
        for death in deaths:
            agents.remove(death)
        return True
    if not ag.isPregnant:
        ag.check_birth(agents, same_neighbours, day)
    else:
        if ag.daysSpentInPregnancy < ag.pregnancy:
            ag.daysSpentInPregnancy += 1
        else:
            childrenList = ag.give_birth(ag.partner)
            for i in childrenList:
                agents.append(i)
            ag.partner = None
            ag.daysSpentInPregnancy = None

    ag.age += 1
    if type(ag).__name__ == "PolarBear" and not ag.isPregnant:
        if 180 <= day <= 300:
            ag.hunger += 0.01
            ag.probability_death += ((ag.hunger) + (ag.age)/1000)
        else:
            ag.hunger += 0.1
            ag.probability_death += ((ag.hunger) + (ag.age)/1000)
        # print(img_count, ag.hunger)

        if type(ag).__name__ == "PolarBear" and ag.age >= 9125:
            ag.probability_death = 0.8
    return False


def update_one_unit_time():
    global agents, days
    for ag in agents:
        ag.move(agents, day)

    i = 0
    while i < len(agents):
        if not update(agents[i]):
            i += 1


if __name__ == "__main__":
    img_count = 0
    day = 0
    blue = cm.get_cmap('Blues', 100)
    cm.register_cmap(name='ice', cmap=ListedColormap(
        [blue(i) for i in range(3)]+[blue(35)]))
    matplotlib.rcParams['image.cmap'] = 'ice'
    pycxsimulator.GUI().start(func=[initialize, observe, update_one_unit_time])
