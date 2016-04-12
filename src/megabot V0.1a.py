import itertools
import time
import numpy
import inverse_kinematics
import direct_kinematics
import math
from contextlib import closing
import pypot.robot

import pygame
from pygame.locals import *

center_pos = [100, 0, -100]

def get_position (angles):
	pos = direct_kinematics.leg_dk(angles[0], angles[1], angles[2])
	return [ pos.posx, pos.posy, pos.posz ]
	
def get_angles (pos):
	angles = inverse_kinematics.leg_ik(pos[0], pos[1], pos[2])
	return [ angles.posx, angles.posy, angles.posz ]
	
def megabot_goto (megabot, leg, pos, duration):
	angles = get_angles(pos)
	motors = [m.name for m in leg]
	cmd = dict(zip(motors, angles))
	megabot.goto_position(cmd, duration)

def leg_goto(leg, pos):
	angles = get_angles(pos)
	i = 0
	for m in leg :
		m.goal_position = angles[i]
		i += 1

class corrected_leg:
	leg = None
	delta_angle = 0
	
	def __init__(self, leg, delta_angle):
		self.leg = leg
		self.delta_angle = delta_angle
		
	def get_corrected_angle(self, initial_angle):
		return initial_angle - self.delta_angle
		
	def goto(self, pos):
		dy = math.cos(math.radians(-self.delta_angle)) * pos[0] +  math.sin(math.radians(-self.delta_angle)) * pos[1]
		dx = (-1 * math.sin(math.radians(-self.delta_angle)) * pos[0]) +  math.cos(math.radians(-self.delta_angle)) * pos[1]
		
		goal_pos = [center_pos[0]+dx, center_pos[1]+dy, center_pos[2]]
		leg_goto(self.leg, goal_pos)
		 
	
class corrected_robot:
	legs = []
	
	def __init__(self, legs):
		self.legs = legs
	
	def goto(self, pos):
		for l in self.legs:
			l.goto(pos)
	
def position_centre (megabot, deltax, deltay, time):
	z=-100
	x=100
	y=0
	
	megabot_goto(megabot, megabot.leg1, [x+deltax, y-deltay, z], time)

	megabot_goto(megabot, megabot.leg3, [x+deltay, y-deltax, z], time)
	megabot_goto(megabot, megabot.leg5, [x-deltay, y+deltax, z], time)


	megabot_goto(megabot, megabot.leg4, [x-deltax, y+deltay, z], time)

	megabot_goto(megabot, megabot.leg2, [x+deltay, y-deltax, z], time)
	megabot_goto(megabot, megabot.leg6, [x-deltay, y+deltax, z], time)
	
def position_avant (megabot):
	z=-100
	x=100
	y=0
	delta=50
	
	megabot_goto(megabot, megabot.leg1, [x, y, z], 0.1)

	megabot_goto(megabot, megabot.leg3, [x, y-delta, z], 0.1)
	megabot_goto(megabot, megabot.leg5, [x, y+delta, z], 0.1)


	megabot_goto(megabot, megabot.leg4, [x+delta, y, z], 0.1)

	megabot_goto(megabot, megabot.leg2, [x, y, z], 0.1)
	megabot_goto(megabot, megabot.leg6, [x, y, z], 0.1)

def position_arriere (megabot):
	z=-100
	x=100
	y=0
	delta=50
	
	megabot_goto(megabot, megabot.leg1, [x+delta, y, z], 0.1)

	megabot_goto(megabot, megabot.leg3, [x, y, z], 0.1)
	megabot_goto(megabot, megabot.leg5, [x, y, z], 0.1)


	megabot_goto(megabot, megabot.leg4, [x, y, z], 0.1)

	megabot_goto(megabot, megabot.leg2, [x, y+delta, z], 0.1)
	megabot_goto(megabot, megabot.leg6, [x, y-delta, z], 0.1)


def make_circle(megabit):
	z=-100
	x=100
	y=0
	delta=50
	

pygame.init()
H_Fenetre = 600
L_Fenetre = 600
H_Reticule = 50
L_Reticule = 50

#Ouverture de la fenetre Pygame
fenetre = pygame.display.set_mode((L_Fenetre, H_Fenetre))

#Chargement et collage du fond
fond = pygame.image.load("../Ressources/Grille.jpg").convert()
fond = pygame.transform.scale(fond, (L_Fenetre, H_Fenetre))
fenetre.blit(fond, (0,0))


#Chargement et collage du personnage
Reticule = pygame.image.load("../Ressources/Reticule.png").convert_alpha()
Reticule = pygame.transform.scale(Reticule, (L_Reticule, H_Reticule))
Reticulte_x = L_Fenetre/2-L_Reticule/2
Reticulte_y = H_Fenetre/2-H_Reticule/2
fenetre.blit(Reticule, (Reticulte_x, Reticulte_y))

#Rafraichissement de l'ecran
pygame.display.flip()
pygame.key.set_repeat(400, 30)
#BOUCLE INFINIE


if __name__ == '__main__':
	#On va maintenant utiliser un fichier de configuration
	#Il nous permettra de limiter nos demandes aux angles valides
	with closing(pypot.robot.from_json('config.json')) as megabot:
		for m in megabot.motors : 
			m.compliant = False;

		leg1 = corrected_leg(megabot.leg1, 0)
		leg2 = corrected_leg(megabot.leg2, -90)
		leg3 = corrected_leg(megabot.leg3, -90)
		leg4 = corrected_leg(megabot.leg4, -180)
		leg5 = corrected_leg(megabot.leg5, 90)
		leg6 = corrected_leg(megabot.leg6, 90)
			
		robot = corrected_robot([leg1, leg2, leg3, leg4, leg5, leg6])

		robot.goto([0, 0])
	
			
		continuer = 1
		gaz=False
		while continuer:
			for event in pygame.event.get():	#Attente des evenements
				if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
					continuer = 0
				if event.type == MOUSEMOTION: #Si mouvement de souris
					#On change les coordonnees du Reticule
					Reticulte_x = event.pos[0]-L_Reticule/2
					Reticulte_y = event.pos[1]-H_Reticule/2
				if event.type == MOUSEBUTTONDOWN or (event.type == KEYDOWN and event.key == K_SPACE) :
						gaz = not(gaz)
						if gaz == 1 :
							Reticule = pygame.image.load("../Ressources/Red_Reticule.png").convert_alpha()
							Reticule = pygame.transform.scale(Reticule, (L_Reticule, H_Reticule))				
						else:
							Reticule = pygame.image.load("../Ressources/Reticule.png").convert_alpha()
							Reticule = pygame.transform.scale(Reticule, (L_Reticule, H_Reticule))	
								
			#Re-collage
			fenetre.blit(fond, (0,0))	
			fenetre.blit(Reticule, (Reticulte_x, Reticulte_y))
			robot.goto([(Reticulte_x - L_Fenetre/2)/6, (Reticulte_y - H_Fenetre/2)/6])
			#Rafraichissement
			pygame.display.flip()
		


		
		
		
		
		