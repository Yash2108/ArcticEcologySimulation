from animal import Animal
from random import random, uniform, choice
from numpy.random import normal
import numpy as np

class PolarBear(Animal):
	
	count = 0
	initial_population = 8
	capacity = 16
	
	def __init__(self, gender, parents, age = 2555, hunger=0.1):
		super().__init__(gender = gender, 
										 age = age, 
										 probability_death = 0.1 * hunger, 
										 probability_birth = 0.1, 
										 movement_speed = 10, 
										 hunger = hunger, 
										 radius = 30, 
										 weaning = 912.5, 
										 mating = {'m': 1825, 'f': 1460}, 
										 parents = parents,
										 pregnancy=[195, 265]
										 )
		self.x = uniform(0, 100)
		self.y = uniform(20, 40)
		self.uid = PolarBear.count
		PolarBear.count += 1
		
	def check_death(self, agents, neighbours):
		if len(neighbours) == 0 and random() < self.probability_death and self.age > self.weaning:
			deaths = []
			deaths.append(self)
			PolarBear.count -= 1
			for child in self.children:
				if child.age < child.weaning:
					deaths.append(child)
					PolarBear.count -= 1
			return deaths
		return False
			
	def give_birth(self, chosen):
		if self.gender == 'f':
			female = self
			male = chosen
		else:
			female = chosen
			male = self
		parents = {
			'f': female,
			'm': male
		}
		child = PolarBear(choice(['f', 'm']), parents, 0)
		self.children.append(child)
		return child
	
	def check_birth(self, agents, same_neighbours):
		if self.age > self.mating:
			if len(same_neighbours) > 0 and random() < self.probability_birth * (1 - PolarBear.count / PolarBear.capacity):
				opp_gender = [ag for ag in same_neighbours if ag.gender != self.gender]
				if len(opp_gender) == 0:
					return False
				chosen = choice(opp_gender)
				self.partner=chosen
				self.daysSpentInPregnancy=0
				return True
		return False
				
	def move(self, agents, day):
		if self.age > self.weaning:
			name = 'PolarBear'
			neighbours_vector = []
			neighbours_dist = []
			for nb in agents:
				if type(nb).__name__ != name:
					neighbours_vector.append([nb.x - self.x, nb.y - self.y])
					neighbours_dist.append(neighbours_vector[-1][0] ** 2 + neighbours_vector[-1][1] ** 2)
					if neighbours_dist[-1] >= self.radius_sq:
						neighbours_vector.pop(-1)
						neighbours_dist.pop(-1)
			if len(neighbours_vector) > 0:
				neighbours_vector = np.array(neighbours_vector)
				neigbours_dist = np.array(neighbours_dist)
				for i in range(len(neighbours_vector)):
					neighbours_vector[i] = (neighbours_vector[i] * self.movement_speed * 
																 (1 - neighbours_dist[i] / self.radius_sq)) / (neighbours_dist[i] ** 0.5)	 
				final_vector = np.sum(neighbours_vector, axis = 0) / len(neighbours_vector)
				self.x += final_vector[0]
				self.y += final_vector[1]
			if day > self.seasons['summer']:
				self.x += uniform(-self.movement_speed // 2, self.movement_speed // 2)
				self.y -= uniform(0, self.movement_speed // 2)				
			elif len(neighbours_vector) == 0:
	 			self.x += uniform(-self.movement_speed, self.movement_speed)
	 			self.y += uniform(-self.movement_speed, self.movement_speed)
			self.x = self.restrict(self.x, 0, 100)
			self.y = self.restrict(self.y, 0, 100)
		else:
			self.x = self.parents['f'].x + uniform(-2, 2)
			self.y = self.parents['f'].y + uniform(-2, 2)
