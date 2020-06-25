

from westworld.environment import SpatialEnvironment
from westworld.agents import BaseAgent
from westworld.objects import BaseLayer
from westworld.simulation import Simulation
from westworld.colors import *


# Prepare layer
layer = BaseLayer(img_filepath = "examples/assets/layers/GeneratedMaze_cellsize=50.png",img_transparency = (255,255,255))

class Agent(BaseAgent):
    
    @property
    def blocking(self):
        return False
    
    def when_blocked(self,collisions):
        self.set_direction()
    
    
    def step(self):
        self.wander()

spawner = lambda x,y : Agent(x,y,width = 10,height = 10,img_asset = "arrow",img_rotate = True,)
        
env = SpatialEnvironment(objects = [layer],background_color = WHITE)
env.spawn(spawner,1000)
sim = Simulation(env,fps = 25)

if __name__ == "__main__":
    sim.run_episode(n_steps = 1000,save = True)