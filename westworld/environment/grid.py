
import numpy as np
import pandas as pd
from PIL import Image
import pygame

# Custom libraries
from .spatial import SpatialEnvironment
from ..algorithms.neighbors import NeighborsFinder

BACKGROUND_COLOR = (0, 0, 0)


class GridEnvironment(SpatialEnvironment):
    def __init__(self,box_size = 10,width = 100,height = 60,objects = None):


        # Grid Environment parameters
        self.width = width
        self.height = height
        self.box_size = box_size
        self.setup_screen()

        # Objects initialization
        self._objects = {}
        self.add_object(objects)

        # Init objects data
        self.set_data()


    def quit(self):
        pygame.quit()


    @property
    def data(self):
        return self._data


    @property
    def objects(self):
        return list(self._objects.values())


    def get_object(self,object_id):
        return self._objects[object_id]

    def remove_object(self,object_id):
        if isinstance(object_id,str):
            return self._objects.pop(object_id)
        else:
            return self._objects.pop(object_id.id)


    def add_object(self,obj):

        if obj is not None:

            # If we add a list of objects, using recursive function to add each object
            if isinstance(obj,list):
                for o in obj:
                    self.add_object(o)
                
            # Add object 
            else:
                self._objects[obj.id] = obj
                

    #=================================================================================
    # COLLIDERS
    #=================================================================================


    def correct_offscreen_move(self,x,y):

        env_width = self.width
        env_height = self.height

        # Check with x
        if x > env_width:
            new_x = 0
        elif x < 0:
            new_x = env_width
        else:
            new_x = x

        # Check with y
        if y > env_height:
            new_y = 0
        elif y < 0:
            new_y = env_height
        else:
            new_y = y

        return new_x,new_y


    def is_object_colliding(self,obj):
        is_collision,_ = obj.collides_with(self.objects)
        return is_collision


    #=================================================================================
    # SPAWNERS
    #=================================================================================



    def spawn(self,spawner,n,overlap = False,**kwargs):

        # Spawn n elements (works also with n = 1)
        for i in range(n):

            spawned = False

            while not spawned:

                # Generate random position
                x = np.random.randint(0,self.width)
                y = np.random.randint(0,self.height)

                # Spawn new object using spawner
                # Pass also kwargs to spawner
                obj = spawner(x,y,**kwargs)

                # If we don't care about overlapping when spawning
                # Just add new object to the queue 
                if overlap:
                    spawned = True
                    self.add_object(obj)

                # If we don't want overlapping, we use collisions to spawn efficiently new objects
                else:
                    if not self.is_object_colliding(obj):
                        spawned = True
                        self.add_object(obj)

        # Append to data
        self.set_data()





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
        mesh[tuple(np.array(positions).T)] = 1

        return mesh




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
        self.neighbors_finder = NeighborsFinder(self._data)




    #=================================================================================
    # OBJECTS MANIPULATION
    #=================================================================================



    def find_neigbors(self,range):
        pass


    def find_objects_in_range(self,obj,search_range = None):
        # TODO add parameters to only find objects that matters
        # For example not using obstacles
        
        objects = self.neighbors_finder.find(obj,search_range)

        return objects




    #=================================================================================
    # ENV LIFECYCLE
    #=================================================================================


    def step(self):

        # Iterate for each object
        for agent in self.objects:

            # Only step with non static objects: ie agents
            if agent.static == False:
                agent.step(self)
                agent.clocktick()

        # Reinitialize data
        self.set_data()


    #=================================================================================
    # RENDERERS
    #=================================================================================

    def setup_screen(self):

        # Init pygame window
        pygame.init()
        pygame.display.set_caption("Westworld environment")

        self.screen = pygame.display.set_mode((
            self.width * self.box_size,
            self.height * self.box_size
            ))

        self.reset_screen()


    def reset_screen(self):
        self.screen.fill(BACKGROUND_COLOR)



    def render(self):

        self.reset_screen()

        for el in self.objects:
            el.render(self)

        pygame.display.update()



    def get_frame(self):
        return pygame.surfarray.array3d(self.screen).swapaxes(0,1)


    def get_img(self):
        img = self.get_frame()
        return Image.fromarray(img)


    def save_img(self,filepath):
        img = self.get_img()
        img.save(filepath)


        




        

        





        


