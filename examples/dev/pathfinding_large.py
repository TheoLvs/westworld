

import sys
sys.path.append("../../")

import time
import pygame
import numpy as np

from westworld.environment.grid import GridEnvironment
from westworld.agents.grid import GridAgent,Obstacle,Trigger
from westworld.simulation.simulation import Simulation

BOX_SIZE = 5

target = (0,0)


class Agent(GridAgent):

    target = target

    def step(self,env):

        # self.move(dx = 1,env = env)
        self.move_towards(x = self.target[0],y = self.target[1],env = env,n = 15)




class LargeSimulation(Simulation):

    def on_event(self,event):

        if self.event_is_click(event):

            x,y = self.get_mouse_pos()
            obstacle = obstacle_spawner(x,y)
            env.add_object(obstacle)

        if self.event_is_rightclick(event):


            new_target = self.get_mouse_pos()

            for agent in self.env.agents:
                agent.target = new_target



agent_spawner = lambda x,y : Agent(x,y,1,1,BOX_SIZE)
obstacle_spawner = lambda x,y : Obstacle(x,y,5,5,BOX_SIZE,(0,200,100))

obstacles = []


# Setup grid
env = GridEnvironment(BOX_SIZE,200,100,objects = obstacles)
env.spawn(agent_spawner,100)


# Setup simulation
sim = LargeSimulation(env,fps = 25)

sim.run_episode(n_steps = 250,save = True)