


from .rectangle import Rectangle



class Obstacle(Rectangle):

    @property
    def blocking(self):
        return True