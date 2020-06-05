from .grid_agent import BaseGridAgent

class CollectibleFinderAgent(BaseGridAgent):


    def __init__(self,x,y,show_search_radius = True,search_radius_method = "circle",search_radius = 2,*args,**kwargs):

        super().__init__(x,y,*args,**kwargs,search_radius = search_radius)

        self.show_search_radius = show_search_radius
        self.search_radius_method = search_radius_method
        self.targets = {}
        self.current_target = None

    
    def step(self):
        
        targets = self.find_in_range(condition = {"collectible":True})
        self.targets.update({t.id:t for t in targets if t.id not in self.targets})
        self.targets = {k:v for k,v in self.targets.items() if k in self.env._objects}
        
        if len(self.targets) == 0:
            self.wander()
            
        else:
            if self.current_target is None:
                self.current_target = list(self.targets.values())[0]
                
            reached_target = self.move_towards(obj = self.current_target,n = 100)
            if reached_target:
                self.current_target = None