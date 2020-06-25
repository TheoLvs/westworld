

import numpy as np
import pygame
import itertools
from PIL import Image

from .base_object import BaseObject
from ..colors import *
from ..assets import make_blob,make_ball,make_arrow



class BaseRectangle(BaseObject):

    def __init__(self,x,y,width = 1,height = 1,
        color = (255,0,0),circle = False,radius = None,
        img_filepath = None,img_transparency = (200, 191, 231),
        img_asset = None,
        img_rotate = False,
        ):
        
        super().__init__()

        self._x = x
        self._y = y
        self.width = width
        self.height = height
        self.color = color
        self.circle = circle
        self._radius = radius
        self.img_filepath = img_filepath
        self.img_asset = img_asset
        self.img_rotate = img_rotate

        if img_transparency is None and img_filepath is not None:
            self.img_transparency = np.array(Image.open(img_filepath))[0,0]
        else:
            self.img_transparency = img_transparency


    def init_internals(self,errors_binding = True):

        if not errors_binding:
            if not self.is_bound():
                return None

        # Create rectangle
        if self.img_filepath is not None:

            # Convert alpha instead of convert with transparent pictures
            self.image = pygame.image.load(self.img_filepath).convert()
            self.image.set_colorkey(self.img_transparency)
            self.rescale_img(width = self.width,height = self.height)

        elif self.img_asset is not None:
            assert self.img_asset in ["blob","ball","arrow"]

            if self.img_asset == "blob":
                img = make_blob(self.color,self.img_transparency)
            elif self.img_asset == "ball":
                lighter_fn = lambda x,t : min([255,int((1+t)*x)]) 
                color1 = self.color
                color2 = tuple([lighter_fn(x,0.6) for x in color1])
                img = make_ball(color1,color2,self.img_transparency)
            elif self.img_asset == "arrow":

                img = make_arrow(self.color,transparency = self.img_transparency)

            # Convert alpha instead of convert with transparent pictures
            self.image = pygame.surfarray.make_surface(img)
            self.image.set_colorkey(self.img_transparency)
            self.rescale_img(width = self.width,height = self.height)

            # Create image copy for rotation
            self.raw_image = self.image.copy()

        else:
            # Sprite init
            self.image = pygame.Surface(self.size)
            self.image.set_colorkey((0,0,0))
            self.image.fill(self.color)



        self.rect = self.get_rect()
        self.mask = pygame.mask.from_surface(self.image)


    def __repr__(self):
        return f"Rectangle({self.x},{self.y},size=({self.width},{self.height}))"

    def get_size_img(self):
        return self.image.get_size()

    def rescale_img(self,width,height = None):
        
        # Safety check to avoid rescaling layers
        if not self.layer:
                
            w,h = self.get_size_img()
            new_w = width * self.cell_size
            new_h = int(h*new_w/w) if height is None else height * self.cell_size
            self.image = pygame.transform.scale(self.image, (new_w,new_h))

    
    def rotate_img(self,angle:float) -> None:
        """Rotate the image by a given angle using Pygame Transform functions
        Documentation available here https://www.pygame.org/docs/ref/transform.html#pygame.transform.rotate
        Used to rotate sprites when turning

        Args:
            angle (float): Input angle in degrees for the rotation
        """

        self.image = pygame.transform.rotate(self.raw_image,angle)

    


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


    def bind(self,env):
        self._env = env
        self._cell_size = env.cell_size
        self.init_internals()





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


        if self.img_filepath is None and self.img_asset is None:

            if not self.circle:
                # Draw a rectangle on the grid using pygame
                self.render_rect(screen = screen,color=self.color)
                # pygame.draw.rect(screen,self.color,self.dimensions)

            else:
                self.render_circle(screen = screen,color=self.color)
                # Draw a circle on the grid using pygame
                # pygame.draw.circle(screen,self.color,self.center,self.radius)
    
        else:

            if self.img_rotate:
                self.rotate_img(self.angle)

            self.render_img(screen = screen)


        if hasattr(self,"show_search_radius") and self.show_search_radius:
            if hasattr(self,"search_radius_method") and self.search_radius_method == "rect":
                self.render_rect(screen = screen,color = WHITE,radius = self.search_radius,thickness = 1,center = True)
            else:
                self.render_circle(screen = screen,color = WHITE,radius = self.search_radius,thickness = 1)

