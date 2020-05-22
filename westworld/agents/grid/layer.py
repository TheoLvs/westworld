
"""Layer Class

Three types of layers
- Obstacle Layer
- Trigger Layer
- Render Layer (does nothing more than display content)
"""

# Maybe inherit from Sprite also
# To be able to add in groups


import pygame
import numpy as np

from ..base_object import BaseObject
from ..sprite import BaseSprite
from ...utils.image import snap_mask_to_grid,image3d_to_mask,mask_to_image3d,aggregate_mask_to_grid

class BaseLayer(BaseSprite):
    def __init__(self,obstacle = True,trigger = False,mask_threshold = 0.1,*args,**kwargs):

        super().__init__(x = 0,y = 0,*args,**kwargs)

        self.mask = self.get_mask()
        self.mask_threshold = mask_threshold

        self.obstacle = obstacle
        self.trigger = trigger


    def get_img(self):
        return pygame.surfarray.array3d(self.sprite.image).swapaxes(0,1)

    def get_mask(self):
        img = self.get_img()
        return image3d_to_mask(img)


    def snap_to_grid(self):
        mask = snap_mask_to_grid(self.mask,self.env.box_size,self.mask_threshold)
        return mask


    def explore_snap_to_grid(self):
        pass


    def get_navigation_mesh(self):
        shape = (self.env.height,self.env.width)
        if self.obstacle:
            mesh = aggregate_mask_to_grid(self.mask,self.env.box_size,threshold=self.mask_threshold)
            assert mesh.shape == shape
            return mesh
        else:
            return np.zeros(shape)

