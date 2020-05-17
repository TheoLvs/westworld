

import uuid


class BaseObject:
    """Default Object serving as base for each agent evolving in environments
    """
    def __init__(self):

        # Create id and clock
        self.id = str(uuid.uuid1())
        self._clock = 0

        # Init function to be overridden
        self.init()


    @property
    def clock(self):
        """Default internal clock for each object
        """
        return self._clock

    def clocktick(self):
        """Helper function to increment internal clock
        """
        self._clock += 1


    @property
    def env(self):
        """Environment linked to the object
        """
        if hasattr(self,"_env"):
            return self._env
        else:
            raise Exception("The object must be attached to an environment")


    def set_env(self,env):
        """Default setter function
        """
        self._env = env


    def init(self):
        """Default init function 
        Can be overriden in special objects
        """
        pass



    
