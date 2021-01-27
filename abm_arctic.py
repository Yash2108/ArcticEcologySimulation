from matplotlib.colors import ListedColormap
from random import randint, random, uniform
from matplotlib import cm
import pycxsimulator
from pylab import *
import numpy as np
import matplotlib
import copy as cp

matplotlib.use('TkAgg')

class Animal:
	
	def __init__(self, gender, age, probability_death, probability_birth, movement_speed, hunger, radius):
		self.gender = gender
		self.age = age
		self.probability_death = probability_death
		self.probability_birth = probability_birth
		self.movement_speed = movement_speed
		self.hunger = hunger
		self.radius = radius
		self.radius_sq = self.radius ** 2
		self.x = (random() * 100) % 100
		self.y = (random() * 100) % 100
		
class PolarBear(Animal):
	
	count = 0
	
	def __init__(self, gender, age, probability_death, probability_birth, movement_speed, hunger, radius):
		super().__init__(gender, age, probability_death, probability_birth, movement_speed, hunger, radius)
		PolarBear.count += 1
		
class RingedSeal(Animal):
	
	count = 0
	
	def __init__(self, gender, age, probability_death, probability_birth, movement_speed, hunger, radius):
		super().__init__(gender, age, probability_death, probability_birth, movement_speed, hunger, radius)
		RingedSeal.count += 1
		
def initialize():
	global env, agents
	env = np.vstack((np.ones((50, 100)), np.zeros((50, 100))))
	agents = []
	for i in range(polar_bear['init']):
		agents.append(PolarBear('m', 60, polar_bear['death'], polar_bear['birth'], 
														polar_bear['movement'], 0, polar_bear['radius']))
	for i in range(ringed_seal['init']):
		agents.append(RingedSeal('m', 60, ringed_seal['death'], ringed_seal['birth'], 
														ringed_seal['movement'], 0, ringed_seal['radius']))	
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
	axis('image')
	axis([0, 100, 100, 0])
	
def update():
	global agents
	ag = agents[randint(len(agents))]
	ag.x += uniform(-ag.movement_speed, ag.movement_speed)
	ag.y += uniform(-ag.movement_speed, ag.movement_speed)
	if ag.x > 100:
		ag.x = 100
	elif ag.x < 0:
		ag.x = 0
	if ag.y > 100:
		ag.y = 100
	elif ag.y < 0:
		ag.y = 0	
	name = type(ag).__name__
	neighbours = [nb for nb in agents if type(nb).__name__ != name and 
							  (ag.x - nb.x) ** 2 + (ag.y - nb.y) ** 2 < ag.radius_sq]
	if name == 'PolarBear':
		if len(neighbours) == 0 and random() < ag.probability_death:
			agents.remove(ag)
		if random() < ag.probability_birth * ((1 - PolarBear.count) / polar_bear['capacity']):
			agents.append(cp.copy(ag))	
	elif name == 'RingedSeal':
		if len(neighbours) > 0 and random() < ag.probability_death:
			agents.remove(ag)
		if random() < ag.probability_birth * ((1 - RingedSeal.count) / ringed_seal['capacity']):
			agents.append(cp.copy(ag))
			
def update_one_unit_time():
	global agents
	t = 0
	while t < 1:
		t += 1 / len(agents)
		update()

	
polar_bear = {'init': 25, 'movement': 8, 'death': 0.5, 'birth': 0.6, 'radius': 15, 'capacity': 75}
ringed_seal = {'init': 200, 'movement': 5, 'death': 0.3, 'birth': 0.8, 'radius': 10, 'capacity': 600}

if __name__ == "__main__":
	blue = cm.get_cmap('Blues', 4)
	cm.register_cmap(name = 'ice', cmap = ListedColormap([blue(0), blue(1)]))
	matplotlib.rcParams['image.cmap'] = 'ice'
	pycxsimulator.GUI().start(func = [initialize, observe, update_one_unit_time])