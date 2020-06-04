"""Simulation where an agent will get all collectibles spawn randomly
"""



import sys
sys.path.append("../")

from westworld.environment import GridEnvironment
from westworld.agents import BaseGridAgent
from westworld.objects import BaseObstacle,BaseTrigger,BaseCollectible
from westworld.simulation import Simulation
from westworld.colors import *



#==================================================================================================
# BASE CLASSES
#==================================================================================================

class Agent(BaseGridAgent):
    
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
    
    def on_trigger(self,obj):
        obj.score += 1
        obj.target = None
        
        

#==================================================================================================
# SIMULATION
#==================================================================================================

        
# Setup agents
agent = Agent(1,1,color = RED)

# Setup collectibles as random spawner
collectible_spawner = lambda x,y : Collectible(x,y,color = WHITE)

# Setup environment
env = GridEnvironment(20,10,30,objects = [agent])
env.spawn(collectible_spawner,10)
env.render()

# Prepare simulation
sim = Simulation(env,fps = 30,name="CollectiblesSimple")

if __name__ == "__main__":
    sim.run_episode(n_steps = 200,save = True)
