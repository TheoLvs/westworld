
from collections import defaultdict
from scipy.stats import norm
import numpy as np
import random

from .grid_agent import BaseGridAgent
from ..colors import *


class SIRAgent(BaseGridAgent):

    def __init__(self,x,y,state = "S",recovery_duration_range = [20,50],contact_risk = 3,show_search_radius = False,search_radius_method = "circle",search_radius = 2,*args,**kwargs):

        super().__init__(x,y,*args,**kwargs,search_radius = search_radius,img_asset = "blob")
        
        self.set_state(state)
        self.show_search_radius = show_search_radius
        self.search_radius_method = search_radius_method
        self.recovery_duration = np.random.randint(*recovery_duration_range)
        self.contact_risk = contact_risk
        self.infected_date = 0

        
    def set_state(self,state):
        
        self.state = state
        
        if state == "S":
            self.color = BLUE
        elif state == "I":
            self.color = RED
        else:
            self.color = GREEN
            
        self.init_internals(errors_binding = False)
        
        
    
    def step(self):
        
        if self.state == "S":
            
            n_infected = len(self.find_in_range({"state":"I"}))
            
            if n_infected > 0:
                proba_infection = norm.cdf(n_infected,loc = self.contact_risk,scale = 3)

                if random.random() < proba_infection:

                    self.set_state("I")
                    self.infected_date = self.clock
                
                
        elif self.state == "I":
            
            if self.clock - self.infected_date >= self.recovery_duration:
                self.set_state("R")
            
        self.wander()
        
        
        
        