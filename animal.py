from random import random, uniform
from numpy.random import normal, randint
from abc import ABC, abstractmethod

class Animal(ABC):
	
	seasons = {'winter': 0, 'spring': 90, 'summer': 180, 'autumn': 270}
	
	def __init__(self, gender, age, probability_death, probability_birth, 
							 movement_speed, hunger, radius, weaning, mating, parents, pregnancy):
		self.gender = gender
		self.age = age
		self.probability_death = probability_death
		self.probability_birth = probability_birth
		self.movement_speed = movement_speed
		self.hunger = hunger
		self.radius = radius
		self.radius_sq = self.radius ** 2
		self.weaning = weaning
		self.mating = mating[gender]
		self.parents = parents
		self.isPregnant=False
		self.daysSpentInPregnancy=None
		self.pregnancy=randint(pregnancy[0], pregnancy[1])
		self.partner=None
		self.children = []
		
	@abstractmethod
	def check_death(self):
		pass
	
	@abstractmethod
	def check_birth(self):
		pass
	
	@abstractmethod
	def move(self):
		pass
	
	def restrict(self, n, min_, max_):
		n = max(min(max_, n), min_)
		if n == 100:
			n -= uniform(0, self.movement_speed * 10)
		elif n == 0:
			n += uniform(0, self.movement_speed * 10)
		return n