import itertools
import time
import numpy
import inverse_kinematics
import direct_kinematics
import math
from contextlib import closing
import pypot.robot

import pygame				#Init de Pygame
from pygame.locals import *	#Import de Pygame locals en direct 

##********** VARIABLES **********##
T_Fenetre = 600						#Hauteur Fenetre
Fenetre_2 = T_Fenetre/2				#Fenetre/2 souvent utilise
T_Reticule = 50						#Taille Reticule
Reticule_2 = Reticule_2			#Reticule/2 souvent utilise

Limit_Dist=50						#Distance Limite
#Ce n'est pas une limite r�elle c'est utile pour avoir 
#un ratio coh�rent en fonction de la position du curseur
Coeff_Dist = Fenetre_2/Limit_Dist	#Ratio en question
Pos_Center = [100, 0, -100]			#Position par d�faut du robot
Is_Mouse = True						#Gestion de la souris
Is_Joystick = False					#ou du Joystick (par ergonomie l'un desactive l'autre)
Joy_X_Axis = 0						#Position du Joystick sur X
Joy_Y_Axis = 0						#Position du Joystick sur Y

##********** PYGAME **********##
#Init
pygame.init()
H_Fenetre = 600
L_Fenetre = 600
H_Reticule = 50
L_Reticule = 50

limit_distance=50
coeff_distance=(L_Fenetre/2)/limit_distance

initial_altitude = -90
alt_var = 20
center_pos = [100, 0, initial_altitude]

is_mouse = True
is_joystick = False


#Ouverture de la fenetre Pygame
fenetre = pygame.display.set_mode((T_Fenetre, T_Fenetre))
#Chargement, redimensionnement et collage de la grille
fond = pygame.image.load("../Ressources/Grille.jpg").convert()
fond = pygame.transform.scale(fond, (T_Fenetre, T_Fenetre))
fenetre.blit(fond, (0,0))
#Chargement, redimensionnement, positionnement et collage du Reticule
Reticule = pygame.image.load("../Ressources/Reticule.png").convert_alpha()
Reticule = pygame.transform.scale(Reticule, (T_Reticule, T_Reticule))
Ret_x = Fenetre_2-Reticule_2
Ret_y = Fenetre_2-Reticule_2
fenetre.blit(Reticule, (Ret_x, Ret_y))
#Rafraichissement de l'ecran
pygame.display.flip()

##********** MOUVEMENTS **********##
#Recupere les angles
def get_angles (pos):
	angles = inverse_kinematics.leg_ik(pos[0], pos[1], pos[2])
	return [ angles.posx, angles.posy, angles.posz ]
#Ordonne � la jambe d'atteindre une position
def leg_goto(leg, pos):
	angles = get_angles(pos)
	i = 0
	for m in leg :
		m.goal_position = angles[i]
		i += 1
		
##********** CLASSES **********##
#Positionnement "correct" d'une patte
class corrected_leg:
	leg = None
	delta_angle = 0
	leg_buffer = []
	
	def __init__(self, leg, delta_angle):
		self.leg = leg
		self.delta_angle = delta_angle
		self.leg_buffer = Pos_Center
		
	def get_corrected_angle(self, initial_angle):
		return initial_angle - self.delta_angle
		
	def goto(self, pos, ref = Pos_Center):
		Angle_Rad = math.radians(-self.delta_angle)
		dy = math.cos(Angle_Rad) * pos[0] +  math.sin(Angle_Rad) * pos[1]
		dx = (-1 * math.sin(Angle_Rad) * pos[0]) +  math.cos(Angle_Rad) * pos[1]
		
		Goal_Pos = [ref[0]+dx, ref[1]+dy, ref[2] + pos[2]]
		leg_goto(self.leg, Goal_Pos)

#Positionnement "correct" du Robot
class corrected_robot:
	legs = []
	rigth_legs = []
	left_legs = []
	state = -1
	start_time = 0
	actual_time = 0
	ast_period_time = 0
	
	def __init__(self, legs, rl, ll):
		self.legs = legs
		self.rigth_legs = rl
		self.left_legs = ll
		self.state = -1
		self.start_time = time.clock() * 1000
		self.actual_time = self.start_time
		self.last_period_time = self.start_time;
	
	def goto(self, pos):
		for l in self.legs:
			l.goto(pos)
	
	def moveto(self, pos, speed, amp):
		t = ((self.actual_time-self.last_period_time)/(speed))
		z = amp * math.sin(math.pi * t)
		old_pos = [pos[0], pos[1], pos[2]]
		pos[0] = pos[0] * t 
		pos[1] = pos[1] * t 
		alt_pos = [old_pos[0] - pos[0], old_pos[1] - pos[1], pos[2]]
		pos[2] = z
		R_pos = pos		# RIGTH LEGS
		L_pos = alt_pos	# LEFT LEGS

		if self.state == 1 :
			R_pos = alt_pos
			L_pos = pos

		for l in self.left_legs:
			l.goto(L_pos)
		for l in self.rigth_legs:
			l.goto(R_pos)

		self.actual_time = time.clock() * 1000
		if ((self.actual_time - speed) >= self.last_period_time):
			self.last_period_time = self.actual_time
			self.state = -1 *  self.state

##********** TESTS **********##
#Simplification Between
def between ( x,  val1, val2) : # return val1 <= x <= val2
	return (val1 <= x and x <= val2)
#Simplification outof
def outof ( x,  val1, val2) : # return val1 > x  or  x > val2
	return (not(between(x, val1, val2)))

	
def update_center_pos_z(z):
	center_pos[2] = z
#Simplification speed
def check_Speed_Axis (Speed_Axis, gaz) : 
	return (outof(Speed_Axis, -0.1, 0.1) and not(gaz)) or ( between(Speed_Axis, -0.1, 0.1) and gaz )

##********** MAIN **********##
if __name__ == '__main__':

	#Test du joystick present
	try:
		Is_Joystick = True
		Is_Mouse = False
		joystick = pygame.joystick.Joystick(0)
		joystick.init()
	except:
		Is_Joystick = False
		Is_Mouse = True
				
	#On va maintenant utiliser un fichier de configuration
	#Il nous permettra de limiter nos demandes aux angles valides
	with closing(pypot.robot.from_json('config.json')) as megabot:
		for m in megabot.motors : 
			m.compliant = False;
		#Positionnement "correct" des pattes
		leg1 = corrected_leg(megabot.leg1, 0)
		leg2 = corrected_leg(megabot.leg2, -90)
		leg3 = corrected_leg(megabot.leg3, -90)
		leg4 = corrected_leg(megabot.leg4, -180)
		leg5 = corrected_leg(megabot.leg5, 90)
		leg6 = corrected_leg(megabot.leg6, 90)
		#Positionnement "correct" du Robot
		robot = corrected_robot([leg1, leg2, leg3, leg4, leg5, leg6], [leg1, leg3, leg5], [leg2, leg4, leg6])
		#Position Initiale du Robot
		robot.goto([0, 0, 0])
	
		
		continuer = True
		gaz=False
		remind_button = 0
		button = 0
		joy_x_axis = 0
		joy_y_axis = 0
		speed_axis = 0
		alt_axis = 0
		
		while continuer:
			
			if is_joystick : 
				button = joystick.get_button(3)
				joy_x_axis = joystick.get_axis(0)
				joy_y_axis = joystick.get_axis(1)
				speed_axis = joystick.get_axis(2)
				alt_axis = joystick.get_axis(6)
			
			for event in pygame.event.get():	#Attente des evenements
				if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
					Continue = False
				#Tab pour switch entre Joystick et Souris
				if event.type == KEYDOWN and event.key == K_TAB:
							Is_Joystick = not(Is_Joystick)
							Is_Mouse = not(Is_Mouse)
				#Mouvement de la souris si elle est utilis�e
				if Is_Mouse and event.type == MOUSEMOTION :
					#On change les coordonnees du Reticule
					Ret_x = event.pos[0]-Reticule_2
					Ret_y = event.pos[1]-Reticule_2
				#Activation des Gaz Si clic souris, espace ou activation des Gaz
				if (event.type == MOUSEBUTTONDOWN) or (event.type == KEYDOWN and event.key == K_SPACE) or check_Speed_Axis(Speed_Axis, Gaz) :
					Gaz = not(Gaz)
					#On change la couleur du Reticule
					if Gaz :
						Reticule = pygame.image.load("../Ressources/Red_Reticule.png").convert_alpha()
						Reticule = pygame.transform.scale(Reticule, (T_Reticule, T_Reticule))
					else :
						Reticule = pygame.image.load("../Ressources/Reticule.png").convert_alpha()
						Reticule = pygame.transform.scale(Reticule, (T_Reticule, T_Reticule))	
			#Fin de l'attente des evenements

			#GESTION DES DEPLACEMENTS (OU PAS)
			#D�finition de la p�riode en fonction des Gaz
			period = 1700 - (math.fabs(Speed_Axis)*1500)
			#Position a atteindre
			Pos_Final = [(Ret_x - Fenetre_2)/Coeff_Dist, (Ret_y - Fenetre_2)/Coeff_Dist, 0]
			if Gaz : 
				robot.moveto(Pos_Final, period, 35)
			else : 
				robot.goto(Pos_Final)
			if is_joystick :
				Reticulte_x = L_Fenetre/2 + (L_Fenetre/2 * joy_x_axis) -L_Reticule/2		
				Reticulte_y = H_Fenetre/2 + (H_Fenetre/2 * joy_y_axis) -H_Reticule/2	
				
			
			period = 1700 - (math.fabs(speed_axis)*1500)
			new_altitude = initial_altitude - ( alt_axis * alt_var)
			update_center_pos_z(new_altitude)
			#PYGAME Re-collage
			fenetre.blit(fond, (0,0))	
			fenetre.blit(Reticule, (Ret_x, Ret_y))
			#PYGAME Rafraichissement
			pygame.display.flip()