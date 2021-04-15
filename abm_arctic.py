from matplotlib.colors import ListedColormap
from random import randint, uniform
from ringedseal import RingedSeal
from polarbear import PolarBear
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

def initialize():
	global env, agents
# 	env = np.vstack((np.zeros((75, 201)), np.ones((26, 201))))
	env = np.flip(imread(os.path.join(os.getcwd(), "assets\\background_3.png")), axis = 0)
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
		
def observe():
	global env, agents
	clf()
	fig = gcf()
	spec = gridspec.GridSpec(ncols=2, nrows=1, width_ratios=[4, 1])
	ax0 = fig.add_subplot(spec[0])
	ax1 = fig.add_subplot(spec[1])
	ax0.imshow(env)
	x = {'PolarBear': [], 'RingedSeal': []}
	y = {'PolarBear': [], 'RingedSeal': []}
	for i in agents:
		name = type(i).__name__
		x[name].append(i.x)
		y[name].append(i.y)
	image_path_1 = get_sample_data(os.path.join(os.getcwd(), "assets\\polar.png"))
	image_path_2 = get_sample_data(os.path.join(os.getcwd(), "assets\\ringedseal.png"))
	imscatter(x['PolarBear'], y['PolarBear'], image_path_1, zoom=0.1, ax=ax0)	
	imscatter(x['RingedSeal'], y['RingedSeal'], image_path_2, zoom=0.03, ax=ax0)	
	ax0.plot(x['PolarBear'], y['PolarBear'], 'o')
	ax0.plot(x['RingedSeal'], y['RingedSeal'], 'o')
	ax0.axis([0, 200, 0, 100])
	ax0.set_title("Ringed Seals: {rs}    Polar Bears: {pb}".format(rs = RingedSeal.count, pb = PolarBear.count))
	mng = plt.get_current_fig_manager()
	mng.window.state('zoomed')	

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
	global agents
	for ag in agents:
		ag.move(agents)
	i = 0
	while i < len(agents):
		if not update(agents[i]):
			i += 1

if __name__ == "__main__":
# 	global fig, axs
# 	fig, axs = plt.subplots(1, 2, gridspec_kw={'width_ratios': [5, 1]})
	blue = cm.get_cmap('Blues', 4)
	cm.register_cmap(name = 'ice', cmap = ListedColormap([blue(0), blue(1)]))
	matplotlib.rcParams['image.cmap'] = 'ice'
	pycxsimulator.GUI().start(func = [initialize, observe, update_one_unit_time])