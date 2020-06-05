from westworld.environment import GridEnvironment
from westworld.agents import BaseGridAgent
from westworld.agents.collectible_finder import CollectibleFinderAgent
from westworld.objects import BaseObstacle,BaseTrigger,BaseCollectible
from westworld.simulation import Simulation
from westworld.colors import *


obstacle = BaseObstacle(10,0,1,7,color = RED)
agent_spawner = lambda x,y : CollectibleFinderAgent(x,y,color = (0,200,255),search_radius = 3,img_asset = "blob")
coll_spawner = lambda x,y : BaseCollectible(x,y,color = (220,150,50),img_filepath = "examples/assets/sprites/sprite_lemon.png")
 
# Setup grid
BOX_SIZE = 40
WIDTH = 20
HEIGHT = 10
env = GridEnvironment(WIDTH,HEIGHT,BOX_SIZE,show_grid = True,objects = [obstacle])
env.spawn(agent_spawner,1)
env.spawn(coll_spawner,20)
env.render()
env.get_img()

# Prepare simulation
sim = Simulation(env,fps = 10,name = "CollectiblesFinder")

if __name__ == "__main__":
    sim.run_episode(n_steps = 1000,save = False)
