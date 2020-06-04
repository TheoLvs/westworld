import sys
sys.path.append("../")

from westworld.environment import GridEnvironment
from westworld.agents import BaseGridAgent
from westworld.objects import BaseObstacle,BaseTrigger,BaseCollectible
from westworld.simulation import Simulation
from westworld.colors import *


class Agent(BaseGridAgent):
    
    def step(self):
        self.wander()
        
        
obstacle = BaseObstacle(10,0,1,7,color = BLUE)
agent_spawner = lambda x,y : Agent(x,y,color = GREEN)
coll_spawner = lambda x,y : BaseCollectible(x,y,color = WHITE,circle = True,radius = 0.3)
agent1 = agent_spawner(1,1)

# Setup grid
BOX_SIZE = 20
WIDTH = 20
HEIGHT = 10

env = GridEnvironment(WIDTH,HEIGHT,BOX_SIZE,show_grid = True,objects = [obstacle,agent1])
env.spawn(coll_spawner,120)
env.render()

# Prepare simulation
sim = Simulation(env,fps = 30,name="CollectiblesObstacle")

if __name__ == "__main__":
    sim.run_episode(n_steps = 200,save = True)
