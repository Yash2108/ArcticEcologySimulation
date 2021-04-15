from matplotlib.colors import ListedColormap
from random import randint, uniform
from ringedseal import RingedSeal
from polarbear import PolarBear
from matplotlib import cm
import pycxsimulator
from pylab import *
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import gridspec
import copy as cp

matplotlib.use('TkAgg')

def initialize():
	global env, agents
	env = np.vstack((np.zeros((75, 201)), np.ones((26, 201))))
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
		
def observe():
	global env, agents
	clf()
	fig = gcf()
	spec = gridspec.GridSpec(ncols=2, nrows=1, width_ratios=[4, 1])
	ax0 = fig.add_subplot(spec[0])
	ax1 = fig.add_subplot(spec[1])
	ax0.imshow(env, origin = 'upper')
	x = {'PolarBear': [], 'RingedSeal': []}
	y = {'PolarBear': [], 'RingedSeal': []}
	for i in agents:
		name = type(i).__name__
		x[name].append(i.x)
		y[name].append(i.y)
	ax0.plot(x['PolarBear'], y['PolarBear'], 'ro', markersize = 8)
	ax0.plot(x['RingedSeal'], y['RingedSeal'], 'yo')
	ax0.axis([0, 200, 0, 100])
	ax0.set_title("Ringed Seals: {rs}    Polar Bears: {pb}".format(rs = RingedSeal.count, pb = PolarBear.count))
	mng = plt.get_current_fig_manager()
	mng.window.state('zoomed')	
	

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
	child = ag.check_birth(agents, same_neighbours)
	if child != False:
		agents.append(child)
	ag.age += 1
	return False
			
def update_one_unit_time():
	global agents
	for ag in agents:
		ag.move(agents)
	i = 0
	while i < len(agents):
		if not update(agents[i]):
			i += 1

if __name__ == "__main__":
# 	global fig, axs
# 	fig, axs = plt.subplots(1, 2, gridspec_kw={'width_ratios': [5, 1]})
	blue = cm.get_cmap('Blues', 4)
	cm.register_cmap(name = 'ice', cmap = ListedColormap([blue(0), blue(1)]))
	matplotlib.rcParams['image.cmap'] = 'ice'
	pycxsimulator.GUI().start(func = [initialize, observe, update_one_unit_time])