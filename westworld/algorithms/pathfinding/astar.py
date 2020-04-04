"""A* pathfinding algorithm implementation
Inspired from the work of : 
- https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
"""

from .pathfinding import Pathfinding


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
        return f"{self.position}"




class AStar(Pathfinding):

    def __init__(self):
        pass


    def run(self,array,start,end,diagonal = False,n = None):
        """Returns a list of tuples as a path from the given start to the given end in the given array
        Base implementation is drawn from Nicholas Swift work explained at https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2

        TODO - This can probably be a lot accelerated by numba and or cython
        TODO - Requires for westworld env to have a get_nav_mesh() method extracting numpy array
        TODO - Will only work if grid environment, yet possible to discretize env if needed
        TODO - Add stop at n iterations to fasten computation
        """

        # Create start and end node
        start_node = Node(None, start)
        end_node = Node(None, end)

        # Get adjacent moves
        moves = self.get_adjacent_moves(diagonal)

        # Initialize both open and closed list
        open_list = []
        closed_list = []

        # Add the start node
        open_list.append(start_node)

        i = 0

        # Loop until you find the end
        while len(open_list) > 0:

            print(len(open_list))
            i += 1

            # Get the current node
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            # Pop current off open list, add to closed list
            open_list.pop(current_index)
            closed_list.append(current_node)

            # Found the goal
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                print(i)
                return path[::-1] # Return reversed path

            # Generate children
            children = []
            for new_position in moves: # Adjacent squares

                # Get node position
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                # Make sure within range
                if node_position[0] > (len(array) - 1) or node_position[0] < 0 or node_position[1] > (len(array[len(array)-1]) -1) or node_position[1] < 0:
                    continue

                # Make sure walkable terrain
                if array[node_position[0]][node_position[1]] != 0:
                    continue

                # Create new node
                new_node = Node(current_node, node_position)

                # Append
                children.append(new_node)

            # Loop through children
            for child in children:

                # Child is on the closed list
                for closed_child in closed_list:
                    if child == closed_child:
                        continue

                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h

                # Child is already in the open list
                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                # Add the child to the open list
                open_list.append(child)



