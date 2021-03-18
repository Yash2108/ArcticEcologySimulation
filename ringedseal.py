from animal import Animal
from random import random, uniform
from numpy.random import exponential

class RingedSeal(Animal):
	
	count = 0
	initial_population = 400
	capacity = 600
	
	#gender, age, probability_death, probability_birth, movement_speed, hunger, radius
	def __init__(self, gender):
		self.x = uniform(0, 100)
		self.y = exponential(2) * 15
		super().__init__(gender, 0, 0.15, 0.3, 0.5, 0, 30)
		RingedSeal.count += 1
		
	def check_death(self, agents, neighbours):
		if len(neighbours) > 0 and random() < self.probability_death:
			RingedSeal.count -= 1
			return True
		return False
			
	def check_birth(self, agents, same_neighbours):
		if len(same_neighbours) > 0 and random() < self.probability_birth * (1 - RingedSeal.count / RingedSeal.capacity):
			for nb in same_neighbours:
				if nb.gender != self.gender:
					RingedSeal.count += 1
					return True
		return False
				
	def move(self, agents):
		self.x = self.restrict(self.x + uniform(-self.movement_speed, self.movement_speed), 0, 100)
		self.y = self.restrict(self.y + uniform(-self.movement_speed, self.movement_speed), 0, 100)
