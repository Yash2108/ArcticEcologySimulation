import matplotlib
import pycxsimulator
matplotlib.use('TkAgg')
from pylab import *
import copy as cp
agents=[]

class Animal:
    pass

class PB(Animal):
    pass

class RS(Animal):
    pass
vals={
    'bear':{
        'pop':25,
        'move':0.03,
        'dr': 0.8,
        'br': 0.1,
        'area': 0.1
    },
    'seal':{
        'pop': 200,
        'move':0.05,
        'dr': 0.3,
        'br': 0.68,
        'area': 0.1
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
        ag=PB() if i<vals['bear']['pop'] else RS()
        ag.move=vals[animal[which_animal]]['move']
        ag.br=vals[animal[which_animal]]['br']
        ag.dr=vals[animal[which_animal]]['dr']
        ag.area=vals[animal[which_animal]]['area']
        ag.x = random()
        ag.y = random()
        agents.append(ag)

def update():
    global agents
    if agents == []:
        return
    ag = agents[randint(len(agents))]

    # simulating random movement
    
    ag.x += uniform(-ag.move, ag.move)
    ag.y += uniform(-ag.move, ag.move)
    ag.x = 1 if ag.x > 1 else 0 if ag.x < 0 else ag.x
    ag.y = 1 if ag.y > 1 else 0 if ag.y < 0 else ag.y

    # detecting collision and simulating death or birth
    neighbors = [nb for nb in agents if type(nb).__name__ != type(ag).__name__ and (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < ag.area]

    if type(ag).__name__ == 'RS':
        if len(neighbors) > 0: # if there are seals nearby
            if random() < ag.dr:
                agents.remove(ag)
                return
        if random() < ag.br*(1-sum(1 for x in agents if type(x).__name__ == 'RS')/seal_limit):
            agents.append(cp.copy(ag))
    else:
        if len(neighbors) == 0: # if there are no rabbits nearby
            if random() < ag.dr:
                agents.remove(ag)
                return
         # if there are rabbits nearby
        neighbors = [nb for nb in agents if type(nb).__name__ == 'PB' and (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < ag.area]
        if len(neighbors)!=0:
            if random() < ag.br:
                if sum(1 for x in agents if type(x).__name__=='PB')<bear_limit:
                    agents.append(cp.copy(ag))
# import pycxsimulator

def observe():
    global agents
    cla()
    bears = [ag for ag in agents if type(ag).__name__ == 'PB']
    if len(bears) > 0:
        x = [ag.x for ag in bears]
        y = [ag.y for ag in bears]
        plot(x, y, 'ro')
    seals = [ag for ag in agents if type(ag).__name__ == 'RS']
    if len(seals) > 0:
        x = [ag.x for ag in seals]
        y = [ag.y for ag in seals]
        plot(x, y, 'b.')
    axis('image')
    axis([0, 1, 0, 1])

def update_one_unit_time():
    global agents
    t = 0.
    while t < 1.:
        t += 1. / len(agents)
        update()
pycxsimulator.GUI().start(func=[initialize, observe, update_one_unit_time])