from matplotlib.colors import ListedColormap
from random import randint, uniform
from ringedseal import RingedSeal
from polarbear import PolarBear
from walrus import Walrus
from matplotlib import cm
import pycxsimulator
from pylab import *
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import gridspec
import copy as cp
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.cbook import get_sample_data
import os

matplotlib.use('TkAgg')
days=0
cumulative_population = {'PolarBear': [], 'RingedSeal': [], "Walrus": []}

def initialize():
	global env, agents
# 	env = np.vstack((np.zeros((75, 201)), np.ones((26, 201))))
	env = imread(os.path.join(os.getcwd(), "assets\\background_3.png"))
	agents = []
	parents = {
		'm': "Initialized",
		'f': "Initialized"
	}
	for i in range(PolarBear.initial_population // 2):
		agents.append(PolarBear('m', parents))
		agents.append(PolarBear('f', parents))
	for i in range(RingedSeal.initial_population // 2):
		agents.append(RingedSeal('m', parents))	
		agents.append(RingedSeal('f', parents))	
	ag=Walrus('m', parents)
	agents.append(ag)
	for i in range(Walrus.initial_population // 2):
		ag1=Walrus('m', parents, ag.group_id)
		ag1.x=ag.x+uniform(-4,4)
		ag1.y=ag.y+uniform(-4,4)
		agents.append(ag1)
		ag1=Walrus('f', parents, ag.group_id)
		ag1.x=ag.x+uniform(-4,4)
		ag1.y=ag.y+uniform(-4,4)	
		agents.append(ag1)	
		
		
def observe():
	global env, agents, days, cumulative_population
	clf()
	fig = gcf()
	# spec = gridspec.GridSpec(ncols=2, nrows=1, width_ratios=[4, 1])
	x = {'PolarBear': [], 'RingedSeal': [], "Walrus":[]}
	y = {'PolarBear': [], 'RingedSeal': [], "Walrus":[]}
	population = {'PolarBear': 0, 'RingedSeal': 0, "Walrus": 0}
	for i in agents:
		name = type(i).__name__
		x[name].append(i.x)
		y[name].append(i.y)
		population[name]+=1
	for i in population:
		cumulative_population[i].append(population[i])
	image_path_1 = get_sample_data(os.path.join(os.getcwd(), "assets\\polar.png"))
	image_path_2 = get_sample_data(os.path.join(os.getcwd(), "assets\\ringedseal.png"))
	image_path_3 = get_sample_data(os.path.join(os.getcwd(), "assets\\walrus.png"))
	day_axis=[0]+list(range(1,days+1))
	# if days==0:
	# 	day_axis=[0]
	# else:
	# 	day_axis=list(range(days))
	ax1 = fig.add_subplot(121, label="1")
	ax0 = fig.add_subplot(121, label="2", frame_on=False)
	ax2 = fig.add_subplot(122, label="3")
	ax3 = fig.add_subplot(122, label="4", frame_on=False)
	ax4 = fig.add_subplot(122, label="5", frame_on=False)
	ax1.imshow(env)
	ax1.set_axis_off()
	ax1.set_aspect(0.84)
	# imscatter(x['PolarBear'], y['PolarBear'], image_path_1, zoom=0.1, ax=ax0)	
	# imscatter(x['RingedSeal'], y['RingedSeal'], image_path_2, zoom=0.03, ax=ax0)	
	# imscatter(x['Walrus'], y['Walrus'], image_path_3, zoom=0.03, ax=ax0)	
	ax0.plot(x['PolarBear'], y['PolarBear'], 'o')
	ax0.plot(x['RingedSeal'], y['RingedSeal'], 'o')
	ax0.plot(x['Walrus'], y['Walrus'], 'o')
	ax0.axis([0, 200, 0, 100])
	ax0.set_title("Day Number: {day}    Ringed Seals: {rs}    Polar Bears: {pb}, Walrus: {wl}".format(day=days, rs = RingedSeal.count, pb = PolarBear.count, wl=Walrus.count))
	ax0.set_aspect(0.935)

	ax2.plot(day_axis, cumulative_population['RingedSeal'], color="C1")
	ax2.tick_params(axis='x', colors="C1")
	ax2.tick_params(axis='y', colors="C1", pad=5)
	ax2.set_xlabel("Day Number")
	ax2.set_ylabel("Ringed Seals")
	# ax2.ytick.set_pad(5)
	ax3.plot(day_axis, cumulative_population['PolarBear'], color="C0")
	ax3.tick_params(axis='x', colors="C0")
	ax3.tick_params(axis='y', colors="C0")
	ax3.yaxis.tick_right()
	ax3.set_xlabel("Day Number")
	ax3.set_ylabel("Polar Bear")
	ax3.yaxis.set_label_position('right') 
	# ax3.ytick.set_pad(10) 
	
	ax4.plot(day_axis, cumulative_population['Walrus'], color="C2")
	ax4.tick_params(axis='x', colors="C2")
	ax4.tick_params(axis='y', colors="C2", pad=45)
	ax4.set_xlabel("Day Number")
	ax4.set_ylabel("Walrus")

	plt.subplots_adjust(right=0.95)
	# ax4.ytick.set_pad(15)
	# ax4.set_axis_off()
	mng = plt.get_current_fig_manager()
	mng.window.state('zoomed')	
	savefig('plot' + str(days) + '.png')

def imscatter(x, y, image, ax=None, zoom=1):
    if ax is None:
        ax = plt.gca()
    try:
        image = plt.imread(image)
    except TypeError:
        # Likely already an array...
        pass
    im = OffsetImage(image, zoom=zoom)
    x, y = np.atleast_1d(x, y)
    artists = []
    for x0, y0 in zip(x, y):
        ab = AnnotationBbox(im, (x0, y0), xycoords='data', frameon=False)
        artists.append(ax.add_artist(ab))
    ax.update_datalim(np.column_stack([x, y]))
    ax.autoscale()
    return artists	

def update(ag):
	global agents
	name = type(ag).__name__
	neighbours = [nb for nb in agents if type(nb).__name__ != name and 
							  (ag.x - nb.x) ** 2 + (ag.y - nb.y) ** 2 < ag.radius_sq]
	same_neighbours = [nb for nb in agents if type(nb).__name__ == name and 
										 (ag.x - nb.x) ** 2 + (ag.y - nb.y) ** 2 < ag.radius_sq]
	deaths = ag.check_death(agents, neighbours)
	if deaths != False:
		for death in deaths:
			agents.remove(death)
		return True
	child = ag.check_birth(agents, same_neighbours)
	if child != False:
		agents.append(child)
	ag.age += 1
	return False
			
def update_one_unit_time():
	global agents, days
	for ag in agents:
		ag.move(agents)
	i = 0
	while i < len(agents):
		if not update(agents[i]):
			i += 1
	days+=1
	for i in Walrus.group_dict:
		Walrus.group_dict[i]['moved']=False


if __name__ == "__main__":
# 	global fig, axs
# 	fig, axs = plt.subplots(1, 2, gridspec_kw={'width_ratios': [5, 1]})
	blue = cm.get_cmap('Blues', 4)
	cm.register_cmap(name = 'ice', cmap = ListedColormap([blue(0), blue(1)]))
	matplotlib.rcParams['image.cmap'] = 'ice'
	pycxsimulator.GUI().start(func = [initialize, observe, update_one_unit_time])