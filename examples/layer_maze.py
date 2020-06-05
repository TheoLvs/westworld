
from westworld.environment import GridEnvironment
from westworld.agents import BaseGridAgent
from westworld.objects import BaseObstacle,BaseTrigger,BaseCollectible,BaseLayer
from westworld.simulation import Simulation
from westworld.colors import *


#==================================================================================================
# BASE CLASSES
#==================================================================================================

class Agent(BaseGridAgent):
    """Smart Agent following the mouse with pathfinding
    """
    def step(self):
        self.follow_mouse(n = 200)
        
class WanderAgent(BaseGridAgent):
    """Agent wandering the environment
    """
    def step(self):
        self.wander()
        
    def when_blocked(self,collisions):
        self.set_direction()
        
        
class RandomAgent(BaseGridAgent):
    """Agent moving with random walk
    """
    def step(self):
        self.random_walk()


#==================================================================================================
# SIMULATION
#==================================================================================================

# Prepare layer
layer = BaseLayer(img_filepath = "examples/assets/layers/GeneratedMaze_cellsize=20.png",img_transparency = (255,255,255))

# Prepare agents
agents = [
    Agent(1,1,color = RED,img_asset = "blob"),
    WanderAgent(1,19,color = BLUE,curiosity = 20),
    RandomAgent(19,19,color = GREEN),
]

# Prepare environment
env = GridEnvironment(
    cell_size = 20,
    show_grid = True,
    background_color = WHITE,
    grid_color = (200,200,200),
    objects = agents + [layer])

# Prepare simulation and run it
sim = Simulation(env,fps = 15,name = "LayerPathfindingMouse")

if __name__ == "__main__":
    sim.run_episode(n_steps = 500,save = False)
