


from .rectangle import BaseRectangle



class BaseObstacle(BaseRectangle):

    @property
    def blocking(self):
        return True

    @property
    def stationary(self):
        return True
