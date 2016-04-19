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
T_Fenetre = 600							#Hauteur Fenetre
Fenetre_2 = T_Fenetre/2					#Fenetre/2 souvent utilise
T_Reticule = 50							#Taille Reticule
Reticule_2 = T_Reticule/2				#Reticule/2 souvent utilise
Initial_Altitude = -90					#Altitude de depart
Alt_Var = 20							#Variation d'altitude
Alt_Axis = 0							#Variable opur le Joystick
Limit_Dist=50							#Distance Limite
#Ce n'est pas une limite reelle c'est utile pour avoir 
#un ratio coherent en fonction de la position du curseur

Coeff_Dist = Fenetre_2/Limit_Dist		#Ratio en question
Pos_Center = [100, 0, Initial_Altitude]	#Position par defaut du robot
Is_Mouse = True							#Gestion de la souris
Is_Joystick = False						#ou du Joystick (par ergonomie l'un desactive l'autre)
Joy_X_Axis = 0							#Position du Joystick sur X
Joy_Y_Axis = 0							#Position du Joystick sur Y

##********** PYGAME **********##
#Init
pygame.init()
#Ouverture de la fenetre Pygame
fenetre = pygame.display.set_mode((T_Fenetre, T_Fenetre))
#Chargement, redimensionnement et collage de la grille
fond = pygame.image.load("../Ressources/Grille.jpg").convert()
fond = pygame.transform.scale(fond, (T_Fenetre, T_Fenetre))
fenetre.blit(fond, (0,0))
#Chargement, redimensionnement, positionnement et collage des Reticules
Reticule = pygame.image.load("../Ressources/Reticule.png").convert_alpha()
Reticule = pygame.transform.scale(Reticule, (T_Reticule, T_Reticule))
Red_Reticule = pygame.image.load("../Ressources/Red_Reticule.png").convert_alpha()
Red_Reticule = pygame.transform.scale(Red_Reticule, (T_Reticule, T_Reticule))
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
#Ordonne a la jambe d'atteindre une position
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
		
	def goto(self, pos, absolute = False, ref = Pos_Center):
		Angle_Rad = math.radians(-self.delta_angle)
		if not(absolute) :
			dy = math.cos(Angle_Rad) * pos[0] +  math.sin(Angle_Rad) * pos[1]
			dx = (-1 * math.sin(Angle_Rad) * pos[0]) +  math.cos(Angle_Rad) * pos[1]
		else:
			dx = pos[0]
			dy = pos[1]
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
	
	def moveto(self, pos, speed, amp, absolute = False):
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
			l.goto(L_pos, absolute)
		for l in self.rigth_legs:
			l.goto(R_pos, absolute)

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
#Simplification speed
def check_Speed_Axis (Speed_Axis, gaz) : 
	return (outof(Speed_Axis, 0, 0.1) and not(gaz)) or (between(Speed_Axis, 0, 0.1) and gaz)
#Update de l'altitude
def update_center_pos_z(z):
	Pos_Center[2] = z

##********** MAIN **********##
if __name__ == '__main__':
	#Test du joystick present
	try:
		joystick = pygame.joystick.Joystick(0)
		joystick.init()
		Is_Joystick = True
		Is_Mouse = False
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
		leg2 = corrected_leg(megabot.leg2, -65)
		leg3 = corrected_leg(megabot.leg3, -115)
		leg4 = corrected_leg(megabot.leg4, -180)
		leg5 = corrected_leg(megabot.leg5, 115)
		leg6 = corrected_leg(megabot.leg6, 65)
		#Positionnement "correct" du Robot
		robot = corrected_robot([leg1, leg2, leg3, leg4, leg5, leg6], [leg1, leg3, leg5], [leg2, leg4, leg6])
		#Initialisation
		robot.goto([0, 0, 0])	#Position
		Continue = True			#Boucle infini
		Gaz=False				#Deplacement
		circle = False			#Rotation
		Joy_X_Axis = 0			#Axe X du Joystick
		Joy_Y_Axis = 0			#Axe Y du Joystick
		Speed_Axis = 0.0		#Axe des Gaz du Joystick
		Alt_Axis = 0			#Axe de l'altitude
		Robot_X = 0
		Robot_Y = 0
		
		while Continue:
			if Is_Joystick : 
				Joy_X_Axis = joystick.get_axis(0)
				Joy_Y_Axis = joystick.get_axis(1)
				Abs_Speed_Axis = joystick.get_axis(2)
				Speed_Axis = math.fabs((Abs_Speed_Axis - 1 ) / 2 )
				Alt_Axis = joystick.get_axis(6)
				Left_Right_Axis = joystick.get_axis(5)
				Ret_x = Fenetre_2 + (Fenetre_2 * Joy_X_Axis) - Reticule_2	
				Ret_y = Fenetre_2 + (Fenetre_2 * Joy_Y_Axis) - Reticule_2
					

			for event in pygame.event.get():	#Attente des evenements
				if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
					Continue = False
				#Tab pour switch entre Joystick et Souris
				if event.type == KEYDOWN and event.key == K_TAB:
							Is_Joystick = not(Is_Joystick)
							Is_Mouse = not(Is_Mouse)
				#Mouvement de la souris si elle est utilisee
				if Is_Mouse : 
					Speed_Axis=0.9
					if event.type == MOUSEMOTION :
						#On change les coordonnees du Reticule
						Ret_x = event.pos[0]-Reticule_2
						Ret_y = event.pos[1]-Reticule_2
					#Activation des Gaz Si clic souris, espace ou activation des Gaz
					if (event.type == MOUSEBUTTONDOWN) or (event.type == KEYDOWN and event.key == K_SPACE) :
						Gaz = not(Gaz)
					if (not(Move) and Gaz):
						if (pygame.key.get_pressed()[K_LEFT]):
							Left_Right_Axis = -1.0
						elif (pygame.key.get_pressed()[K_RIGHT]):
							Left_Right_Axis = 1.0
						else :
							Left_Right_Axis = 0.0			
				#Activation des Gaz Si clic souris, espace ou activation des Gaz
				elif (check_Speed_Axis(Speed_Axis, Gaz)) :
					Gaz = not(Gaz)
			#Fin de l'attente des evenements


			#GESTION DES DEPLACEMENTS (OU PAS)
			#Definition de la periode en fonction des Gaz
			period = (1500*(1-Speed_Axis)) + 100
			#Position a atteindre
			Robot_X = (Ret_x - Fenetre_2)/Coeff_Dist
			Robot_Y = (Ret_y - Fenetre_2)/Coeff_Dist
			Pos_Final = [ Robot_X, Robot_Y, 0]
			new_altitude = Initial_Altitude - ( Alt_Axis * Alt_Var)
			update_center_pos_z(new_altitude)
			new_rotation_pos = [0, -50 * Left_Right_Axis, 0]
			
			if (Gaz and (outof(Robot_X, -5, 5) or outof(Robot_Y, -5, 5))) : 
				Move = True
			else : 
				Move = False
			if (not(Move) and Gaz and outof(Left_Right_Axis, -0.1, 0.1)):
				circle = True
			else :
				circle = False
			
			if Move : 
				robot.moveto(Pos_Final, period, 35, False)
			elif circle :
				robot.moveto(new_rotation_pos, period, 35, True)
			else : 
				robot.goto(Pos_Final)

			#PYGAME Re-collage
			fenetre.blit(fond, (0,0))	
			if Gaz :
				fenetre.blit(Red_Reticule, (Ret_x, Ret_y))
			else:
				fenetre.blit(Reticule, (Ret_x, Ret_y))
			#PYGAME Rafraichissement
			pygame.display.flip()