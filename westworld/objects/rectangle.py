

import numpy as np
import pygame
import itertools

from .base_object import BaseObject
from ..colors import *



class BaseRectangle(BaseObject):

    def __init__(self,x,y,width = 1,height = 1,color = (255,0,0),circle = False,radius = None):
        
        super().__init__()

        self._x = x
        self._y = y
        self.width = width
        self.height = height
        self.color = color
        self.circle = circle
        self._radius = radius


    def _init_sprite_internals(self):

        # Sprite init
        self.image = pygame.Surface(self.size)
        self.image.set_colorkey((0,0,0))
        self.image.fill(self.color)
        self.rect = self.get_rect()
        self.mask = pygame.mask.from_surface(self.image)


    def __repr__(self):
        return f"Rectangle({self.x},{self.y},size=({self.width},{self.height}))"


    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y


    @x.setter
    def x(self, value):
        self._x = value
        self.rect.x = value * self.cell_size


    @y.setter
    def y(self, value):
        self._y = value
        self.rect.y = value * self.cell_size
    


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
    def dimensions(self):
        return (
            self.x * self.cell_size,
            self.y * self.cell_size,
            *self.size,
        )

    @property
    def size(self):
        return (
            self.width * self.cell_size,
            self.height * self.cell_size,
        )


    @property
    def radius(self):
        if self._radius is None:
            assert self.width == self.height
            return self.width/2
        else:
            return self._radius


    @property
    def center(self):
        radius = self.radius
        return (
            int(self.x * self.cell_size + radius),
            int(self.y * self.cell_size + radius),
        )


    def get_rect(self,x = None,y = None):
        if x is None: x = self.x
        if y is None: y = self.y
        return pygame.rect.Rect((x*self.cell_size,y*self.cell_size,*self.size))


    # def get_collider(self,x,y):
    #     dimensions = (
    #         x * self.cell_size,
    #         y * self.cell_size,
    #         self.width * self.cell_size,
    #         self.height * self.cell_size
    #     )
    #     return pygame.rect.Rect(dimensions)


    # def get_sprite(self,x,y):
    #     sprite = self.sprite
    #     sprite.rect = self.get_collider(x,y)
    #     return sprite




    @property
    def collider(self):
        return pygame.rect.Rect(self.dimensions)


    # @property
    # def sprite(self):
    #     sprite = pygame.sprite.Sprite()
    #     sprite.image = pygame.Surface(self.dimensions[-2:])
    #     sprite.image.set_colorkey((0,0,0))
    #     sprite.image.fill(self.color)
        
    #     # Prepare mask and rect
    #     sprite.rect = self.collider
    #     sprite.mask = pygame.mask.from_surface(sprite.image)
    #     return sprite

        
        

    @property
    def cell_size(self):
        if hasattr(self,"_cell_size"):
            return self._cell_size
        else:
            raise Exception("Object must be added to an environment first to setup box size")


    def set_env(self,env):
        self._env = env

        if hasattr(env,"cell_size"):
            self._cell_size = env.cell_size
            self._init_sprite_internals()





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


    # def collides_with(self,others,x = None,y = None):
    #     """Compute collisions between the object and any other objects
    #     Returns if there is a collision + the list of object ids in collision
    #     """

    #     # In the absence of external colliders
    #     # We take the internal collider
    #     if x is None and y is None:
    #         collider = self.collider
    #         sprite = self.sprite
    #     else:
    #         collider = self.get_collider(x,y)
    #         sprite = self.get_sprite(x,y)

        
    #     # If no other colliders
    #     if len(others) == 0:
    #         collisions = []

    #     # Compute collisions using PyGame
    #     else:
    #         other_colliders = [(other.id,other.collider) for other in others if (other.id != self.id and other.blocking)]
    #         if len(other_colliders) > 0:
    #             ids,other_colliders = list(zip(*other_colliders))
    #             collisions = collider.collidelistall(other_colliders)
    #             collisions = [ids[i] for i in collisions]
    #         else:
    #             collisions = []

    #     # Compute collisions with obstacle layer group using pixel perfect collision
    #     if self.env.has_layers:
    #         layer_collisions = pygame.sprite.spritecollide(sprite,self.env._obstacle_layer_group,False,pygame.sprite.collide_mask)
    #         if len(layer_collisions) > 0:
    #             collisions.append("obstacle_layer")

    #     # Return signal of collision and colliders touched
    #     if len(collisions) > 0:
    #         return True,collisions
    #     else:
    #         return False,collisions





    #=================================================================================
    # RENDERERS
    #=================================================================================




    def render(self,screen = None):
        """Render function to visualize object in the environment
        Visualize either a circle or square in any color
        Vision range can be visualized as well

        TODO: 
            - Improve visualization not only within PyGame
            - Visualize with Sprites as well in PyGame 
        """

        if screen is None:
            screen = self.env.screen

        if not self.circle:
            # Draw a rectangle on the grid using pygame
            self.render_rect(screen = screen,color=self.color)
            # pygame.draw.rect(screen,self.color,self.dimensions)

        else:
            self.render_circle(screen = screen,color=self.color)
            # Draw a circle on the grid using pygame
            # pygame.draw.circle(screen,self.color,self.center,self.radius)


        # if hasattr(self,"vision_range") and self.vision_range is not None:
        #     if hasattr(self,"show_vision_range"):
        #         if self.show_vision_range:
        #             pygame.draw.circle(screen,WHITE,self.center,int(self.vision_range * self.cell_size),1)

