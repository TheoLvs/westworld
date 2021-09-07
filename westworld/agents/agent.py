
import numpy as np
import random
import pygame

from ..objects.rectangle import BaseRectangle
from ..algorithms.pathfinding.astar import AStar
from ..algorithms.neighbors import NeighborsFinder


class BaseAgent(BaseRectangle):
    def __init__(self,x,y,width = 1,height = 1,color = (255,0,0),circle = False,diagonal = False,
    curiosity = 20,search_radius = 2,speed = 5,
    active_pathfinding = 1.0,
    **kwargs,
    ):
        super().__init__(x,y,width,height,color,circle,**kwargs)


        # Movement description
        self.speed = speed
        self.diagonal = diagonal
        self.pathfinder = AStar(active_pathfinding)

        # Other characteristics
        self.set_direction()
        self.curiosity = curiosity
        self.search_radius = search_radius
 

    @property
    def stationary(self):
        return False




    #=================================================================================
    # MOVEMENTS
    #=================================================================================



    def set_direction(self,angle = None):
        if angle is None: angle = np.random.uniform(0,360)
        self.angle = angle


    def turn(self,angle):
        self.angle += angle


    def explore(self):
        pass


    def when_blocked(self,collisions):
        pass

    def wander(self):

        if self.on_grid:
            # Move using an unit movement (adjacent squares only) but more or less in the direction given by the angle
            dx,dy = self._sample_unit_movement_from_angle(self.angle)
            self.move(dx = dx,dy = dy)

        else:
            self.move(speed = self.speed)

        # Change direction based on curiosity value
        if self.clock > 1 and self.clock % self.curiosity == 0:
            self.set_direction()



    @staticmethod
    def _sample_unit_movement_from_angle(angle):
        # TODO does not allow diagonal movement for now
        
        # Compute cos and sin
        x = np.cos(angle)
        y = np.sin(angle)
        
        # Test conditions
        if x == 0.0:
            return (0,y)
        elif y == 0.0:
            return (x,0)
        
        # Compute signs
        sign_x = x / np.abs(x)
        sign_y = y / np.abs(y)
        
        # Compute absolute values and probabilities
        x,y = np.abs([x,y])


        #-----------------
        # Other option here is as followed
        # First experiments show it's a little slower (0.1 us)
        # yet it's maybe more generalizable
        # py = y / (x+y)
        
        # # Compute dx and dy based on probabilities
        # dy = np.random.binomial(1,py)
        # dx = 1 - dy
        
        # # Add signs
        # dx *= sign_x
        # dy *= sign_y

        # Draw values between 0 and x,y
        xd = np.random.uniform(0,x)
        yd = np.random.uniform(0,y)
        
        if xd > yd:
            return (sign_x,0)
        else:
            return (0,sign_y)


    def follow_direction(self,dr = 1):
        # Will be more suitable for a navigation agent implemented in a future class
        # Grid agent can only move in adjacent squares, eventually diagonals
        return self.move(angle = self.angle,dr = dr)


    def move_at(self,x,y):
        dx = x - self.x
        dy = y - self.y 
        self.move(dx = dx,dy = dy)



    def find_path_towards(self,x = None,y = None,obj = None,n = None):

        # Start position
        start_pos = self.pos_array[0]

        # Prepare target position
        if obj is not None:
            if isinstance(obj,str):
                obj = self.env[obj]
            target_pos = obj.pos_array[0]
        else:
            target_pos = y,x

        if self.pathfinder.needs_recompute(start_pos,target_pos):

            # Prepare mesh
            mesh = self.env.get_navigation_mesh(self)

            # Find path
            path = self.pathfinder.run(mesh,start_pos,target_pos,diagonal=self.diagonal,n=n)
            return path
        
        else:
            return self.pathfinder.last_path


    def move_towards(self,x = None,y = None,obj = None,n = None,naive = False):
        """Movement function, during one step the agent will move towards a target position or object using pathfinding
        """


        if obj is None:
            if self.pos == (x,y):
                return True
        else:

            # If given object is a string, we retrieve the object from the inventory using the id
            # Returns an error if the object id is not in the inve  ntory
            if isinstance(obj,str): obj = self.env[obj]

            if self.pos == obj.pos:
                return True

            x,y = obj.pos


        # TODO add in naive pathfinding
        if naive:
            MOVES = []
            if self.x > x:
                MOVES.append((-1,0))
            elif self.x < x:
                MOVES.append((1,0))
            if self.y > y:
                MOVES.append((0,-1))
            elif self.y < y:
                MOVES.append((0,1))

            dx,dy = random.choice(MOVES)
            self.move(dx,dy)

        else:

            # Find path with pathfinding algorithm
            path = self.find_path_towards(x,y,obj,n)

            # Move to next position in the path
            # First element is the current position
            # Warning coordinates are reversed in numpy arrays
            if path is not None:
                if len(path) > 1:
                    y,x = path[1]
                    self.move_at(x,y)
                    return False
                else:
                    return False


    def follow_mouse(self,n = None):
        """Movement function, during one step the agent will follow the mouse position using pathfinding
        """
        x,y = pygame.mouse.get_pos()
        x = x // self.cell_size
        y = y // self.cell_size
        self.move_towards(x = x,y = y,n = n)


    def move(self,dx:int = 0,dy:int = 0,speed:float = None,angle:float = None) -> bool:
        """Movement main function, moves an agent to a new location
        Movement can either be launched with:
            1/ a delta x and y (useful in grid environments) (if speed is None)
            2/ Or using a given speed and angle (useful in spatial environments) (if speed is given)

        The movement will be blocked if the object has a blocking property == True
        and enters a collision given by self.collides()

        Args:
            dx (int, optional): Delta x for the movement. Defaults to 0.
            dy (int, optional): Delta y for the movement. Defaults to 0.
            speed (float, optional): Speed for the angular movement. Defaults to None.
            angle (float, optional): Angle for the movement. Defaults to None.

        Returns:
            bool: [description]
        """

        # Store default values for collisions
        is_collision = False

        if speed is not None:
            if angle is None: angle = self.angle
            angle = 2* np.pi * angle / 360 #- 0.5 * np.pi
            dx = int(speed * np.cos(angle))
            dy = - int(speed * np.sin(angle)) # Negative because y axis is inverted

            self.move(dx = dx,dy = dy)

        # Move using radial movement (with angle and radius)
        elif angle is not None:

            cell_size = self.cell_size

            # Compute delta directions with basic trigonometry
            # In a grid environment, movement is rounded to the integer to fit in the grid
            dx = int(speed * cell_size * np.cos(angle))
            dy = int(speed * cell_size * np.sin(angle))

            return self.move(dx = dx,dy = dy)

        # Move using euclidean movement (with dx and dy)
        else:

            # Store old position
            old_pos = self.x,self.y
                
            # Store movements
            x = int(self.x + dx)
            y = int(self.y + dy)

            # Correct moves going offscreen
            # TODO use this function only in toroidal environments
            x,y = self.env.wrap_in_toroidal_envs(x,y)

            # Store new positions as attributes
            self.x = x
            self.y = y

            # Compute collisions
            collisions = self.collides()
            is_collision = len(collisions) > 0

            # If in collision, cancel movement and trigger block callback
            if is_collision:
                self.x,self.y = old_pos
                self.when_blocked(collisions)

        return is_collision




    def random_walk(self):

        if self.diagonal:

            # Sample a random move between -1, 0 or + 1
            # ie 8 moves around agent's position
            dx,dy = np.random.randint(0,3,2) - 1

        else:
            dx,dy = random.choice([(1,0),(-1,0),(0,1),(0,-1)])


        self.move(dx,dy)



    #=================================================================================
    # FINDER
    #=================================================================================


    def find_closest(self,k = 1,**kwargs):

        # Get objects data we want to search
        objects_data = self.env.find(return_data = True,**kwargs)
        objects_data = objects_data.drop(self.id,errors = "ignore")
        
        if len(objects_data) == 0:
            distances,ids = [],[]
        else:
            # Create neighbors algorithm
            finder = NeighborsFinder(objects_data)
            distances,ids = finder.find_closest(self,k = k)

        return ids


    def find(self,return_objects = True,**kwargs):
        return self.env.find(return_objects = return_objects,**kwargs)


    def find_in_range(self,radius = None,method = "circle",**kwargs):
        # TODO add parameters to only find objects that matters
        # For example not using obstacles
        # Easily done by appending to condition to add obstacles = False

        if radius is None:
            radius = self.search_radius
            assert radius is not None

        group = pygame.sprite.Group()
        
        objs = self.env.find(return_objects = True,**kwargs)
        group.add(*objs)

        search = self.collides_group(group,method = method,ratio = radius)
        return search


        # # Find objects data
        # objects_data = self.env.find_objects(condition = condition,return_data = True)
        # objects_data = objects_data.drop(self.id,errors = "ignore")

        # if len(objects_data) == 0:
        #     return []
        # else:
        #     # Create finder algorithm
        #     finder = NeighborsFinder(objects_data)
        #     ids = finder.find_in_range(self,search_range)

        #     return ids
