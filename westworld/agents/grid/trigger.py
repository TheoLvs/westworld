




from .rectangle import BaseRectangle



class BaseTrigger(BaseRectangle):


    @property
    def blocking(self):
        return False


    @property
    def stationary(self):
        return False


    def step(self):

        # Find collisions
        is_collision,objects = self.collides_with(self.env.objects)
        
        # Trigger callback
        if is_collision:
            self.on_collision(objects)




    def on_collision(self,objects):
        print(f"Collision with objects {objects}")