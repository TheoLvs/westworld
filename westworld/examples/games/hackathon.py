from ...environment import GridEnvironment
from ...agents import BaseAgent
from ...objects import BaseObstacle,BaseTrigger,BaseCollectible
from ...simulation import Simulation
from ...colors import *


import pygame
import numpy as np
import matplotlib.pyplot as plt

class BasePlayer(BaseAgent):
    def __init__(self,x,y,player1 = True,reproductor = False):
        
        self.player1 = player1
        self.color = RED if player1 else BLUE
        self.gold = 0
        self.reproductor = reproductor
        
        super().__init__(x,y,color = self.color)
        
    def __repr__(self):
        return f"{'Red' if self.player1 else 'Blue'}Player({self.x},{self.y},gold={self.gold})"
        
    def post_render(self):
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

        # Safe check to avoid having players from the same team who fight
        if len(same_team) == 0 or len(other_team) == 0:
            return None
                
        same_team_strength = np.sum([x.gold for x in same_team])
        other_team_strength = np.sum([x.gold for x in other_team])
        
        proba_win_same = self._compute_proba_win(same_team_strength,other_team_strength)
        
        if np.random.rand() < proba_win_same: 
            
            for player in other_team:
                player.kill()

            same_team[0].gold += other_team_strength
                
        else:
            
            for player in same_team:
                player.kill()
        
            other_team[0].gold += same_team_strength
        
        
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



def make_obstacle(x,y,width,height):
    return Obstacle(x,y,width,height)

def make_reproduction_trigger(x,y):
    return ReproductionTrigger(x,y)

        
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



class MapsGenerator:
    def __init__(self,width,height):

        self.width = width
        self.height = height

    def make_map0(self):
        return {}

    def make_map1(self):

        triggers = [
            make_reproduction_trigger(1,1),
            make_reproduction_trigger(self.width-2,1),
            make_reproduction_trigger(1,self.height-2),
            make_reproduction_trigger(self.width-2,self.height-2),
        ]

        obstacles = [
            make_obstacle(0,0,self.width,1), # Top contour
            make_obstacle(0,0,1,self.height), # Left contour
            make_obstacle(self.width-1,0,1,self.height), # Right contour 
            make_obstacle(0,self.height-1,self.width,1), # Bottom contour
        ] 

        return {
            "triggers":triggers,
            "obstacles":obstacles,
        }


class GameEnvironment(GridEnvironment):

    def __init__(self,width,height,
        player1_spawner,player2_spawner,n_players = 5,
        level = {},
        gold_start = 200,gold_step_frequency = 1,gold_step_quantity = 1,
        cell_size = 15,
    ):

        # Store spawners
        self.player1_spawner = player1_spawner
        self.player2_spawner = player2_spawner
        self.gold_spawner = lambda x,y : Gold(x,y)
        self.n_players = n_players

        # Store obstacles and triggers
        self.obstacles = level.get("obstacles")
        self.triggers = level.get("triggers")

        # Store gold attributes
        self.gold_start = gold_start
        self.gold_step_frequency = gold_step_frequency
        self.gold_step_quantity = gold_step_quantity

        # Setup score zone
        margin = (0,50)

        # Init base environment class after initialization to use class attributes
        super().__init__(width,height,cell_size,show_grid = True,background_color=(22, 41, 60),grid_color=(34, 46, 75),toroidal=True,margin = margin)


    def post_render(self):
        self.render_score()


    def render_score(self):

        score = self.get_score()
        blue_score = score["Blue"]
        red_score = score["Red"]

        self.render_text("Age of Emp-AI-re",position = (10,self.height*self.cell_size + 15),color = WHITE,size = 20,font = "Calibri")
        self.render_text(f"Player 1 (Red): {red_score}",position = (200,self.height*self.cell_size + 15),color = RED,size = 20,font = "Calibri")
        self.render_text(f"Player 2 (Blue): {blue_score}",position = (400,self.height*self.cell_size + 15),color = (100,100,255),size = 20,font = "Calibri")
        self.render_text(f"©Ekimetrics",position = (600,self.height*self.cell_size + 10),color = WHITE,size = 14,font = "Calibri")
        self.render_text(f"Powered by Westworld",position = (600,self.height*self.cell_size + 25),color = WHITE,size = 14,font = "Calibri")


    def get_score(self):

        blue_score = np.sum([x.gold for x in self.find(player1 = False)])
        red_score = np.sum([x.gold for x in self.find(player1 = True)])

        return {"Blue":blue_score,"Red":red_score}


    def setup(self):

        # Add obstacles and triggers
        self.add_object(self.triggers)
        self.add_object(self.obstacles)

        # Add players and collectibles
        self.spawn(self.player1_spawner,self.n_players)
        self.spawn(self.player2_spawner,self.n_players)
        self.spawn(self.gold_spawner,self.gold_start)

    
    def post_step(self):
        
        gold_left = self.find(name = "Gold")
        self.log({"gold_left":len(gold_left)})
        
        if self.clock > 0 and self.clock % self.gold_step_frequency == 0:
            self.spawn(self.gold_spawner,self.gold_step_quantity)



class NaivePlayer(BasePlayer):
    
    def action(self):

        # Find closest food
        targets = self.find_closest(name = "Gold",k = 1)

        # If there is still food, move towards the food
        if len(targets) > 0:

            target = targets[0]

            # Use naive pathfinding for faster computation as there is no obstacle
            self.move_towards(obj = target,naive = True)

        # Otherwise just wandering
        # Changing direction every n steps where n = curiosity
        else:
            self.wander()



class RandomPlayer(BasePlayer):
    def action(self):
        self.random_walk()


def show_results(episode_data):

    result = episode_data.groupby(["step","player"])["gold"].sum().unstack("player").rename(columns = {False:"Player 2 (Blue)",True:"Player 1 (Red)"})
    result["Player 1 (Red)"].plot(figsize = (15,4),c = "red")
    result["Player 2 (Blue)"].plot(c = "blue")
    plt.legend()
    plt.show()