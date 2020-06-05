

import uuid
import pygame
from pygame.sprite import Sprite



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


    @property
    def env(self):
        """Environment linked to the object
        """
        if hasattr(self,"_env"):
            return self._env
        else:
            raise Exception("The object must be attached to an environment")


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



    def collides(self):

        collisions = []

        # Find all rect collisions
        if self.env.has_blocking():
            _,c = self.collides_group(self.env.group_blocking,method = "rect")
            collisions.extend(c)

        # Find all mask collisions
        if self.env.has_layers():
            _,c = self.collides_group(self.env.group_layers,method = "mask")
            collisions.extend(c)

        if self.env.has_triggers():
            _,triggers = self.collides_group(self.env.group_triggers,method = "rect")
            for trigger in triggers:
                trigger.on_collision(self)

        is_collision = len(collisions) > 0
        return is_collision,collisions




    def collides_group(self,group,method = "rect",ratio = None,radius = None):

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
            if ratio is  None:
                collisions = pygame.sprite.spritecollide(self,group,False,pygame.sprite.collide_circle)
            else:
                collisions = pygame.sprite.spritecollide(self,group,False,pygame.sprite.collide_circle_ratio(ratio))

        # Mask collider
        elif method == "mask":
            collisions = pygame.sprite.spritecollide(self,group,False,pygame.sprite.collide_mask)

        # Filter to remove self object from collisions 
        collisions = [x for x in collisions if x.id != self.id]
        is_collision = len(collisions) > 0

        return is_collision,collisions


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


    def render_rect(self,x = None,y = None,width = None,height = None,ratio = None,color = None,center = False,screen = None,cell_size = None,thickness = 0):

        # Default arguments
        if x is None: x = self.x
        if y is None: y = self.y
        if color is None: color = self.color
        if screen is None: screen = self.env.screen
        if cell_size is None: cell_size = self.env.cell_size
        if width is None: width = self.width
        if height is None: height = self.height
        if ratio is not None:
            width = ratio
            height = ratio

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
