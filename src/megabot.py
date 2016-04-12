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


pygame.init()
H_Fenetre = 600
L_Fenetre = 600
H_Reticule = 50
L_Reticule = 50

limit_distance=50
coeff_distance=(L_Fenetre/2)/limit_distance

center_pos = [100, 0, -100]
is_mouse = True
is_joystick = False
joy_x_axis = 0
joy_y_axis = 0



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
#pygame.key.set_repeat(400, 30)


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
	leg_buffer = []
	
	def __init__(self, leg, delta_angle):
		self.leg = leg
		self.delta_angle = delta_angle
		self.leg_buffer = center_pos
		
	def get_corrected_angle(self, initial_angle):
		return initial_angle - self.delta_angle
		
	def goto(self, pos, ref = center_pos):
		dy = math.cos(math.radians(-self.delta_angle)) * pos[0] +  math.sin(math.radians(-self.delta_angle)) * pos[1]
		dx = (-1 * math.sin(math.radians(-self.delta_angle)) * pos[0]) +  math.cos(math.radians(-self.delta_angle)) * pos[1]
		
		goal_pos = [ref[0]+dx, ref[1]+dy, ref[2] + pos[2]]
		leg_goto(self.leg, goal_pos)
		 
	
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
		if self.state == -1 : # RIGTH LEGS
			for l in self.rigth_legs:
				l.goto(pos,)
			for l in self.left_legs : 
				l.goto(alt_pos)
		else : # LEFT LEGS
			for l in self.left_legs:
				l.goto(pos,)
			for l in self.rigth_legs:
				l.goto(alt_pos)
		self.actual_time = time.clock() * 1000
		if ((self.actual_time - speed) >= self.last_period_time):
			self.last_period_time = self.actual_time
			self.state = -1 *  self.state


def between ( x,  val1, val2) : # return val1 <= x <= val2
	return (val1 <= x and x <= val2)
	
def outof ( x,  val1, val2) : # return val1 > x  or  x > val2
	return (not(between(x, val1, val2)))
	
def check_speed_axis_for_gaz (speed_axis, gaz) : 
	return (outof(speed_axis, -0.1, 0.1) and not(gaz)) or ( between(speed_axis, -0.1, 0.1) and gaz )

if __name__ == '__main__':

	#Test du joystick present
	try:
		is_joystick = True
		is_mouse = False
		joystick = pygame.joystick.Joystick(0)
		joystick.init()

	except:
		is_joystick = False
		is_mouse = True
				
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
			
		robot = corrected_robot([leg1, leg2, leg3, leg4, leg5, leg6], [leg1, leg3, leg5], [leg2, leg4, leg6])

		

		robot.goto([0, 0, 0])
	
		
		continuer = True
		gaz=False
		remind_button = 0
		button = 0
		joy_x_axis = 0
		joy_y_axis = 0
		speed_axis = 0
		
		while continuer:
			
			if is_joystick : 
				button = joystick.get_button(3)
				joy_x_axis = joystick.get_axis(0)
				joy_y_axis = joystick.get_axis(1)
				speed_axis = joystick.get_axis(2)
			
			for event in pygame.event.get():	#Attente des evenements
				if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
					continuer = False
				if event.type == KEYDOWN and event.key == K_TAB:
							is_joystick = not(is_joystick)
							is_mouse = not(is_mouse)
				if is_mouse and event.type == MOUSEMOTION : #Si mouvement de souris
					#On change les coordonnees du Reticule
					Reticulte_x = event.pos[0]-L_Reticule/2
					Reticulte_y = event.pos[1]-H_Reticule/2
				if (event.type == MOUSEBUTTONDOWN) or (event.type == KEYDOWN and event.key == K_SPACE) or button==1  or (outof(speed_axis, -0.1, 0.1) and not(gaz)) or check_speed_axis_for_gaz(speed_axis, gaz) :
					gaz = not(gaz)
					if gaz == 1 :
						Reticule = pygame.image.load("../Ressources/Red_Reticule.png").convert_alpha()
						Reticule = pygame.transform.scale(Reticule, (L_Reticule, H_Reticule))				
					else:
						Reticule = pygame.image.load("../Ressources/Reticule.png").convert_alpha()
						Reticule = pygame.transform.scale(Reticule, (L_Reticule, H_Reticule))	


			if is_joystick :
				Reticulte_x = L_Fenetre/2 + (L_Fenetre/2 * joy_x_axis) -L_Reticule/2		
				Reticulte_y = H_Fenetre/2 + (H_Fenetre/2 * joy_y_axis) -H_Reticule/2	
				
			
			period = 1700 - (math.fabs(speed_axis)*1500)
			#Re-collage
			fenetre.blit(fond, (0,0))	
			fenetre.blit(Reticule, (Reticulte_x, Reticulte_y))
			if gaz : 
				robot.moveto([(Reticulte_x - L_Fenetre/2)/coeff_distance, (Reticulte_y - H_Fenetre/2)/coeff_distance, 0], period, 35)
			else : 
				robot.goto([(Reticulte_x - L_Fenetre/2)/coeff_distance, (Reticulte_y - H_Fenetre/2)/coeff_distance, 0])
			remind_button = button
			#Rafraichissement
			pygame.display.flip()