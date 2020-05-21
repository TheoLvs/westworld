
import numpy as np
import pygame

from .rectangle import BaseRectangle
from ...algorithms.pathfinding.astar import AStar
from ...algorithms.neighbors import NeighborsFinder


class BaseAgent(BaseRectangle):
    def __init__(self,x,y,width = 1,height = 1,color = (255,0,0),circle = False,diagonal = False,
    curiosity = 20,vision_range = None,
    ):
        super().__init__(x,y,width,height,color,circle)


        # Movement description
        self.diagonal = diagonal
        self.pathfinder = AStar()

        # Other characteristics
        self.set_direction()
        self.curiosity = curiosity
        self.vision_range = vision_range
 

    @property
    def stationary(self):
        return False


    def __repr__(self):
        return f"Agent(x={self.x},y={self.y})"



    #=================================================================================
    # MOVEMENTS
    #=================================================================================

    def set_direction(self):
        self.direction_angle = np.random.uniform(0,2*np.pi)


    def _angle_generator(self):
        # Not sure it's the right way to do, control is not easy with generators
        i = 0
        while True:
            if i % self.curiosity == 0:
                angle = np.random.uniform(0,2*np.pi)
            i += 1
            yield angle

    def explore(self):
        pass

    def wander(self):

        # Move using an unit movement (adjacent squares only) but more or less in the direction given by the angle
        dx,dy = self._sample_unit_movement_from_angle(self.direction_angle)
        self.move(dx = dx,dy = dy)

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
        return self.move(angle = self.direction_angle,dr = dr)


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
        
        # Prepare mesh
        mesh = self.env.get_navigation_mesh(self)

        # Find path
        path = self.pathfinder.run(mesh,start_pos,target_pos,diagonal=self.diagonal,n=n)
        return path


    def move_towards(self,x = None,y = None,obj = None,n = None):

        # Find path with pathfinding algorithm
        path = self.find_path_towards(x,y,obj,n)

        # Move to next position in the path
        # First element is the current position
        # Warning coordinates are reversed in numpy arrays
        if path is not None:
            if len(path) > 1:
                y,x = path[1]
                self.move_at(x,y)
            else:
                pass


    def move(self,dx = 0,dy = 0,angle = None,dr = None):

        # Store default value for collisions
        is_collision = False

        # Move using radial movement (with angle and radius)
        if angle is not None:

            box_size = self.box_size

            # Compute delta directions with basic trigonometry
            # In a grid environment, movement is rounded to the integer to fit in the grid
            dx = int(dr * box_size * np.cos(angle))
            dy = int(dr * box_size * np.sin(angle))

            return self.move(dx = dx,dy = dy)

        # Move using euclidean movement (with dx and dy)
        else:
                
            # Store movements
            x = self.x + dx
            y = self.y + dy

            # Correct moves going offscreen
            # TODO use this function only in toroidal environments
            x,y = self.env.correct_offscreen_move(x,y)

            # Compute collisions
            collider = self.get_collider(x,y)
            is_collision,_ = self.collides_with(self.env.objects,collider = collider)

            if not is_collision:

                # Store new positions as attributes
                self.x = x
                self.y = y

                    


        return is_collision




    def random_walk(self):

        # Sample a random move between -1, 0 or + 1
        # ie 8 moves around agent's position
        dx,dy = np.random.randint(0,3,2) - 1
        self.move(dx,dy)



    #=================================================================================
    # FINDER
    #=================================================================================


    def find_closest(self,k = 1,condition = None):

        # Get objects data we want to search
        objects_data = self.env.find_objects(condition = condition,return_data = True)
        objects_data = objects_data.drop(self.id,errors = "ignore")
        
        if len(objects_data) == 0:
            return [],[]
        else:
            # Create neighbors algorithm
            finder = NeighborsFinder(objects_data)
            distances,ids = finder.find_closest(self,k = k)

            return distances,ids




    def find_in_range(self,search_range = None,condition = None):
        # TODO add parameters to only find objects that matters
        # For example not using obstacles
        # Easily done by appending to condition to add obstacles = False

        if search_range is None:
            search_range = self.vision_range
            assert self.vision_range is not None

        # Find objects data
        objects_data = self.env.find_objects(condition = condition,return_data = True)
        objects_data = objects_data.drop(self.id,errors = "ignore")

        if len(objects_data) == 0:
            return []
        else:
            # Create finder algorithm
            finder = NeighborsFinder(objects_data)
            ids = finder.find_in_range(self,search_range)

            return ids
