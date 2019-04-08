from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam
from soccersimulator import VolleySimulation, volley_show_simu
from tools import * 
import math
from random import randint
GAME_WIDTH = 180
GAME_HEIGHT = 90

class Attaque(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Fonceur")

    def compute_strategy(self, state, id_team, id_player):
        fct = SuperState(state, id_team, id_player)
        if(fct.peut_frapper()):
            if(fct.can_att):
                if(fct.ennemi_proche().y > GAME_HEIGHT/2):
                    return fct.shoot( 1.5*Vector2D((2-id_team)*GAME_WIDTH +8*(-1)**id_team ,random.randint(8,40) ) )
                else:
                    return fct.shoot( 1.5*Vector2D((2-id_team)*GAME_WIDTH +8*(-1)**id_team ,random.randint(45,80) ) )
            else:
                return fct.pousse_ball()
        else:
            return fct.aller_vect
        
        
team1 = SoccerTeam(name="Team 1")
team2 = SoccerTeam(name="Team 2")

# Add players
team2.add("kiwi",Attaque()) 
team1.add("Est",Attaque()) 




simu = VolleySimulation(team1, team2)

# Simulate and display the match
volley_show_simu(simu)