from matplotlib.colors import ListedColormap
from random import randint, uniform
from ringedseal import RingedSeal
from polarbear import PolarBear
from matplotlib import cm
import pycxsimulator
from pylab import *
import numpy as np
import matplotlib
import copy as cp

matplotlib.use('TkAgg')
def initialize():
	global env, agents
	env = np.vstack((np.zeros((75, 101)), np.ones((26, 101))))
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
	global env, agents, img_count, day
	cla()
	img_count += 1
	day = img_count % 365
# 	mng = plt.get_current_fig_manager()
# 	mng.window.state('zoomed')
	imshow(env, origin = 'upper')
	x = {'PolarBear': [], 'RingedSeal': [], 'PolarBear_child': [], 'RingedSeal_child': []}
	y = {'PolarBear': [], 'RingedSeal': [], 'PolarBear_child': [], 'RingedSeal_child': []}
	for i in agents:
		name = type(i).__name__
		if i.age > i.weaning:
			x[name].append(i.x)
			y[name].append(i.y)
		else:
			x[name + '_child'].append(i.x)
			y[name + '_child'].append(i.y)			
	plot(x['PolarBear'], y['PolarBear'], 'ro', markersize = 8)
	plot(x['RingedSeal'], y['RingedSeal'], 'yo', markersize = 6)
	plot(x['PolarBear_child'], y['PolarBear_child'], 'ro', markersize = 3)
	plot(x['RingedSeal_child'], y['RingedSeal_child'], 'yo', markersize = 3)
	axis([0, 100, 0, 100])
	title("Step: {st}    Ringed Seals: {rs}    Polar Bears: {pb}".format(rs = RingedSeal.count, pb = PolarBear.count, st = img_count))

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
		ag.check_birth(agents, same_neighbours)
	else:
		if ag.daysSpentInPregnancy<ag.pregnancy:
			ag.daysSpentInPregnancy+=1
		else:
			child=ag.give_birth(ag.partner)
			agents.append(child)
			ag.partner=None
			ag.daysSpentInPregnancy=None

	ag.age += 1
	if type(ag).__name__ == "PolarBear" and not ag.isPregnant:
		ag.hunger += 0.1
		ag.probability_death = 0.1 * ag.hunger
	return False
			
def update_one_unit_time():
	global agents
	for ag in agents:
		if not ag.isPregnant:
			ag.move(agents, day)
	i = 0
	while i < len(agents):
		if not update(agents[i]):
			i += 1

if __name__ == "__main__":
	img_count = 0
	day = 0
	blue = cm.get_cmap('Blues', 4)
	cm.register_cmap(name = 'ice', cmap = ListedColormap([blue(0), blue(1)]))
	matplotlib.rcParams['image.cmap'] = 'ice'
	pycxsimulator.GUI().start(func = [initialize, observe, update_one_unit_time])