

import sys
sys.path.append("../")

import time
import pygame
import numpy as np
import random

from westworld.environment import GridEnvironment
from westworld.agents import BaseGridAgent
from westworld.objects import BaseObstacle,BaseTrigger,BaseCollectible
from westworld.simulation import Simulation
from westworld.colors import *

BOX_SIZE = 10
WIDTH = 50
HEIGHT = 30
N_ZONES = 10
TARGETS = list(zip(np.random.randint(0,WIDTH,N_ZONES),np.random.randint(0,HEIGHT,N_ZONES)))

class Agent(BaseGridAgent):
    def init(self):
        self.target = random.choice(TARGETS)
    def step(self):
        self.move_towards(*self.target,n = 20)


agent_spawner = lambda x,y : Agent(x,y,color = GREEN)

# Setup grid
env = GridEnvironment(WIDTH,HEIGHT,BOX_SIZE)
env.spawn(agent_spawner,100)

# Setup simulation
sim = Simulation(env,fps = 30,name = "PathfindingZonesSimulation")
sim.run_episode(n_steps = 250,save = False)