

import pygame
import time
import imageio
class Simulation:

    def __init__(self,env,fps = 10):
        self.env = env
        self.fps = fps
        self._reset_frame_cache()

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
            elif isinstance(save,str):
                filepath = save
            else:
                raise SimulationError("Save must be True or a string to name the simulation gif")
                    
            if frames is None:
                frames = self.frame_cache

            if filepath is None:
                filepath = f"{int(time.time())}.gif"

            print("[INFO] Saving gif")
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

                # Quit if keydown
                if event.type == pygame.KEYDOWN:
                    simulation_on = False

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

        # Quitting pygame to end the simulation
        pygame.quit()



class SimulationError(Exception):
    pass