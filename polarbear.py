from animal import Animal
from random import random, uniform
from numpy.random import normal

class PolarBear(Animal):
	
	count = 0
	initial_population = 4
	capacity = 8
	
	#gender, age, probability_death, probability_birth, movement_speed, hunger, radius
	def __init__(self, gender):
		self.x = uniform(0, 100)
		self.y = uniform(60, 80)
		super().__init__(gender, 60, 0.1, 0.1, 10, 0, 30)
		PolarBear.count += 1
		
	def check_death(self, agents, neighbours):
		if len(neighbours) == 0 and random() < self.probability_death:
			PolarBear.count -= 1
			return True
		return False
			
	def check_birth(self, agents, same_neighbours):
		if len(same_neighbours) > 0 and random() < self.probability_birth * (1 - PolarBear.count / PolarBear.capacity):
			for nb in same_neighbours:
				if nb.gender != self.gender:
					PolarBear.count += 1
					return True
		return False
				
	def move(self):
		self.x = self.restrict(self.x + uniform(-self.movement_speed, self.movement_speed), 0, 100)
		self.y = self.restrict(self.y + uniform(-self.movement_speed, self.movement_speed), 0, 100)