
import numpy as np
import pygame

from .rectangle import Rectangle
from ...algorithms.pathfinding.astar import AStar


class GridAgent(Rectangle):
    def __init__(self,x,y,width = 1,height = 1,box_size = None,color = (255,0,0),circle = False,diagonal = False):
        super().__init__(x,y,width,height,box_size,color,circle)

        self.change_direction()

        # Movement description
        self.diagonal = diagonal
        self.pathfinder = AStar()


    @property
    def static(self):
        return False


    def __repr__(self):
        return f"Agent(x={self.x},y={self.y})"


    #=================================================================================
    # MOVEMENTS
    #=================================================================================

    def change_direction(self):
        self.direction_angle = np.random.uniform(0,2*np.pi)

    def follow_direction(self,dr = 1,env = None):
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
        y,x = path[1]
        self.move_at(x,y,env = env)


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



