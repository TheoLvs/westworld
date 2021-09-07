




from .rectangle import BaseRectangle



class BaseTrigger(BaseRectangle):


    @property
    def blocking(self):
        return False


    @property
    def stationary(self):
        return True

    @property
    def trigger(self):
        return True

    @property
    def collectible(self):
        return True



    def on_trigger(self,obj):
        pass

    def on_trigger_exit(self,obj):
        pass


    def on_collision(self,obj):

        self.on_trigger(obj)
        self.on_trigger_exit(obj)

