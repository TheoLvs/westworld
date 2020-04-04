


class PathfindingError(Exception):
    pass



class Pathfinding:


    @staticmethod
    def get_adjacent_moves(diagonal = False):

        moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        diagonal_moves = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        if not diagonal:
            return moves
        else:
            return moves + diagonal_moves


    @staticmethod
    def show_path(mesh,start,end,path,sep = " "):

        path_str = []

        for i,row in enumerate(mesh):
            row_str = []
            for j,cell in enumerate(row):
                if (i,j) == start:
                    row_str.append("O")
                elif (i,j) == end:
                    row_str.append("X")
                elif cell == 1:
                    row_str.append("#")
                elif (i,j) in path:
                    row_str.append(".")
                else:
                    row_str.append(" ")

            row_str = ["|"] + row_str + ["|"]
            row_str = sep.join(row_str)
            path_str.append(row_str)

        print("\n".join(path_str))

