

import uuid
import pygame
from pygame.sprite import Sprite

from ..exceptions import ObjectNotBoundError



class BaseObject(Sprite):
    """Default Object serving as base for each agent evolving in environments
    """
    def __init__(self):

        # Init base sprite class
        super().__init__()

        # Create id and clock
        self.id = str(uuid.uuid1())
        self._clock = 0

        # Init function to be overridden
        self.init()


    @property
    def clock(self):
        """Default internal clock for each object
        """
        return self._clock

    def clocktick(self):
        """Helper function to increment internal clock
        """
        self._clock += 1


    def kill(self):
        self.env.remove_object(self)


    @property
    def env(self):
        """Environment linked to the object
        """
        if self.is_bound():
            return self._env
        else:
            raise ObjectNotBoundError("The object must be attached to an environment")


    def is_bound(self):
        return hasattr(self,"_env")


    def bind(self,env):
        """Default setter function
        """
        self._env = env


    def init(self):
        """Default init function 
        Can be overriden in special objects
        """
        pass


    @property
    def on_grid(self):
        return self.env.is_grid

    @property
    def stationary(self):
        return True

    @property
    def blocking(self):
        return True

    @property
    def trigger(self):
        return False

    @property
    def collectible(self):
        return False

    @property
    def radius(self):
        return 1



    @property
    def layer(self):
        return False


    @property
    def obstacle(self):
        return self.stationary and self.blocking



    def collides(self) -> list:
        """Returns if an object collides with any objects in the environment
        Needs to be binded to an environment of course
        The function will computes collisions against:
            - Rectangular or circle collisions with the blocking sprite group
            - Mask collisions with the layer sprite group
            - Rectangular collisions with the trigger sprite group

        TODO:
        Could be improved to account for trigger layers

        Returns:
            list: List of objects in collisions, empty if no collision
        """
        

        collisions = []

        # Find all rect collisions
        if self.env.has_blocking():
            c = self.collides_group(self.env.group_blocking,method = self.collision_method)
            collisions.extend(c)

        # Find all mask collisions
        if self.env.has_layers():
            c = self.collides_group(self.env.group_layers,method = "mask")
            collisions.extend(c)

        if self.env.has_triggers():
            triggers = self.collides_group(self.env.group_triggers,method = "rect")
            for trigger in triggers:
                trigger.on_collision(self)

        return collisions




    def collides_group(self,group:pygame.sprite.Group, method:str = "rect", ratio:float = None) -> list:
        """Collision helper functions, computes if an object enters a collision with a sprite group
        Three methods are available (rect, circle and mask)

        Args:
            group (pygame.sprite.Group): The target sprite group on which to test collisions
            method (str, optional): Collision method, either rectangular, circular or using a pixel perfect mask. Defaults to "rect".
            ratio (float, optional): Apply a ratio around the center of the object, useful to get collisions in a circle range. Defaults to None.

        Returns:
            list: List of objects in collisions, empty if no collision
        """

        # Verify method is in acceptable values
        assert method in ["rect","circle","mask"]

        # Rectangular collider
        if method == "rect":
            if ratio is None:
                collisions = pygame.sprite.spritecollide(self,group,False)
            else:
                collisions = pygame.sprite.spritecollide(self,group,False,pygame.sprite.collide_rect_ratio(ratio))

        # Circle collider
        elif method == "circle":
            # Warning, to check ratio works with rect but for circle 
            # We need to add the cell_size, maybe works as a radius and not a ratio

            if ratio is  None:
                collisions = pygame.sprite.spritecollide(self,group,False,pygame.sprite.collide_circle)
            else:
                ratio = ratio * self.env.cell_size
                collisions = pygame.sprite.spritecollide(self,group,False,pygame.sprite.collide_circle_ratio(ratio))

        # Mask collider
        elif method == "mask":
            collisions = pygame.sprite.spritecollide(self,group,False,pygame.sprite.collide_mask)

        # Filter to remove self object from collisions 
        collisions = [x for x in collisions if x.id != self.id]

        return collisions


    def render_circle(self,x = None,y = None,radius = None,color = None,screen = None,thickness = 0,cell_size = None):

        # Default arguments
        if x is None: x = self.x
        if y is None: y = self.y
        if color is None: color = self.color
        if screen is None: screen = self.env.screen
        if cell_size is None: cell_size = self.env.cell_size
        if radius is None: radius = self.radius 

        # When in a grid, the center is normalized on cell size
        if cell_size is not None:
            x = int((x + 0.5) * cell_size)
            y = int((y + 0.5) * cell_size)
            radius = int(radius * cell_size)

        # Draw a circle on the grid using pygame
        pygame.draw.circle(screen,color,(x,y),radius,thickness)

    
    def render_image(self):
        pass

    
    def render_text(self,text,font = "Arial",size = 30,screen = None,color = (255,255,255)):
        
        x = self.x
        y = self.y
        cell_size = self.env.cell_size
        
        position = (
            int(x* cell_size),
            int(y* cell_size),
        )

        self.env.render_text(text,font,size,position,screen,color = color)



    def render_rect(self,x = None,y = None,width = None,height = None,radius = None,color = None,center = False,screen = None,cell_size = None,thickness = 0):

        # Default arguments
        if x is None: x = self.x
        if y is None: y = self.y
        if color is None: color = self.color
        if screen is None: screen = self.env.screen
        if cell_size is None: cell_size = self.env.cell_size
        if width is None: width = self.width
        if height is None: height = self.height
        if radius is not None:
            width = radius * 2
            height = radius * 2

        # Center the square on x,y or not
        if not center:
            dimensions = (x*cell_size,y*cell_size,width * cell_size,height*cell_size)
        else:
            dimensions = (
                int((x + 0.5 - 0.5 * width) * cell_size),
                int((y + 0.5 - 0.5 * height) * cell_size),
                width * cell_size,
                height * cell_size,
            )


        # Draw rectangle using pygame
        pygame.draw.rect(screen,color,dimensions,thickness)


    def render_img(self,image = None,x = None,y = None,screen = None,cell_size = None):

        if x is None: x = self.x 
        if y is None: y = self.y
        if cell_size is None: cell_size = self.env.cell_size
        if image is None: image = self.image
        if screen is None: screen = self.env.screen
        pos = (x * cell_size,y * cell_size)
        screen.blit(image,pos)
