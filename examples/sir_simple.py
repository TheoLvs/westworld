
from westworld.environment import GridEnvironment
from westworld.agents import BaseGridAgent
from westworld.agents.sir_agent import SIRAgent
from westworld.objects import BaseObstacle,BaseTrigger,BaseCollectible,BaseLayer
from westworld.simulation import Simulation
from westworld.logger import Logger
from westworld.colors import *

import matplotlib.pyplot as plt


graphs = {"Population":{"cols":["S","I","R"],"kind":"line"}}
logger = Logger(use_visdom=False,freq_update = 5,graphs = graphs)
        
def callback_logger(env):
    
    for state in ["S","I","R"]:
        n = len(env.find_objects({"state":state}))
        logger.log_metric(state,n)
    
    
    

CONTACT_RISK = 6
RECOVERY_DURATION_RANGE = [20,50]

spawner = lambda state : lambda x,y : SIRAgent(x,y,state = state,contact_risk = CONTACT_RISK,recovery_duration_range = RECOVERY_DURATION_RANGE)

    
    
# Setup grid
CELL_SIZE = 20
WIDTH = 40
HEIGHT = 30
env = GridEnvironment(cell_size = CELL_SIZE,width = WIDTH,height = HEIGHT,show_grid = False,callbacks_step=[callback_logger])
env.spawn(spawner("S"),100)
env.spawn(spawner("I"),1)


# Prepare simulation and run it
sim = Simulation(env,fps = 10,name = "SimpleSIR")

if __name__ == "__main__":
    sim.run_episode(n_steps = 200,save = False)

    logger.df[["S","I","R"]].plot()
    plt.show()

