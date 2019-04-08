from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam
from soccersimulator import VolleySimulation, volley_show_simu
from tools import * 
import math


class Echauffement(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Fonceur")

    def compute_strategy(self, state, id_team, id_player):
        fct = SuperState(state, id_team, id_player)
        if(fct.peut_frapper()):
            return fct.shoot(fct.ennemi_proche())
        else:
            return fct.aller_vect
        
        
team1 = SoccerTeam(name="Team 1")
team2 = SoccerTeam(name="Team 2")

# Add players
team2.add("kiwi",Echauffement()) 
team1.add("Est",Echauffement()) 




simu = VolleySimulation(team1, team2)

# Simulate and display the match
volley_show_simu(simu)