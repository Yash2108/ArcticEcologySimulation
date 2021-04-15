from animal import Animal
from random import random, uniform, choice
from numpy.random import normal
import numpy as np

class Walrus(Animal):
	
	count = 0
	initial_population = 4
	capacity = 8
	
	#gender, age, probability_death, probability_birth, movement_speed, hunger, radius, weaning, mating, parents
	def __init__(self, gender, parents, age = 2555):
		self.x = uniform(0, 200)
		self.y = uniform(20, 40)
		super().__init__(gender, age, 0.1, 0.1, 10, 0, 30, 912.5, {'m': 1825, 'f': 1460}, parents)
		self.uid = Walrus.count
		Walrus.count += 1
		
	def check_death(self, agents, neighbours):
		pbs=[]
		for i in neighbours:
			if i.__name__=="PolarBear":
				pbs.append(i)
		if len(pbs) == 0 and random() < self.probability_death and self.age > self.weaning:
			deaths = []
			deaths.append(self)
			Walrus.count -= 1
			if len(self.children)!=0:
				for child in self.children:
					if child.age < child.weaning:
						deaths.append(child)
						Walrus.count -= 1
				return deaths
			return True
		return False
			
	def give_birth(self, female, male):
		parents = {
			'f': female,
			'm': male
		}
		child = Walrus(choice(['f', 'm']), parents, 0)
		self.children.append(child)
		return child
	
	def check_birth(self, agents, same_neighbours):
		if self.age > self.mating:
			if len(same_neighbours) > 0 and random() < self.probability_birth * (1 - Walrus.count / Walrus.capacity):
				opp_gender = [ag for ag in same_neighbours if ag.gender != self.gender]
				if len(opp_gender) == 0:
					return False
				chosen = choice(opp_gender)
				if self.gender == 'f':
					female = self
					male = chosen
				else:
					female = chosen
					male = self
				return self.give_birth(female, male)
		return False
				
	def move(self, agents):
		if self.age > self.weaning:
	 		name = 'Walrus'
	 		neighbours_vector = []
	 		neighbours_dist = []
	 		for nb in agents:
	 			if type(nb).__name__ == 'PolarBear':
	 				neighbours_vector.append([nb.x - self.x, nb.y - self.y])
	 				neighbours_dist.append(neighbours_vector[-1][0] ** 2 + neighbours_vector[-1][1] ** 2)
	 				if neighbours_dist[-1] >= self.radius_sq:
	 					neighbours_vector.pop(-1)
	 					neighbours_dist.pop(-1)
	 		if len(neighbours_vector) > 0:
	 			neighbours_vector = np.array(neighbours_vector)
	 			neigbours_dist = np.array(neighbours_dist)
	 			for i in range(len(neighbours_vector)):
	 				neighbours_vector[i] = (neighbours_vector[i] * self.movement_speed * self.radius_sq) / (neighbours_dist[i] ** 0.5 * neighbours_dist[i])
	# 				neighbours_vector[i] = (neighbours_vector[i] * self.movement_speed ** 0.5)
	 			self.x, self.y = np.sum(neighbours_vector, axis = 0)
	 		else:
	 			self.x += uniform(-self.movement_speed, self.movement_speed)
	 			self.y += uniform(-self.movement_speed, self.movement_speed)
	 		self.x = self.restrict(self.x, 0, 200)
	 		self.y = self.restrict(self.y, 0, 100)
		else:
			self.x = self.parents['f'].x
			self.y = self.parents['f'].y