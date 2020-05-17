



from .trigger import BaseTrigger


class BaseCollectible(BaseTrigger):
    """Collectible objects in an environment
    Collectibles are objects an agent can find, after having been found the object disappears
    Eg: Pacman or Snake
    It's simply define by subclassing the trigger class, ie a non-stationary non-blocking object with a callback on collision
    """


    def step(self):
        """Step function triggered by the environment
           - We look if the an agent has encountered the collectible
           - The on_collision method is called that need to be subclassed
           - The object is removed from the environment
        """

        # Find collisions
        is_collision,objects = self.collides_with(self.env.objects)
        assert len(objects) <= 1
        
        # Trigger callback
        if is_collision:
            self.on_collision(objects)

            # Remove object from the environment
            self.env.remove_object(self)



    def on_collision(self,objects):
        print(f"Collision with objects {objects}, this function should be overridden")