import copy as cp
from animal import Animal
import random as rd
from numpy.random import normal

class PolarBear(Animal):
	
	count = 0
	initial_population = 4
	capacity = 8
	
	#gender, age, probability_death, probability_birth, movement_speed, hunger, radius
	def __init__(self, gender):
		self.x = rd.uniform(0, 100)
		self.y = rd.uniform(60, 80)
		super().__init__(gender, 60, 0.1, 0.1, 10, 0, 30)
		PolarBear.count += 1
		
	def check_death(self, agents, neighbours):
		if len(neighbours) == 0 and rd.random() < self.probability_death:
			agents.remove(self)
			PolarBear.count -= 1
			
	def check_birth(self, agents, same_neighbours):
		if len(same_neighbours) > 0 and rd.random() < self.probability_birth * (1 - PolarBear.count / PolarBear.capacity):
			for nb in same_neighbours:
				if nb.gender != self.gender:
					agents.append(cp.copy(self))
					PolarBear.count += 1
					break