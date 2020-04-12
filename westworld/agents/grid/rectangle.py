

import numpy as np
import pygame
import itertools

from ..base_object import BaseObject
from ...colors import *



class Rectangle(BaseObject):

    def __init__(self,x,y,width,height,box_size,color,circle = False):
        
        super().__init__()

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.box_size = box_size
        self.color = color
        self.circle = circle



    def __repr__(self):
        return f"Rectangle(x={self.x},y={self.y},w={self.width},h={self.height})"


    @property
    def value(self):
        return 1


    @property
    def pos(self):
        return self.x,self.y


    @property
    def pos_array(self):
        # TODO see if faster not as property but attribute
        xs = range(self.x,self.x + self.width)
        ys = range(self.y,self.y + self.height)

        pos = list(itertools.product(ys,xs))
        return pos


    @property
    def static(self):
        return True


    @property
    def blocking(self):
        return True

    @property
    def dimensions(self):
        return (
            self.x * self.box_size,
            self.y * self.box_size,
            self.width * self.box_size,
            self.height * self.box_size
        )


    @property
    def radius(self):
        assert self.width == self.height
        return int((self.width * self.box_size)/2)


    @property
    def center(self):
        radius = self.radius
        return (
            int(self.x * self.box_size + radius),
            int(self.y * self.box_size + radius),
        )

    @property
    def collider(self):
        return pygame.rect.Rect(self.dimensions)


    def get_collider(self,x,y):
        dimensions = (
            x * self.box_size,
            y * self.box_size,
            self.width * self.box_size,
            self.height * self.box_size
        )
        return pygame.rect.Rect(dimensions)



    def get_data(self):
        data = {
            "id":self.id,
            "pos":self.pos,
            "type":self.__class__.__name__
        }
        
        if hasattr(self,"attrs"):
            data = {
                **data,
                **{key:getattr(self,key) for key in self.attrs}
            }
        
        return data



    #=================================================================================
    # MOVEMENT
    #=================================================================================

    def move(self,*args,**kwargs):
        pass

    def step(self,*args,**kwargs):
        pass


    def collides_with(self,others,collider = None):

        # In the absence of external colliders
        # We take the internal collider
        if collider is None:
            collider = self.collider
        
        # If no other colliders
        if len(others) == 0:
            collisions = []

        # Compute collisions using PyGame
        else:
            other_colliders = [other.collider for other in others if (other.id != self.id and other.blocking)]
            collisions = collider.collidelistall(other_colliders)

        # Return signal of collision and colliders touched
        if len(collisions) > 0:
            return True,collisions
        else:
            return False,collisions





    #=================================================================================
    # RENDERERS
    #=================================================================================


    def render(self,env):

        if not self.circle:
            # Draw a rectangle on the grid using pygame
            pygame.draw.rect(env.screen,self.color,self.dimensions)

        else:

            # Draw a circle on the grid using pygame
            pygame.draw.circle(env.screen,self.color,self.center,self.radius)


        if hasattr(self,"vision_range") and self.vision_range is not None:
            if hasattr(self,"show_vision_range"):
                if self.show_vision_range:
                    pygame.draw.circle(env.screen,WHITE,self.center,int(self.vision_range * self.box_size),1)

