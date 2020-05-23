"""A* pathfinding algorithm implementation
Closely adapted from the work of : 
- Nicholas Swift https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
- Ryan Collinwood https://gist.github.com/ryancollingwood/32446307e976a11a1185a5394d6657bc (improvement on the latter example)
"""

import numpy as np
import random
import heapq
import warnings

from .pathfinding import Pathfinding,PathfindingError



class Node:
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


    def __repr__(self):
        return f"{self.position} - g: {self.g} h: {self.h} f: {self.f}"

    # defining less than for purposes of heap queue
    def __lt__(self, other):
        return self.f < other.f
    
    # defining greater than for purposes of heap queue
    def __gt__(self, other):
        return self.f > other.f



class AStar(Pathfinding):

    def __init__(self,proba_recompute = 1.0):


        # Probability to recompute the path at each step
        # 1 represents active pathfinding where we recompute at each step
        self.proba_recompute = float(proba_recompute)
        assert 0 <= self.proba_recompute <= 1

        self.last_target = (-1,-1)
        self.last_path = []


    def needs_recompute(self,start_pos,target_pos):

        # If active pathfinding
        if self.proba_recompute == 1:
            return True

        # If target is the same, draw a random float to see if we recompute 
        elif target_pos == self.last_target:
            return random.random() < self.proba_recompute

        # If target is different we of course needs to recompute
        else:
            return True


    def return_path(self,current_node):
        path = []
        current = current_node
        while current is not None:
            path.append(current.position)
            current = current.parent

        # Return reversed path
        path = path[::-1]

        # Store last path found
        self.last_path = path
        
        return path


    def run(self,mesh,start,end,diagonal = False,n = None):
        """Returns a list of tuples as a path from the given start to the given end in the given mesh
        Base implementation is drawn from Nicholas Swift work explained at https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2

        TODO - This can probably be a lot accelerated by numba and or cython
        TODO - Requires for westworld env to have a get_nav_mesh() method extracting numpy array
        TODO - Will only work if grid environment, yet possible to discretize env if needed
        TODO - Add stop at n iterations to fasten computation
        """

        # Safety check
        try:
            mesh[start],mesh[end]
        except IndexError as e:
            raise PathfindingError(f"Start or end not in the mesh: {e}")

        # Create start and end node
        start_node = Node(None, start)
        end_node = Node(None, end)

        # Store last target
        self.last_target = end

        # Get adjacent moves
        moves = self.get_adjacent_moves(diagonal)

        # Initialize both open and closed list
        open_list = []
        closed_list = []

        # Heapify the open_list and Add the start node
        heapq.heapify(open_list) 
        heapq.heappush(open_list, start_node)

        # Adding a stop condition
        outer_iterations = 0
        max_iterations = np.product(mesh.shape)
        if n is not None:
            max_iterations = min([max_iterations,n])

        # Loop until you find the end
        while len(open_list) > 0:

            outer_iterations += 1

            # Get the current node
            current_node = heapq.heappop(open_list)
            closed_list.append(current_node)

            if outer_iterations > max_iterations:
                # if we hit this point return the path such as it is
                # it will not contain the destination
                warnings.warn("Giving up on pathfinding too many iterations")
                return self.return_path(current_node)     

            # Found the goal
            if current_node == end_node:
                return self.return_path(current_node)

            # Generate children
            children = []
            
            for new_position in moves: # Adjacent squares

                # Get node position
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                # Make sure within range
                if node_position[0] > (len(mesh) - 1) or node_position[0] < 0 or node_position[1] > (len(mesh[len(mesh)-1]) -1) or node_position[1] < 0:
                    continue

                # Make sure walkable terrain
                if mesh[node_position[0]][node_position[1]] != 0:
                    continue

                # Create new node
                new_node = Node(current_node, node_position)

                # Append
                children.append(new_node)

            # Loop through children
            for child in children:
                # Child is on the closed list
                if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                    continue

                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h

                # Child is already in the open list
                if len([open_node for open_node in open_list if child.position == open_node.position and child.g > open_node.g]) > 0:
                    continue

                # Add the child to the open list
                heapq.heappush(open_list, child)

        warnings.warn("Couldn't get a path to destination")
        return None