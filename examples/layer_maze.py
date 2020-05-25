
from westworld.agents.grid.agent import BaseAgent
from westworld.agents.grid.layer import BaseLayer
from westworld.environment.grid import GridEnvironment
from westworld.simulation.simulation import Simulation
from westworld.colors import *

#==================================================================================================
# BASE CLASSES
#==================================================================================================

class Agent(BaseAgent):
    """Smart Agent following the mouse with pathfinding
    """
    def step(self):
        self.follow_mouse(n = 200)
        
class WanderAgent(BaseAgent):
    """Agent wandering the environment
    """
    def step(self):
        self.wander()
        
    def when_blocked(self,collisions):
        self.set_direction()
        
        
class RandomAgent(BaseAgent):
    """Agent moving with random walk
    """
    def step(self):
        self.random_walk()


#==================================================================================================
# SIMULATION
#==================================================================================================

# Prepare layer
layer = BaseLayer(filepath = "examples/layers/GeneratedMaze_cellsize=20.png",transparency = (255,255,255),init_window = True)

# Prepare agents
agents = [
    Agent(1,1,color = RED),
    WanderAgent(1,19,color = BLUE,curiosity = 20),
    RandomAgent(19,19,color = GREEN),
]

# Prepare environment
env = GridEnvironment(
    box_size = 20,
    layers = layer,
    show_grid = True,
    background_color = WHITE,
    grid_color = (200,200,200),
    objects = agents)

# Prepare simulation and run it
sim = Simulation(env,fps = 15,name = "LayerPathfindingMouse")

if __name__ == "__main__":
    sim.run_episode(n_steps = 200,save = False)
