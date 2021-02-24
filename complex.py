import matplotlib
import pycxsimulator
matplotlib.use('TkAgg')
from pylab import *
import copy as cp
import random as rnd
import math
agents=[]

class Animal:
    id=1
    
class PB(Animal):
    def __init__(self):
        self.id=Animal.id
        Animal.id+=1

class RS(Animal):
    def __init__(self):
        self.id=Animal.id
        Animal.id+=1

vals={
    'bear':{
        'pop':4,
        'poplimit': 8,
        'move':0.03,
        'dr': 0.8,
        'br': 0.1,
        'area': 0.1,
        'type': 'bear',
        'weaning': 2.5
    },
    'seal':{
        'pop': 100,
        'poplimit': 400,
        'move':0.05,
        'dr': 0.2,
        'br': 0.68,
        'area': 0.1,
        'type': 'seal',
        'weaning': 6*7/365
    }
}
animal={0:'bear', 1:'seal'}
seal_limit=1000
bear_limit=250

def initialize():
    global agents
    agents = []
    for i in range(vals['bear']['pop']+vals['seal']['pop']):
        which_animal=0 if i<vals['bear']['pop'] else 1
        birth(which_animal, randint(0, 5475)/365, None)
        # agents[-1].age=

def move(ag):
    ag.x += uniform(-ag.move, ag.move)
    
    ag.y += uniform(-ag.move, ag.move)
    ag.x = 1 if ag.x > 1 else 0 if ag.x < 0 else ag.x
    ag.y = 1 if ag.y > 1 else 0 if ag.y < 0 else ag.y

def feed(predator, prey):
    if random() < prey.dr:
        # print(predator.type, predator.id, "Killed", prey.type, prey.id)
        agents.remove(prey)
        return True
    else:
        return False

def birth(which_animal, age, parent):
    # which_animal=0 if i<vals['bear']['pop'] else 1
    ag=PB() if which_animal==0 else RS()

    ag.move=vals[animal[which_animal]]['move']
    ag.br=vals[animal[which_animal]]['br']
    # ag.dr=vals[animal[which_animal]]['dr']
    if age<=vals[animal[which_animal]]['weaning']:
        if parent!=None:
            ag.dr=parent.dr
        else:
            ag.dr=0.5
    else:
        ag.dr=prob_den_func(age)
    # ag.dr=parent.dr if age<=vals[animal[which_animal]]['weaning'] else prob_den_func(age)
    ag.area=vals[animal[which_animal]]['area']
    ag.type=vals[animal[which_animal]]['type']
    ag.gender=rnd.choice(['m', 'f'])
    ag.x = random()
    ag.y = random()
    ag.hunger = 0
    ag.age=age
    ag.parent=parent
    
    agents.append(ag)

def prob_den_func(x, mu=15, sigma=4.69):
    y=math.exp(-((x-mu)**2)/(2*(sigma**2)))/(sigma*math.sqrt(2*22/7))
    # print(x,y)
    return y*5

def update():
    global agents
    if agents == []:
        return
    ag = agents[randint(len(agents))]

    # simulating random movement
    move(ag)


    # detecting collision and simulating death or birth

    if ag.type == 'seal':
        seals=[nb for nb in agents if nb.type == 'seal' and (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < ag.area and nb!=ag]
        bears=[nb for nb in agents if nb.type == 'bear' and (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < ag.area]
        if len(bears) > 0: # if there are bears nearby
            bear=rnd.choice(bears)
            if feed(bear, ag):
                #bear killed seal
                return
            # if random() < ag.dr:
            #     agents.remove(ag)
            #     return
        if len(seals)>0:
            # if sum(1 for x in agents if x.type=='seal')<seal_limit:
            opp_gender=[]
            for x in seals:
                if x.gender!=ag.gender:
                    opp_gender.append(x)
            if len(opp_gender)!=0:
                if random() < ag.br*(1-sum(1 for x in agents if x.type == 'seal')/vals['seal']['poplimit']):
                    mate=rnd.choice(opp_gender)
                    #number of seals increased
                    # print(mate.type, mate.id, "Mates with",ag.type, ag.id)
                    female= ag if ag.gender=='f' else mate
                    birth(1, 0, female)
                # agents.append(cp.copy(ag))
    else:
        seals=[nb for nb in agents if nb.type == 'seal' and (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < ag.area]
        bears=[nb for nb in agents if nb.type == 'bear' and (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < ag.area and nb!=ag]
        if len(seals) == 0: # if there are no seals nearby
            if random() < ag.dr:
                agents.remove(ag)
                # bear dies due to lack of food
                return
        # if len(seals)>10:
        #     if len(bears)<4:
        #         if random() < ag.dr:
        #             agents.remove(ag)
        #             return
        # if there are seals nearby

        if len(bears)!=0:
            opp_gender=[]
            same_gender=[]
            for x in seals:
                if x.gender!=ag.gender:
                    opp_gender.append(x)
                else:
                    same_gender.append(x)
            if len(opp_gender)!=0:
                if random() < ag.br*(1-sum(1 for x in agents if x.type=='bear')/vals['bear']['poplimit']):
                # if sum(1 for x in agents if x.type=='bear')<bear_limit:
                    mate=rnd.choice(opp_gender)
                    female= ag if ag.gender=='f' else mate
                    # number of bears increased
                    # print(mate.type, mate.id, "Mates with",ag.type, ag.id)
                    birth(0, 0, female)
                    # agents.append(cp.copy(ag))
    for x in agents:
        x.age+=1

# import pycxsimulator

def observe():
    global agents
    cla()
    bears = [ag for ag in agents if ag.type == 'bear']
    if len(bears) > 0:
        x = [ag.x for ag in bears]
        y = [ag.y for ag in bears]
        plot(x, y, 'ro')
    seals = [ag for ag in agents if ag.type == 'seal']
    if len(seals) > 0:
        x = [ag.x for ag in seals]
        y = [ag.y for ag in seals]
        plot(x, y, 'b.')
    axis('image')
    axis([0, 1, 0, 1])
    # print("Number of bears: ", len(bears))
    # print("Number of seals: ", len(seals))

def update_one_unit_time():
    global agents
    t = 0.
    while t < 1.:
        t += 1. / len(agents)
        update()

pycxsimulator.GUI().start(func=[initialize, observe, update_one_unit_time])

# val=norm.cdf(age, 15, 3.6)
# basic_survival_rate=0.5
# if age>15:
#     val-=0.5
#     basic_survival_rate-=val
# else:
#     basic_survival_rate+=val