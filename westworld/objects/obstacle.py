


from .rectangle import BaseRectangle



class BaseObstacle(BaseRectangle):

    @property
    def blocking(self):
        return True

    @property
    def stationary(self):
        return True


    def __repr__(self):
        return f"Obstacle({self.x},{self.y},size=({self.width},{self.height}))"
