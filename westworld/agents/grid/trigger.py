




from .rectangle import Rectangle



class Trigger(Rectangle):


    @property
    def blocking(self):
        return False


    @property
    def static(self):
        return False


    def step(self):

        is_collision,x = self.collides_with(self.env.objects)
        
        if is_collision:
            print(x)
            self.on_collision()



    def on_collision(self):
        print("Collision")