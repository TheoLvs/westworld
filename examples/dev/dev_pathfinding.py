

import sys
sys.path.append("C:/git/westworld")

import time
import pygame
import numpy as np

from westworld.environment.grid import GridEnvironment
from westworld.agents.grid import GridAgent,Obstacle,Trigger

BOX_SIZE = 50


class Agent(GridAgent):

    def step(self,env):

        self.move(dx = 1,env = env)


agents = [
    Agent(1,1,1,1,BOX_SIZE,circle = True),
    Agent(1,3,1,1,BOX_SIZE,circle = True),
]


obstacles = [
    Obstacle(7,0,1,8,BOX_SIZE,(0,200,100)),
]

triggers = [
    Trigger(18,1,1,1,BOX_SIZE,(255,255,255),circle = True)
]



# Setup grid
env = GridEnvironment(BOX_SIZE,20,10,objects = agents + obstacles + triggers)

n_steps = 1000
i = 0
simulation_on = True
step_duration = 0.1


while simulation_on:


    env.step()
    env.render()
    time.sleep(step_duration)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            # agent.change_direction()
            simulation_on = False
    
        if event.type == pygame.QUIT:
            simulation_on = False

    if i >= n_steps:
        simulation_on = False
    else:
        i += 1
        

pygame.quit()
