

import sys
sys.path.append("../")

from westworld.environment.grid import GridEnvironment
from westworld.agents.grid import BaseAgent,BaseObstacle,BaseTrigger
from westworld.simulation.simulation import Simulation
from westworld.colors import *

TARGET = (0,0)


class Agent(BaseAgent):

    target = TARGET

    def step(self):
        x,y = self.target
        self.move_towards(x = x,y = y,n = 15)




class PathfindingClickSimulation(Simulation):

    def on_event(self,event):

        if self.event_is_click(event):

            x,y = self.get_mouse_pos()
            obstacle = obstacle_spawner(x,y)
            env.add_object(obstacle)

        if self.event_is_rightclick(event):


            new_target = self.get_mouse_pos()

            for agent in self.env.objects:
                agent.target = new_target



agent_spawner = lambda x,y : Agent(x,y)
obstacle_spawner = lambda x,y : BaseObstacle(x,y,5,5,color = GREEN)


# Setup grid
env = GridEnvironment(200,100,4)
env.spawn(agent_spawner,100)


# Setup simulation
sim = PathfindingClickSimulation(env,fps = 25)
sim.run_episode(n_steps = 500,save = True)