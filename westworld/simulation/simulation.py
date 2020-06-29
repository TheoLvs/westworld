

import pygame
import time
import numpy as np
import ffmpeg
import imageio
from pathlib import Path
from tqdm import tqdm_notebook
from ipywidgets import interact,widgets
from IPython.display import display 
from PIL import Image

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
        reward,done = self.env.step()

        # Render all objects in the environment
        self.env.prerender()
        self.env.render()
        self.env.postrender()

        return reward,done



    def save_simulation_video(self,save,frames = None,filepath = None):

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

                filepath = f"{self.name}.mp4"

            img_dir = Path("./captures")
            img_dir.mkdir(exist_ok=True)
            filepath = f"./captures/{filepath}"

            print(f"[INFO] Saving video at {filepath}")
            self._save_video_from_images(filepath,frames,fps = self.fps)


    @staticmethod
    def _save_video_from_images(filepath,images, fps=60, vcodec='libx264'):
        # From https://github.com/kkroening/ffmpeg-python/issues/246
        if not isinstance(images, np.ndarray):
            images = np.asarray(images)
        n,height,width,channels = images.shape
        process = (
            ffmpeg
                .input('pipe:', format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(width, height))
                .output(filepath, pix_fmt='yuv420p', vcodec=vcodec, r=fps)
                .overwrite_output()
                .run_async(pipe_stdin=True)
        )
        for frame in images:
            process.stdin.write(
                frame
                    .astype(np.uint8)
                    .tobytes()
            )
        process.stdin.close()
        process.wait()




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



    def replay_episode(self,fps = 5):

        # Prepare widgets
        play = widgets.Play(
            value=0,
            min=0,
            max=len(self.frame_cache) - 1,
            step=1,
            interval=int(1000/fps),
            description="Press play",
            disabled=False
        )
        slider = widgets.IntSlider(min = 0,value = 0,max = len(self.frame_cache) - 1,step = 1)
        widgets.jslink((play, 'value'), (slider, 'value'))

        # Visualize frames and widgets
        @interact(i = play)
        def show(i):
            img = Image.fromarray(self.frame_cache[i])
            return img

        display(slider)


    def run_episode(self,n_steps = 100,save = None,replay = False,fps_replay = 5,save_format = "video"):


        # Simulation variables
        simulation_on = True
        i = 0
        clock = pygame.time.Clock()

        # Create progress bar
        progress_bar = tqdm_notebook(total=n_steps)

        # Cache first frame if needed
        if save is not None:
            self.cache_frame()

        # Main simulation loop for one episode
        while simulation_on:

            # Main step function
            reward,done = self.step()

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
            if i >= n_steps - 1:
                simulation_on = False
            else:
                i += 1

            # Update progress bar
            progress_bar.update(1)

            # Stop simulation if done is signaled in the inner loop
            if done:
                simulation_on = False


        # Saving simulation as gif
        if save_format == "video":
            self.save_simulation_video(save = save)
        elif save_format == "gif":
            self.save_simulation_gif(save = save)
        else:
            raise Exception("save_format must be 'video' or 'gif'")
        progress_bar.close()

        # Quit simulation
        self.env.quit()

        # Replay
        if replay:
            self.replay_episode(fps = fps_replay)


    def get_mouse_pos(self):
        # TODO could be in the environment class
        x,y = pygame.mouse.get_pos()
        x = x // self.env.cell_size
        y = y // self.env.cell_size
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