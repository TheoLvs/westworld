




from .rectangle import Rectangle



class Trigger(Rectangle):


    @property
    def blocking(self):
        return False