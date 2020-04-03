


class Pathfinding:


    def get_adjacent_moves(self,diagonal = False):

        moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        diagonal_moves = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        if not diagonal:
            return moves
        else:
            return moves + diagonal_moves

