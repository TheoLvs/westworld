
from westworld.environment import GridEnvironment
from westworld.agents import BaseGridAgent
from westworld.agents.sir_agent import SIRAgent
from westworld.objects import BaseObstacle,BaseTrigger,BaseCollectible,BaseLayer
from westworld.simulation import Simulation
from westworld.logger import Logger
from westworld.colors import *
import matplotlib.pyplot as plt


logger = Logger()

def callback_logger(env):
    for state in ["S","I","R"]:
        n = len(env.find_objects({"state":state}))
        logger.log_metric(state,n)


CONTACT_RISK = 6
RECOVERY_DURATION_RANGE = [50,150]

spawner = lambda state : lambda x,y : SIRAgent(x,y,state = state,contact_risk = CONTACT_RISK,recovery_duration_range = RECOVERY_DURATION_RANGE)


# Prepare layer
layer = BaseLayer(img_filepath = "examples/assets/layers/Layer_1590257407_boxsize=20.png",img_transparency = (255,255,255))

# Prepare environment
env = GridEnvironment(
    cell_size = 10,
    show_grid = True,
    background_color = WHITE,
    grid_color = (200,200,200),
    callbacks_step = [callback_logger],
    objects = [layer])


env.spawn(spawner("S"),100)
env.spawn(spawner("I"),10)

# Prepare simulation and run it
sim = Simulation(env,fps = 25,name = "RoomSIR")

if __name__ == "__main__":
    sim.run_episode(n_steps = 200,save = False)

    logger.df[["S","I","R"]].plot()
    plt.show()