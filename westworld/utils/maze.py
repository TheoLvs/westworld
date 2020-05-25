
import os
import numpy as np
import matplotlib.pyplot as plt
from mazelib import Maze
from mazelib.generate.DungeonRooms import DungeonRooms
from mazelib.generate.Prims import Prims

from ipywidgets import interact,Dropdown,IntSlider
from PIL import Image


from .image import mesh_to_mask,mask_to_image3d



class MazeGenerator:
    """Helper class to generate mazes using mazelib
    """

    def __init__(self,width = 20,height = 20,cell_size = 20):
        
        self.width = width
        self.height = height 
        self.cell_size = cell_size
        self.maze = Maze()
        self.options = ["dungeon","prims"]

    @property
    def mesh(self):
        return self.maze.grid


    def make_mask(self):
        mask = mesh_to_mask(self.mesh,self.cell_size)
        # return mask
        img = mask_to_image3d(mask)#.astype(np.int8)
        return img


    def generate(self,method = ["dungeon"],rooms = None,width = None,height = None):

        if width is None: width = self.width
        if height is None: width = self.height

        if method == "dungeon":
            self.maze.generator = DungeonRooms(width,height, rooms=rooms)
        elif method == "prims":
            self.maze.generator = Prims(width,height)
        else:
            raise Exception(f"Maze generation method must be in {self.options}")

        self.maze.generate()



    def explore(self,**kwargs):


        @interact(
            method = Dropdown(desc = "Generation method",options = self.options),
            i = IntSlider(desc = "Generation",min = 0,max = 100,value = 0),
            width = IntSlider(desc = "Width",min = 10,max = 300,value = 20),
            height = IntSlider(desc = "Height",min = 10,max = 300,value = 20),
        )
        def show(method,i,width,height):

            self.generate(method = method,width = width,height = height,**kwargs)
            mesh = self.mesh
            plt.figure(figsize = (8,8))
            plt.imshow(mesh)
            plt.title("Generated maze")
            plt.show()



    def save(self,folder = "."):

        filename = "GeneratedMaze_cellsize={self.cell_size}.png"
        filepath = os.path.join(folder,filename)

        mask = self.make_mask()

        Image.fromarray(mask).save(filepath)

