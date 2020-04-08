# Simple pathfinding

!!! abstract
    In this page, a few examples of simulations to experiment with pathfinding


## Simple pathfinding
In this simulation
- All agents are moving towards the same point
- When we left click we add an object
- When we right click we change the point of attraction

??? note "Python code for this simulation"

    ```python
    import time
    import pygame
    import numpy as np

    from westworld.environment.grid import GridEnvironment
    from westworld.agents.grid import GridAgent,Obstacle,Trigger
    from westworld.simulation.simulation import Simulation

    BOX_SIZE = 5
    LOOKAHEAD = 15
    target = (0,0)

    #-----------------------------------------------------------
    # DEFINING CLASSES
    #-----------------------------------------------------------

    class Agent(GridAgent):

        target = target

        def step(self,env):
            self.move_towards(x = self.target[0],y = self.target[1],env = env,n = LOOKAHEAD)


    class LargeSimulation(Simulation):

        def on_event(self,event):

            # If left click we add an obstacle 
            if self.event_is_click(event):

                x,y = self.get_mouse_pos()
                obstacle = obstacle_spawner(x,y)
                env.add_object(obstacle)

            # If right click we change the direction for pathfinding
            if self.event_is_rightclick(event):

                new_target = self.get_mouse_pos()

                for agent in self.env.agents:
                    agent.target = new_target


    #-----------------------------------------------------------
    # DEFINING SIMULATION
    #-----------------------------------------------------------

    # Prepare spawners and 
    agent_spawner = lambda x,y : Agent(x,y,1,1,BOX_SIZE)
    obstacle_spawner = lambda x,y : Obstacle(x,y,5,5,BOX_SIZE,(0,200,100))

    # Setup grid
    env = GridEnvironment(BOX_SIZE,200,100)
    env.spawn(agent_spawner,100)

    # Setup simulation
    sim = LargeSimulation(env,fps = 25)
    sim.run_episode(n_steps = 250,save = True)
    ```



##### Clicking to add obstacles
![](../img/PathfindingSimulation_1586357286.gif)

##### With more points
Simulation when running is still slow, but replay is at a normal 25 FPS
![](../img/PathfindingSimulation_1586358482.gif)


## Simple Pathfinding with zones
In this second example : 
- All agents are moving towards a different target point chosen randomly

??? note "Python code for this simulation"

    ```python
    import time
    import pygame
    import numpy as np
    import random

    from westworld.environment.grid import GridEnvironment
    from westworld.agents.grid import GridAgent,Obstacle,Trigger
    from westworld.simulation.simulation import Simulation

    BOX_SIZE = 5
    LOOKAHEAD = 15
    WIDTH = 100
    HEIGHT = 100
    N_ZONES = 10
    TARGETS = list(zip(np.random.randint(0,WIDTH,N_ZONES),np.random.randint(0,HEIGHT,N_ZONES)))


    #-----------------------------------------------------------
    # DEFINING SIMULATION
    #-----------------------------------------------------------

    class Agent(GridAgent):
        def __init__(self,*args,**kwargs):
            super().__init__(*args,**kwargs)
            self.target = random.choice(TARGETS)

        def step(self,env):
            self.move_towards(x = self.target[0],y = self.target[1],env = env,n = LOOKAHEAD)


    class PathfindingSimulationZones(Simulation):
        pass

    #-----------------------------------------------------------
    # DEFINING CLASSES
    #-----------------------------------------------------------

    # Setup spawners
    agent_spawner = lambda x,y : Agent(x,y,1,1,BOX_SIZE)

    # Setup grid
    env = GridEnvironment(BOX_SIZE,WIDTH,HEIGHT)
    env.spawn(agent_spawner,300)

    # Setup simulation
    sim = PathfindingSimulationZones(env,fps = 25)
    sim.run_episode(n_steps = 250,save = True)
    ```

![](../img/PathfindingSimulationZones_1586359228.gif)
