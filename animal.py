from random import random, uniform
from numpy.random import normal
from abc import ABC, abstractmethod

class Animal(ABC):
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
		self.daysBeforeBirth=None
		self.pregnancy=pregnancy
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