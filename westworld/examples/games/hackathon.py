from ...environment import GridEnvironment
from ...agents import BaseAgent
from ...objects import BaseObstacle,BaseTrigger,BaseCollectible
from ...simulation import Simulation
from ...colors import *


import pygame
import numpy as np

class BasePlayer(BaseAgent):
    def __init__(self,x,y,player1 = True,reproductor = False):
        
        self.player1 = player1
        self.color = RED if player1 else BLUE
        self.gold = 0
        self.reproductor = reproductor
        
        super().__init__(x,y,color = self.color)
        
    def __repr__(self):
        return f"{'Red' if self.player1 else 'Blue'}Player({self.x},{self.y},gold={self.gold})"
        
    def postrender(self):
        self.render_text(self.gold,size = 12,color=(255,255,255))
        
    @property
    def blocking(self):
        return False
    
    def find_group(self,**kwargs):
        # Add in class
        objs = self.find(**kwargs)
        objs = [x for x in objs if x.id != self.id]
        group = pygame.sprite.Group(objs)
        return group
    
    def collides_with(self,**kwargs):
        # Add in class
        group = self.find_group(**kwargs)
        collisions = self.collides_group(group)
        return collisions
    
    def action(self):
        pass
                
    def _attack(self,others):
        
        all_players = others + [self]
        
        # print(all_players)
        
        same_team = []
        other_team = []
        
        for player in all_players:
            if player.player1 == self.player1:
                same_team.append(player)
            else:
                other_team.append(player)
                
        same_team_strength = np.sum([x.gold for x in same_team])
        other_team_strength = np.sum([x.gold for x in other_team])
        
        proba_win_same = self._compute_proba_win(same_team_strength,other_team_strength)
        
        if np.random.rand() < proba_win_same: 
            
            for player in other_team:
                player.kill()
                
        else:
            
            for player in same_team:
                player.kill()
        
        
        
    def _compute_proba_win(self,a,b):
        return (a+1) / (a+b+2)
        
        
        
        
    def step(self):
        
        self.action()
        
        collisions = self.collides_with(name="Player")
        if len(collisions) > 0:
            self._attack(collisions)
            
        self.log({
            "gold":self.gold,
            "player":self.player1
        })


class Obstacle(BaseObstacle):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs,color = (230, 230, 250))



        
class Gold(BaseCollectible):
    def __init__(self,x,y):
        super().__init__(x,y,color = (220,150,50),img_asset = "ball")
        
    def on_trigger(self,obj):
        obj.gold += 1    


class ReproductionTrigger(BaseTrigger):
    
    def __init__(self,x,y,disable_time = 20):
        super().__init__(x,y,color = (255, 0, 255))
        
        self._active = 0
        self._disable_time = disable_time
        
        
    @property
    def active(self):
        return self._active == 0
    
    @property
    def stationary(self):
        return False
    
    def on_trigger(self,obj):
        
        if self.active:
            
            self._active = self._disable_time
            
            max_children = 1
            n_children = np.random.randint(1,max_children + 1)
            for i in range(n_children):
                if obj.player1:
                    new_child = self.env.player1_spawner(obj.x,obj.y)
                else:
                    new_child = self.env.player2_spawner(obj.x,obj.y)
                self.env.add_object(new_child)
            
            
    def step(self):
        
        if self.active:
            self.color = (255, 0, 255)
        else:
            self.color = (120,120,120)
            self._active -= 1





# Setup spawners
gold_spawner = lambda x,y : Gold(x,y)


class GameEnvironment(GridEnvironment):

    def __init__(self,width,height,
        player1_spawner,player2_spawner,n_players = 5,
        obstacles = None,triggers = None,
        gold_start = 200,gold_step_frequency = 1,gold_step_quantity = 1,
        cell_size = 15,
    ):

        super().__init__(width,height,cell_size,show_grid = True,background_color=(22, 41, 60),grid_color=(34, 46, 75),toroidal=True)

        # Store spawners
        self.player1_spawner = player1_spawner
        self.player2_spawner = player2_spawner

        # Store gold attributes
        self.gold_start = gold_start
        self.gold_step_frequency = gold_step_frequency
        self.gold_step_quantity = gold_step_quantity



    # def reset(self):

        # Add obstacles and triggers
        self.add_object(triggers)
        self.add_object(obstacles)

        # Add players and collectibles
        self.spawn(player1_spawner,n_players)
        self.spawn(player2_spawner,n_players)
        self.spawn(gold_spawner,self.gold_start)

    
    def post_step(self):
        
        gold_left = self.find(name = "Gold")
        self.log({"gold_left":len(gold_left)})
        
        if self.clock > 0 and self.clock % self.gold_step_frequency == 0:
            self.spawn(gold_spawner,self.gold_step_quantity)