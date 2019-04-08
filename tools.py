GAME_WIDTH = 150
GAME_QUARTER = GAME_WIDTH/4
GAME_HALF = GAME_WIDTH/2
GAME_THREE_QUARTER = GAME_WIDTH*3/4
GAME_HEIGHT = 90
GAME_GOAL_HEIGHT = 10
PLAYER_RADIUS = 1.
BALL_RADIUS = 0.65
MAX_GAME_STEPS = 2000
maxPlayerSpeed = 1.
maxPlayerAcceleration = 0.2
maxBallAcceleration = 5 

from soccersimulator import *
from math import *


class SuperState ( object ):
    def __init__ ( self , state , id_team , id_player ):
        self . state = state
        self . id_team = id_team
        self . id_player = id_player
	
    @property
    def ball(self):
        return self.state.ball.position
    @property
    def ball_vitesse(self):
        return self.state.ball.vitesse
		
    @property
    def player(self):
        return self.state.player_state(self.id_team, self.id_player).position
		
    @property
    def goalAdv ( self ):
        return Vector2D((2 - self.id_team )*settings.GAME_WIDTH , settings.GAME_HEIGHT / 2)
		
    @property
    def goal(self):
        return Vector2D((self.id_team - 1)*settings.GAME_WIDTH , settings.GAME_HEIGHT / 2)
    
    def id_team_adv(self):
        if(self.id_team ==1):
            return 2
        return 1
	
  #====================================================================================================================================
#            Tir avec anticipation balle
    
    @property
    def aller_vect(self):
        return SoccerAction(self.vect_anticipe-self.player,Vector2D())
    @property	
    def vect_anticipe(self):
        if(self.player.distance(self.ball) < 6):
            return self.ball + 1.01*self.state.ball.vitesse
        return (self.ball+ 5.75*self.state.ball.vitesse)
   
    @property              
    def vect_anticipe_att(self):    
        return self.state.ball + 4.5*self.state.ball.vitesse 
     
    def ball_position_future(self):
        if self.ball_vitesse.norm > 2 or self.ball_vitesse.norm < -2:
            return self.ball+self.ball_vitesse*10
        else :
            return self.ball
  #====================================================================================================================================
#     Simple tir
  
    def mini_shoot(self,p):
        return SoccerAction(Vector2D(),(p-self.player)*0.03)
      
              
    def get_dir_jeu(self):
        return  (self.goalAdv-self.goal).normalize()
    
    def shoot(self,p):
        return SoccerAction(Vector2D(),(p-self.player))
    
    def peut_frapper(self):
        return (self.ball-self.player).norm <= settings.PLAYER_RADIUS + settings.BALL_RADIUS 

    @property    
    def ball_camp(self):
        if (pow(-1 ,self.id_team) * self.ball.x) >= (pow(-1 ,self.id_team) *settings.GAME_WIDTH/2):
            return True
        else:
            return False      
           
    def Immobile(self):
        return SoccerAction(Vector2D(0,0), Vector2D(0,0))  

#====================================================================================================================================
#           Proximité joueur de notre équipe ou équipe adverse
    def est_proche_adv(self,p):
        opponents = [self.state.player_state(id_team, id_player).position for (id_team, id_player) in self.state.players if ( id_team != self.id_team)]
        for i in range(0, len(opponents)):
            if(p.distance(opponents[i]) < 3):
                return True
        return False
    
 
    def ennemi_proche(self):
        opponents = [self.state.player_state(id_team, id_player) for (id_team, id_player) in self.state.players if (id_team != self.id_team)]
        return min([(self.player.distance(player_p.position), player_p.position) for player_p in opponents])[1]
    
    def joueur_proche_rang(self, rang):
        """ Classe tous les joueurs de l'équipe du player du  plus proche au plus loin et renvoie le joueur corresponsant au rang"""
        LP= [self.state.player_state(it,ip).position for (it,ip) in self.state.players if it == self.id_team and ip != self.id_player]
        L_distance = [(self.player.distance(player_p), player_p) for player_p in LP]#on recupère la position de chaque joeurs 
        L_distance.sort()
        return L_distance[rang-1][1]
#====================================================================================================================================
#            Deplacement
        
    
    def aller(self,p):
        return SoccerAction((p-self.player),Vector2D())
    
    def aller_vers_balle(self):
        return self.aller(self.ball+self.ball_vitesse)
    
    def mini_shoot(self):
        SoccerAction(Vector2D(),(self.goalAdv- self.ball_position_future())) 
        
    
    def shoot(self,p):
        return SoccerAction(Vector2D(),0.1*(p-self.player))
    
    def shoot_but(self):
        return self.shoot(self.goalAdv) 
        
    def pousse_ball(self):
        return SoccerAction(Vector2D(),(self.goalAdv- self.ball_position_future())*0.015) # 0.02 constante pour le dribble

    def pousse_ball_centre(self):
        if self.domicile():
            return SoccerAction(Vector2D(),(Vector2D(0,10)))
        else :
            return SoccerAction(Vector2D(),(Vector2D(-1,-2)))
        
    def position_coop_2v2(self):
        nb_coop=len([idp for (idt, idp) in self.state.players if idt == self.idteam])
        return self.state.player_state(self.key[0],(1+self.key[1])%(nb_coop)).position
    
    def degagement(self):
        return self.shoot_but()
    
    def passe(self,p):
        return SoccerAction(Vector2D(),(p-self.player).norm_max(3))
    
    def frappe_position(self):
        return abs((self.ball-Vector2D(GAME_WIDTH/2,GAME_HEIGHT/2)).x)<=45
    
    @property
    def position_defenseur(self):
        if self.id_team == 2 :
            return Vector2D(GAME_WIDTH*(15.0/16),GAME_HEIGHT/2)
        return Vector2D(GAME_WIDTH/16.0,GAME_HEIGHT/2)
    @property
    def can_def(self):
        if self.id_team == 1 :
            if self.ball.x<(GAME_WIDTH/2) :
                return True
            return False
        if self.ball.x>(GAME_WIDTH/2):
            return True
        return False
    @property
    def can_att(self):
        if self.id_team == 1:
            if(self.ball.x < GAME_WIDTH/2 and self.ball.x > GAME_WIDTH/3):
                return True
            return False
        if (self.ball.x > GAME_WIDTH/2 and self.ball.x < GAME_WIDTH*3/4):      
            return True
        return False
    
    def can_def2(self):
        if self.id_team == 1 :
            if self.ball.x < GAME_HALF-10 and self.ball.x> GAME_WIDTH*(2/10):
                return True
            return False
        if self.ball.x > (GAME_HALF+10) and self.ball.x < GAME_WIDTH*(8/10):
            return True
        return False
     
    def attaquant4_position_dribble(self):
        return abs((self.ball-self.goal).x)>70
#====================================================================================================================================
#            Replacement 
    def replacement_attaquant4(self):
        return self.aller(Vector2D(self.get_dir_jeu().x*80+self.goal.x,self.ball.y))
		
    def replacement_defense2(self):
        if(self.id_team == 1):
            return self.aller(Vector2D(GAME_HEIGHT/2, GAME_QUARTER))
        return self.aller(Vector2D(GAME_HEIGHT/2,GAME_THREE_QUARTER))
    
    def posi_att(self):
        if(self.id_team == 1):
            return self.aller(Vector2D(GAME_WIDTH/2-5,GAME_HEIGHT/2))
        else:
            return self.aller(Vector2D(GAME_WIDTH/2+5,GAME_HEIGHT/2))
#====================================================================================================================================
#                 Action Joueur    
    

    def action_attaquant4(self):
        if self.attaquant4_position_dribble():
            if not self.peut_frapper():
                return self.aller_vers_balle()
            elif not (self.frappe_position()):
                return self.pousse_ball()
            else :
                return self.shoot_but()
        else :
            return self.replacement_attaquant4()
        
        
    def defense(self):
        if self.peut_frapper() :
            return self.degagement()
        if self.can_def :
            return self.aller_vect
        if self.ball.x>(GAME_WIDTH*(3.0/4))-5 :
            return self.aller_vect
        return self.aller(self.position_defenseur)
    
    def defense2(self):
        if self.ball_camp:
            if self.peut_frapper():
                j1 = self.joueur_proche_rang(3)
                j2 = self.joueur_proche_rang(2)
                if self.est_proche_adv(j1):
                    return self.degagement()
                elif self.est_proche_adv(j2):
                    return self.degagement()
                else:
                    if(self.player.distance(j2) > self.player.distance(j1)):
                        return self.passe(j2)
                    else:
                        return self.passe(j1)
            else:
                 if self.can_def2():
                     return self.aller_vect
                 else:
                     return SoccerAction(acceleration = Vector2D(0, self.ball.y-self.player.y), shoot = Vector2D(0,0))            
        else:
            if(self.id_team == 1):
                return self.aller(Vector2D(GAME_QUARTER,GAME_HEIGHT/2))
            else:
                return self.aller(Vector2D(GAME_THREE_QUARTER,GAME_HEIGHT/2))
        
