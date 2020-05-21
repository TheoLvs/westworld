

from ..environment.grid import GridEnvironment
from ..agents.grid import BaseAgent,BaseObstacle,BaseTrigger,BaseCollectible
from ..simulation.simulation import Simulation
from ..colors import *



#==================================================================================================
# BASE CLASSES
#==================================================================================================

class Agent(BaseAgent):
    
    def init(self):
        self.score = 0
        self.target = None
    
    def step(self):
        
        # Safety check
        if self.target is not None:
            if self.target not in self.env._objects:
                self.target = None

        # Find next target
        if self.target is None:
            _,ids = self.find_closest(k = 1,condition = {"collectible":True})
            if len(ids) == 0:
                self.env.finish_episode()
            else:
                stop = False
                self.target = ids[0]
        
        if not self.env.done:
            self.move_towards(obj = self.target,n = 10)
        
        
class Collectible(BaseCollectible):
    
    collectible = True
    
    def on_collision(self,objects):
        obj = self.env[objects[0]]
        obj.score += 1
        obj.target = None
        
        

#==================================================================================================
# SIMULATION
#==================================================================================================

        
# Setup agents
agent = Agent(1,1,color = RED)
agent2 = Agent(75,25,color = BLUE)

# Setup collectibles as random spawner
collectible_spawner = lambda x,y : Collectible(x,y,color = WHITE)

# Setup environment
env = GridEnvironment(80,30,10,objects = [agent,agent2])
env.spawn(collectible_spawner,100)
env.render()

# Prepare simulation
simulation = Simulation(env,fps = 30,name="CollectiblesMultiplayer")
