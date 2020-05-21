"""Simulation where agent become red if in range of other agents
It highlight the vision range feature useful to search collectibles, simulate vision, or contagion in epidemic models
"""
import sys
sys.path.append("../")

from westworld.environment.grid import GridEnvironment
from westworld.agents.grid import BaseAgent
from westworld.simulation.simulation import Simulation
from westworld.colors import *


# Setup classes
class Agent(BaseAgent):
    
    show_vision_range = True
    
    def step(self):
        self.wander()
        
        collisions = self.find_in_range()
        if len(collisions) > 0:
            self.color = RED
        else:
            self.color = GREEN
            


agent_spawner = lambda x,y : Agent(x,y,color = GREEN,curiosity = 10,vision_range = 3)

# Setup grid
BOX_SIZE = 20
WIDTH = 50
HEIGHT = 30
env = GridEnvironment(WIDTH,HEIGHT,BOX_SIZE)
env.spawn(agent_spawner,20)
env.render()


# Setup simulation
sim = Simulation(env,fps = 10,name = "EpidemicVisionRange")


if __name__ == "__main__":
    sim.run_episode(n_steps = 200,save = True)
