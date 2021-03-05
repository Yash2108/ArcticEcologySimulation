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
	env = np.vstack((np.ones((50, 100)), np.zeros((50, 100))))
	agents = []
	for i in range(PolarBear.initial_population // 2):
		agents.append(PolarBear('m'))
		agents.append(PolarBear('f'))
	for i in range(RingedSeal.initial_population // 2):
		agents.append(RingedSeal('m'))	
		agents.append(RingedSeal('f'))	
		
def observe():
	global env, agents
	cla()
	imshow(env)
	x = {'PolarBear': [], 'RingedSeal': []}
	y = {'PolarBear': [], 'RingedSeal': []}
	for i in agents:
		name = type(i).__name__
		x[name].append(i.x)
		y[name].append(i.y)
	plot(x['PolarBear'], y['PolarBear'], 'ro')
	plot(x['RingedSeal'], y['RingedSeal'], 'yo')
	axis([0, 100, 100, 0])
	title("Ringed Seals: {rs}    Polar Bears: {pb}".format(rs = RingedSeal.count, pb = PolarBear.count))

def restrict(n, movement_speed, min_, max_):
	n = max(min(max_, n), min_)
	if n == 100:
		n -= uniform(0, movement_speed * 10)
	elif n == 0:
		n += uniform(0, movement_speed * 10)
	return n

def update(ag):
	global agents
	name = type(ag).__name__
	neighbours = [nb for nb in agents if type(nb).__name__ != name and 
							  (ag.x - nb.x) ** 2 + (ag.y - nb.y) ** 2 < ag.radius_sq]
	same_neighbours = [nb for nb in agents if type(nb).__name__ == name and 
							  (ag.x - nb.x) ** 2 + (ag.y - nb.y) ** 2 < ag.radius_sq]
	ag.move()
	if ag.check_death(agents, neighbours):
		agents.remove(ag)
		return True
	elif ag.check_birth(agents, same_neighbours):
		agents.append(cp.copy(ag))
	return False
			
def update_one_unit_time():
	global agents
	for ag in agents:
		ag.move()
	i = 0
	while i < len(agents):
		if not update(agents[i]):
			i += 1

if __name__ == "__main__":
	blue = cm.get_cmap('Blues', 4)
	cm.register_cmap(name = 'ice', cmap = ListedColormap([blue(0), blue(1)]))
	matplotlib.rcParams['image.cmap'] = 'ice'
	pycxsimulator.GUI().start(func = [initialize, observe, update_one_unit_time])