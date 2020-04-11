

import pygame
import time
import imageio
from pathlib import Path

class Simulation:

    def __init__(self,env,fps = 10,name = None):

        self.env = env
        self.fps = fps
        self._reset_frame_cache()

        name = self.__class__.__name__ if name is None else name
        self.name = f"{name}_{int(time.time())}"
    


    def _reset_frame_cache(self):
        self.frame_cache = []

    def cache_frame(self):
        frame = self.env.get_frame()
        self.frame_cache.append(frame)


    def step(self):
        """Method that can to be overridden by children simulations
        This will be run during the main run method
        TODO not forced to render
        """

        # Step for the environment
        self.env.step()

        # Render all objects in the environment
        self.env.render()


    def save_simulation_gif(self,save,frames = None,filepath = None):

        # Saving loop
        if save is not None:
            if save == True:
                filepath = None
            elif save == False:
                return None
            elif isinstance(save,str):
                filepath = save
            else:
                raise SimulationError("Save must be True or a string to name the simulation gif")
                    
            if frames is None:
                frames = self.frame_cache

            if filepath is None:

                filepath = f"{self.name}.gif"

            img_dir = Path("./captures")
            img_dir.mkdir(exist_ok=True)
            filepath = f"./captures/{filepath}"

            print(f"[INFO] Saving gif at {filepath}")
            imageio.mimsave(filepath,frames,fps=self.fps)



    def run_episode(self,n_steps = 100,save = None):


        # Simulation variables
        simulation_on = True
        i = 0
        clock = pygame.time.Clock()

        # Main simulation loop for one episode
        while simulation_on:

            # Main step function
            self.step()

            # Cache frame if needed
            if save is not None:
                self.cache_frame()

            # Wait between frames
            clock.tick(self.fps)

            # Quitting loop
            for event in pygame.event.get():

                # Launch functions that can be overridden
                self.on_event(event)

                # Quit if click on QUIT
                if event.type == pygame.QUIT:
                    simulation_on = False

            # Stopping conditions
            if i >= n_steps:
                simulation_on = False
            else:
                i += 1


        # Saving simulation as gif
        self.save_simulation_gif(save = save)

        # Quit simulation
        self.env.quit()


    def get_mouse_pos(self):
        # TODO could be in the environment class
        x,y = pygame.mouse.get_pos()
        x = x // self.env.box_size
        y = y // self.env.box_size
        return x,y 

    def event_is_click(self,event):
        LEFT = 1
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT

    def event_is_rightclick(self,event):
        RIGHT = 3
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT

    def on_event(self,event):
        pass



class SimulationError(Exception):
    pass