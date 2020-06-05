
import numpy as np
import pandas as pd
import pygame
import random
from PIL import Image
from win32api import GetSystemMetrics


# Custom libraries
from .spatial import SpatialEnvironment
from ..algorithms.neighbors import NeighborsFinder


class GridEnvironment(SpatialEnvironment):
    def __init__(self,width = None,height = None,cell_size = 10,
        objects = None,show_grid = False,grid_color = (50,50,50),background_color = (0,0,0),
        ):

        # Init pygame
        pygame.init()
        self.screen = pygame.display.set_mode((1,1),0,0)

        # Store parameters
        self._cell_size = cell_size
        self._done = False
        self.show_grid = show_grid
        self.grid_color = grid_color
        self.width = width if width is not None else (GetSystemMetrics(0) // cell_size) - 3
        self.height = height if height is not None else (GetSystemMetrics(1) // cell_size) - 3
        self.background_color = background_color

        # Groups initialization
        self.group_blocking = pygame.sprite.Group()
        self.group_layers = pygame.sprite.Group()
        self.group_triggers = pygame.sprite.Group()

        # Objects initialization
        self._objects = {}
        self.add_object(objects)

        # Grid Environment parameters
        self.setup_screen()

        # Init objects data
        self.set_data()
        self.render()


    @property
    def cell_size(self):
        return self._cell_size

    def init_screen(self):
        pass



    @property
    def layers(self):
        return self.group_layers.sprites()

    def has_layers(self):
        return len(self.group_layers) > 0
    
    def has_blocking(self):
        return len(self.group_blocking) > 0

    def has_triggers(self):
        return len(self.group_triggers) > 0


    def quit(self):
        pygame.quit()


    def finish_episode(self):
        self._done = True


    @property
    def data(self):
        return self._data

    @property
    def done(self):
        return self._done


    @property
    def objects(self):
        return list(self._objects.values())


    def get_object(self,object_id):
        if isinstance(object_id,str):
            return self._objects[object_id]
        else:
            return self._objects[object_id.id]


    def __getitem__(self,object_id):
        return self.get_object(object_id)

    def remove_object(self,object_id):

        if isinstance(object_id,str):
            obj = self._objects.pop(object_id)
        else:
            obj = self._objects.pop(object_id.id)

        self.group_blocking.remove(obj)
        self.group_triggers.remove(obj)
        self.group_layers.remove(obj)



    def add_object(self,obj):

        if obj is not None:

            # If we add a list of objects, using recursive function to add each object
            if isinstance(obj,list):
                for o in obj:
                    self.add_object(o)
                
            # Add object 
            else:
                
                # Set environment as attribute for easy manipulation
                obj.bind(self)
                self._objects[obj.id] = obj

                if obj.layer:
                    self.group_layers.add(obj)

                if obj.blocking:
                    self.group_blocking.add(obj)

                if obj.trigger:
                    self.group_triggers.add(obj)
                


    def find_objects(self,condition = None,return_pos = False,return_objects = False,return_data = False,**kwargs):
        # TODO is it faster with numpy or pandas
        # The loop could be accelerated with numba?
        ids = []

        if condition is None:
            ids = [x.id for x in self.objects]
        else:
            def helper_check_fn(obj,k,v):
                if not hasattr(obj,k):
                    return False
                else:
                    return getattr(obj,k) == v

            for obj in self.objects:
                if all([helper_check_fn(obj,k,v) for k,v in condition.items()]):
                    ids.append(obj.id)
                

        if return_pos:
            return [self._objects[k].pos for k in ids]
        elif return_objects:
            return [self._objects[k] for k in ids]
        elif return_data:
            return self.data.loc[ids]
        else:
            return ids








    #=================================================================================
    # COLLIDERS
    #=================================================================================


    def correct_offscreen_move(self,x,y):

        env_width = self.width
        env_height = self.height

        # Check with x
        if x >= env_width:
            new_x = 0
        elif x < 0:
            new_x = env_width - 1
        else:
            new_x = x

        # Check with y
        if y >= env_height: 
            new_y = 0
        elif y < 0:
            new_y = env_height - 1
        else:
            new_y = y

        return new_x,new_y


    def is_object_colliding(self,obj):
        is_collision,_ = obj.collides()
        return is_collision


    #=================================================================================
    # SPAWNERS
    #=================================================================================



    def spawn(self,spawner,n,allow_overlap = False,**kwargs):
        """Spawner function
        """

        # Spawn n elements (works also with n = 1)
        for i in range(n):

            # Generate a random position considering or not overlaps
            x,y = self.get_random_available_pos(allow_overlap = allow_overlap)

            # Spawn new object using spawner
            # Pass also kwargs to spawner
            obj = spawner(x,y,**kwargs)
            self.add_object(obj)

        # Append to data
        self.set_data()


    #=================================================================================
    # LAYERS
    #=================================================================================


    def _set_obstacle_layer_group(self):
        group = pygame.sprite.Group()
        for layer in self.layers:
            if layer.obstacle:
                group.add(layer.sprite)
        self._obstacle_layer_group = group


    # @property
    # def has_layers(self):
    #     return len(self.layers) >= 1



    #=================================================================================
    # MESHES AND ARRAYS
    #=================================================================================


    def get_grid(self):
        return np.zeros((self.width,self.height)).T


    def get_navigation_mesh(self,obj = None):

        # Prepare empty mesh        
        mesh = self.get_grid()

        # Get all blocking objects
        object_id = "" if obj is None else obj.id
        positions = [x.pos_array for x in self.objects if (x.id != object_id and x.blocking)]
        positions = [y for x in positions for y in x]

        # Update mesh with blocking positions
        if len(positions) > 0:
            mesh[tuple(np.array(positions).T)] = 1


        # Update navigation mesh with obstacles layer if any
        if self.has_layers:
            all_meshes = [mesh]
            all_meshes.extend([layer.get_navigation_mesh() for layer in self.layers])
            mesh = np.int8(np.sum(all_meshes,axis = 0) > 0)

        return mesh

    def get_available_mesh(self):

        # Prepare empty mesh        
        mesh = self.get_grid()

        # Get all blocking objects
        positions = [y for x in self.objects for y in x.pos_array]

        if len(positions) > 0:

            # Update mesh with blocking positions
            mesh[tuple(np.array(positions).T)] = 1

        return mesh


    def get_available_pos(self):

        # Get mesh
        mesh = self.get_available_mesh()

        # Return list of pos
        return np.array(np.where(mesh == 0)).T


    def get_random_available_pos(self,allow_overlap = False):

        if allow_overlap:
            x = np.random.randint(0,self.width)
            y = np.random.randint(0,self.height)
        else:
            # Warning x,y are reversed in numpy
            pos = self.get_available_pos()
            y,x = random.choice(pos)
        return x,y



    #=================================================================================
    # DATA MANIPULATION
    #=================================================================================


    def _prepare_data(self):
        # TODO this function is not optimized at all, 
        # It takes a few ms for only a few agents in the environment
        # Iteration is quite fast, it's transforming to dataframe that takes time
        # Yet we can probably use dataframes for faster computing later on, maybe interesting to use faster equivalents
        # Such a numpy arrays, jax arrays or torch tensors
        data = [obj.get_data() for obj in self.objects]
        if len(data) == 0:
            return None
        else:
            data = pd.DataFrame(data).set_index("id")
            return data


    def set_data(self):

        # Update data
        self._data = self._prepare_data()

        # Update also neighbors finder
        # self.neighbors_finder = NeighborsFinder(self._data)







    #=================================================================================
    # ENV LIFECYCLE
    #=================================================================================

    def callback_step(self):
        pass

    def step(self):

        # Iterate for each object
        for agent in self.objects:

            # Only step with non static objects: ie agents
            if agent.stationary == False:
                agent.step()
                agent.clocktick()

        # Reinitialize data
        # TODO this can be optional for performance
        # Actually it's only required for computations such as pathfinding
        self.set_data()

        # Step callback
        self.callback_step()

        # Prepare reward and done
        # TODO add reward
        reward = 0
        done = self.done

        return reward,done


    #=================================================================================
    # RENDERERS
    #=================================================================================




    def _init_screen_from_layer(self):

        # Init grid map from layers
        layer = self.layers[0]
        w,h = layer.get_size()
        self.width = w//self.cell_size
        self.height = h//self.cell_size




    def setup_screen(self):
        """Setup the first PyGame Screen
        """

        if self.has_layers():
            self._init_screen_from_layer()
        

        # Init pygame window
        pygame.init()
        pygame.display.set_caption("Westworld environment")

        # Create window
        self.screen = pygame.display.set_mode((
            self.width * self.cell_size,
            self.height * self.cell_size
            ),pygame.RESIZABLE)

        # Fill with black
        self.reset_screen()


    def render_text(self,text,font = "Arial",size = 30,position = (5,5),screen = None,color = (0,0,0)):

        font = pygame.font.SysFont(font, size)
        text_surface = font.render(f"{text}", False,color)

        if screen is None: screen = self.screen
        screen.blit(text_surface,position)




    def reset_screen(self):
        """Reset PyGame screen by filling with BLACK color
        """
        self.screen.fill(self.background_color)


    def render_grid(self,color = (50,50,50)):

        for x in range(self.width):
            for y in range(self.height):
                rect = pygame.Rect(x*self.cell_size, y*self.cell_size,self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, color, rect, 1)



    def render(self,screen = None):
        """Render the environment
        TODO: could be without PyGame
        """

        if screen is None:
            # Reset current screen to black
            self.reset_screen()
            screen = self.screen

        # Show grid if necessary
        if self.show_grid:
            self.render_grid(self.grid_color)

        # Render each object
        for el in self.objects:
            el.render(screen = screen)

        # Update the PyGame renderer
        pygame.display.update()



    def get_frame(self):
        """Get the current frame as numpy array

        Returns:
            np.ndarray: The current frame as numpy array
        """
        return pygame.surfarray.array3d(self.screen).swapaxes(0,1)


    def get_img(self):
        """Get the current frame as PIL image

        Returns:
            PIL.Image: The current frame as PIL Image
        """
        img = self.get_frame()
        return Image.fromarray(img)


    def save_img(self,filepath):
        """Save the current frame in a picture file (eg .png)

        Args:
            filepath (str): The output filename
        """
        img = self.get_img()
        img.save(filepath)


        




        

        





        


