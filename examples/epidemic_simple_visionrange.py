import sys
sys.path.append("c:/git/westworld/")

from westworld.environment.grid import GridEnvironment
from westworld.agents.grid import GridAgent,Obstacle,Trigger
from westworld.simulation.simulation import Simulation
from westworld.colors import *

# Setup constants
BOX_SIZE = 20
WIDTH = 50
HEIGHT = 30

# Setup classes
class Agent(GridAgent):
    
    # Constants
    attrs = ["vision_range"]
    show_vision_range = True
    
    # Step function
    # What happens in a clock tick
    def step(self,env):
        self.wander(env = env)
        
        coll = env.find_objects_in_range(self)
        if len(coll) > 0:
            self.color = RED
        else:
            self.color = GREEN
            

class EpidemicEnvironment(GridEnvironment):

    def step(self,*args,**kwargs):
        super().step(*args,**kwargs)

            
class SimpleEpidemic(Simulation):
    pass

agent_spawner = lambda x,y : Agent(x,y,1,1,BOX_SIZE,color = GREEN,curiosity = 10,vision_range = 3)

# Setup grid
env = EpidemicEnvironment(BOX_SIZE,WIDTH,HEIGHT)
env.spawn(agent_spawner,20)
env.render()


# Setup simulation
sim = SimpleEpidemic(env,fps = 10)
sim.run_episode(n_steps = 100,save = True)