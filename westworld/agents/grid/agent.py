
import numpy as np
import pygame

from .rectangle import Rectangle
from ...algorithms.pathfinding.astar import AStar


class GridAgent(Rectangle):
    def __init__(self,x,y,width = 1,height = 1,box_size = None,color = (255,0,0),circle = False,diagonal = False,
    curiosity = 20,vision_range = None,
    ):
        super().__init__(x,y,width,height,box_size,color,circle)


        # Movement description
        self.diagonal = diagonal
        self.pathfinder = AStar()

        # Other characteristics
        self.set_direction()
        self.curiosity = curiosity
        self.vision_range = vision_range
 

    @property
    def static(self):
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

    def wander(self,env = None):

        # Move using an unit movement (adjacent squares only) but more or less in the direction given by the angle
        dx,dy = self._sample_unit_movement_from_angle(self.direction_angle)
        self.move(dx = dx,dy = dy,env = env)

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


    def follow_direction(self,dr = 1,env = None):
        # Will be more suitable for a navigation agent implemented in a future class
        # Grid agent can only move in adjacent squares, eventually diagonals
        return self.move(angle = self.direction_angle,dr = dr,env = env)


    def move_at(self,x,y,env = None):
        dx = x - self.x
        dy = y - self.y 
        self.move(dx = dx,dy = dy,env = env)



    def find_path_towards(self,x = None,y = None,obj = None,env = None,n = None):

        # Start position
        start_pos = self.pos_array[0]

        # Prepare target position
        if obj is not None:
            target_pos = obj.pos_array[0]
        else:
            target_pos = y,x
        
        # Prepare mesh
        mesh = env.get_navigation_mesh(self)

        # Find path
        path = self.pathfinder.run(mesh,start_pos,target_pos,diagonal=self.diagonal,n=n)
        return path


    def move_towards(self,x = None,y = None,obj = None,env = None,n = None):

        # Find path with pathfinding algorithm
        path = self.find_path_towards(x,y,obj,env,n)

        # Move to next position in the path
        # First element is the current position
        # Warning coordinates are reversed in numpy arrays
        if path is not None:
            if len(path) > 1:
                y,x = path[1]
                self.move_at(x,y,env = env)
            else:
                pass


    def move(self,dx = 0,dy = 0,angle = None,dr = None,env = None):

        # Store default value for collisions
        is_collision = False

        # Move using radial movement (with angle and radius)
        if angle is not None:

            box_size = 1 if env is None else env.box_size

            # Compute delta directions with basic trigonometry
            # In a grid environment, movement is rounded to the integer to fit in the grid
            dx = int(dr * box_size * np.cos(angle))
            dy = int(dr * box_size * np.sin(angle))

            return self.move(dx = dx,dy = dy,env = env)

        # Move using euclidean movement (with dx and dy)
        else:

            if env is None: 
                
                # If movement is not bounded by environment
                # We update position without constraints
                self.x += dx
                self.y += dy

            else:
                
                # Store movements
                x = self.x + dx
                y = self.y + dy

                # Correct moves going offscreen
                x,y = env.correct_offscreen_move(x,y)

                # Compute collisions
                collider = self.get_collider(x,y)
                is_collision,_ = self.collides_with(env.objects,collider = collider)

                if not is_collision:

                    # Store new positions as attributes
                    self.x = x
                    self.y = y

                    


        return is_collision




    def random_walk(self,env = None):

        # Sample a random move between -1, 0 or + 1
        # ie 8 moves around agent's position
        dx,dy = np.random.randint(0,3,2) - 1
        self.move(dx,dy,env = env)



