

import uuid


class BaseObject:
    def __init__(self):

        self.id = str(uuid.uuid1())
        self._clock = 0


    @property
    def clock(self):
        return self._clock

    def clocktick(self):
        self._clock += 1
