from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam
from soccersimulator import VolleySimulation, volley_show_simu
from tools import * 
import math
from random import randint
GAME_WIDTH = 180
GAME_HEIGHT = 90


class Defense2(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Fonceur")

    def compute_strategy(self, state, id_team, id_player):
        fct = SuperState(state, id_team, id_player)
        if fct.peut_frapper() :
            j1 = fct.joueur_proche_rang(1)
            if(fct.player.distance(j1) <30):
                return fct.passe(j1)
            else:
                return fct.degagement()
        if fct.can_def :
            return fct.aller_vect
        return fct.aller(fct.position_defenseur)
    

    
    
    
    
class Attaque2(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Fonceur")

    def compute_strategy(self, state, id_team, id_player):
        fct = SuperState(state, id_team, id_player)
        if(fct.peut_frapper()):
            if(fct.player.distance(fct.ennemi_proche())< 10):
                if(fct.ennemi_proche().y > GAME_HEIGHT/2):
                    return fct.shoot( Vector2D((2-id_team)*GAME_WIDTH +8*(-1)**id_team ,random.randint(10,30) ) )
                else:
                    return fct.shoot( Vector2D((2-id_team)*GAME_WIDTH +8*(-1)**id_team ,random.randint(55,75) ) )
            else:
                return fct.shoot_but()
        else:
            if(fct.player.distance(fct.ball)<20):
                return fct.aller_vect
            else:
                return fct.posi_att()
        
        
team1 = SoccerTeam(name="Team 1")
team2 = SoccerTeam(name="Team 2")

# Add players
team2.add("bleui",Defense2()) 
team1.add("rouge2",Attaque2()) 
team2.add("kiwi",Attaque2()) 
team1.add("rouge1",Attaque2()) 





simu = VolleySimulation(team1, team2)

# Simulate and display the match
volley_show_simu(simu)