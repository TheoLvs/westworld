

import sys
sys.path.append("../../")

import time
import pygame
import numpy as np

from westworld.environment.grid import GridEnvironment
from westworld.agents.grid import GridAgent,Obstacle,Trigger
from westworld.simulation.simulation import Simulation

BOX_SIZE = 50

class Agent(GridAgent):

    def step(self,env):

        # self.move(dx = 1,env = env)
        self.move_towards(obj = triggers[0],env = env)


agents = [
    Agent(1,1,1,1,BOX_SIZE,circle = True),
    Agent(1,3,1,1,BOX_SIZE,circle = True),
]

obstacles = [Obstacle(7,0,1,8,BOX_SIZE,(0,200,100))]
triggers = [Trigger(18,1,1,1,BOX_SIZE,(255,255,255),circle = True)]


# Setup grid
env = GridEnvironment(BOX_SIZE,20,10,objects = agents + obstacles + triggers)


# Setup simulation
sim = Simulation(env,fps = 5)

sim.run_episode(save = True)