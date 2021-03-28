from animal import Animal
from random import random, uniform, choice
from numpy.random import normal
import numpy as np

class PolarBear(Animal):
	
	count = 0
	initial_population = 8
	capacity = 16
	
	#gender, age, probability_death, probability_birth, movement_speed, hunger, radius
	def __init__(self, gender, parents):
		self.x = uniform(0, 100)
		self.y = uniform(60, 80)
		super().__init__(gender, 0, 0.1, 0.1, 10, 0, 30, 912.5, {'m': 1825, 'f': 1460}, parents)
		self.uid = PolarBear.count
		PolarBear.count += 1
		
	def check_death(self, agents, neighbours):
		if len(neighbours) == 0 and random() < self.probability_death:
			PolarBear.count -= 1
			return True
		return False
			
	def check_birth(self, agents, same_neighbours):
		if self.age>self.mating:
			if len(same_neighbours) > 0 and random() < self.probability_birth * (1 - PolarBear.count / PolarBear.capacity):
				opp_gender=[ag for ag in same_neighbours if ag.gender!=self.gender]
				# for nb in same_neighbours: 
				# 	if nb.gender != self.gender:
				if len(opp_gender)==0:
					return False
				chosen=choice(opp_gender)
				female= self if self.gender=='f' else chosen
				xy=PolarBear
				PolarBear.count += 1
				return True
			return False
		return False
				
	def move(self, agents):
		name = 'PolarBear'
		neighbours_vector = []
		neighbours_dist = []
		for nb in agents:
			if type(nb).__name__ != name:
				neighbours_vector.append([self.x - nb.x, self.y - nb.y])
				neighbours_dist.append(neighbours_vector[-1][0] ** 2 + neighbours_vector[-1][1] ** 2)
				if neighbours_dist[-1] >= self.radius_sq:
					neighbours_vector.pop(-1)
					neighbours_dist.pop(-1)
		if len(neighbours_vector) > 0:
			neighbours_vector = np.array(neighbours_vector)
			neigbours_dist = np.array(neighbours_dist)
			for i in range(len(neighbours_vector)):
				neighbours_vector[i] = (neighbours_vector[i] * self.movement_speed) / neighbours_dist[i]
# 				neighbours_vector[i] = (neighbours_vector[i] * self.movement_speed ** 0.5)
			print(neighbours_vector)
			self.x, self.y = np.sum(neighbours_vector, axis = 0)
		else:
			self.x += uniform(-self.movement_speed, self.movement_speed)
			self.y += uniform(-self.movement_speed, self.movement_speed)
		self.x = self.restrict(self.x, 0, 100)
		self.y = self.restrict(self.y, 0, 100)

# 		same_neighbours = [nb for nb in agents if type(nb).__name__ == name and 
# 										   (self.x - nb.x) ** 2 + (self.y - nb.y) ** 2 < self.radius_sq]
# 		self.x = self.restrict(self.x + uniform(-self.movement_speed, self.movement_speed), 0, 100)
# 		self.y = self.restrict(self.y + uniform(-self.movement_speed, self.movement_speed), 0, 100)