from random import random
from numpy.random import normal
from abc import ABC, abstractmethod

class Animal(ABC):
	
	def __init__(self, gender, age, probability_death, probability_birth, movement_speed, hunger, radius):
		self.gender = gender
		self.age = age
		self.probability_death = probability_death
		self.probability_birth = probability_birth
		self.movement_speed = movement_speed
		self.hunger = hunger
		self.radius = radius
		self.radius_sq = self.radius ** 2
		
	@abstractmethod
	def check_death(self, agents, ag, neighbours):
		pass
	
	@abstractmethod
	def check_birth(self, same_neighbours):
		pass