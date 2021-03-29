from animal import Animal
from random import random, uniform, choice
from numpy.random import exponential

class RingedSeal(Animal):
	
	count = 0
	initial_population = 400
	capacity = 600
	
	#gender, age, probability_death, probability_birth, movement_speed, hunger, radius
	def __init__(self, gender, parents, age = 2555):
		super().__init__(gender, 2555, 0.15, 0.3, 0.5, 0, 30, 42, {'m': 1825, 'f': 1095}, parents)
		self.x = uniform(0, 100)
		self.y = self.restrict(100 - exponential(1.95) * 15, 0, 100)
		self.uid=RingedSeal.count
		RingedSeal.count += 1
		
	def check_death(self, agents, neighbours):
		if len(neighbours) > 0 and random() < self.probability_death and self.age > self.weaning:
			deaths = []
			deaths.append(self)
			RingedSeal.count -= 1
			for child in self.children:
				if child.age < child.weaning:
					deaths.append(child)
					RingedSeal.count -= 1
			return deaths
		return False
	
	def give_birth(self, female, male):
		parents = {
			'm': male,
			'f': female
		}
		child = RingedSeal(choice(['f', 'm']), parents, 0)
		self.children.append(child)
		return child
		
	def check_birth(self, agents, same_neighbours):
		if self.age > self.mating:
			if len(same_neighbours) > 0 and random() < self.probability_birth * (1 - RingedSeal.count / RingedSeal.capacity):
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
				RingedSeal.count += 1
				return self.give_birth(female, male)
		return False
				
	def move(self, agents):
		if self.age > self.weaning:
			self.x = self.restrict(self.x + uniform(-self.movement_speed, self.movement_speed), 0, 100)
			self.y = self.restrict(self.y + uniform(-self.movement_speed, self.movement_speed), 0, 100)
		else:
			self.x = self.parents['f'].x
			self.y = self.parents['f'].y
