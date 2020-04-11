

import sys
sys.path.append("../")

import time
import pygame
import numpy as np
import random

from westworld.environment.grid import GridEnvironment
from westworld.agents.grid import GridAgent,Obstacle,Trigger
from westworld.simulation.simulation import Simulation
from westworld.colors import *

BOX_SIZE = 20
WIDTH = 50
HEIGHT = 30


N_ZONES = 10
TARGETS = list(zip(np.random.randint(0,WIDTH,N_ZONES),np.random.randint(0,HEIGHT,N_ZONES)))
print(TARGETS)




class Agent(GridAgent):


    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.target = random.choice(TARGETS)


    # @property
    # def blocking(self):
    #     return False

    def step(self,env):

        # self.move(dx = 1,env = env)
        self.wander(env = env)




class PathfindingSimulationZones(Simulation):

    def on_event(self,event):

        if self.event_is_click(event):

            x,y = self.get_mouse_pos()
            obstacle = obstacle_spawner(x,y)
            env.add_object(obstacle)

        if self.event_is_rightclick(event):


            new_target = self.get_mouse_pos()

            for agent in self.env.agents:
                agent.target = new_target



agent_spawner = lambda x,y : Agent(x,y,1,1,BOX_SIZE,color = GREEN,curiosity = 100,vision_range = 3)
agent_spawner2 = lambda x,y : Agent(x,y,1,1,BOX_SIZE,color = RED,curiosity = 10,vision_range = 10)

obstacle_spawner = lambda x,y : Obstacle(x,y,5,5,BOX_SIZE,(0,200,100))
obstacles = []




# Setup grid
env = GridEnvironment(BOX_SIZE,WIDTH,HEIGHT,objects = obstacles)
env.spawn(agent_spawner,3)
env.spawn(agent_spawner2,3)

# Setup simulation
sim = PathfindingSimulationZones(env,fps = 10)
sim.run_episode(n_steps = 250,save = False)