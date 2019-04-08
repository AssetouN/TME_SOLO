from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam
from soccersimulator import VolleySimulation, volley_show_simu
from tools import * 
import math
from random import randint
GAME_WIDTH = 180
GAME_HEIGHT = 90


class Switch(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Switch")
            
    def compute_strategy_def(self, state, id_team, id_player):
        fct = SuperState(state, id_team, id_player)
        if fct.peut_frapper() :
          return fct.degagement()
        if fct.can_def :
            return fct.aller_vect
        return fct.aller(fct.position_defenseur)
    
    
    def compute_strategy_attack(self, state, id_team, id_player):
        fct = SuperState(state, id_team, id_player)
        if(fct.peut_frapper()):
            if(fct.can_att):
                if(fct.player.distance(fct.ennemi_proche())< 10):
                    if(fct.ennemi_proche().y > GAME_HEIGHT/2):
                        return fct.shoot( Vector2D((2-id_team)*GAME_WIDTH +8*(-1)**id_team ,random.randint(10,30) ) )
                    else:
                        return fct.shoot( Vector2D((2-id_team)*GAME_WIDTH +8*(-1)**id_team ,random.randint(55,75) ) )
                else:
                    return fct.shoot_but()
            else:
                return fct.pousse_ball()
        else:
            return fct.aller_vect
        
    def compute_strategy(self, state, id_team, id_player):
       
        fct = SuperState(state, id_team, id_player)
    
        
        if (fct.ball_camp):
           return self.compute_strategy_def( state, id_team, id_player)
        else:
            return self.compute_strategy_attack( state, id_team, id_player)




            
class Test_Attaque(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Fonceur")

    def compute_strategy(self, state, id_team, id_player):
        fct = SuperState(state, id_team, id_player)
        if(fct.peut_frapper()):
            if(fct.can_att):
                if(fct.player.distance(fct.ennemi_proche())< 10):
                    if(fct.ennemi_proche().y > GAME_HEIGHT/2):
                        return fct.shoot( Vector2D((2-id_team)*GAME_WIDTH +8*(-1)**id_team ,random.randint(10,30) ) )
                    else:
                        return fct.shoot( Vector2D((2-id_team)*GAME_WIDTH +8*(-1)**id_team ,random.randint(55,75) ) )
                else:
                    return fct.shoot_but()
            else:
                return fct.pousse_ball()
        else:
            return fct.aller_vect
              
team1 = SoccerTeam(name="Team 1")
team2 = SoccerTeam(name="Team 2")

# Add players
team2.add("kiwiS",Switch()) 
team1.add("kiwi",Test_Attaque())




simu = VolleySimulation(team1, team2)

# Simulate and display the match
volley_show_simu(simu)