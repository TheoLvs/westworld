

from .grid import GridEnvironment


class SpatialEnvironment(GridEnvironment):
    def __init__(self,width = None,height = None,
        objects = None,background_color = (0,0,0),
        callbacks_step = None,
        ):

        super().__init__(width = width,height = height,cell_size = 1,show_grid = False,objects = objects,
        background_color = background_color,callbacks_step = callbacks_step)



