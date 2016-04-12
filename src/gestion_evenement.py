import itertools
import time
import numpy
import inverse_kinematics
import direct_kinematics
import math
import sys, os

import pygame
from pygame.locals import *

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

sys.stdout = os.devnull
sys.stderr = os.devnull

pygame.joystick.init()
#BOUCLE INFINIE
continuer = 1
gaz=False


is_mouse = True
is_joystick = False
joy_x_axis = 0
joy_y_axis = 0

while continuer:
	try:
		is_joystick = True
		is_mouse = False
		joystick = pygame.joystick.Joystick(0)
		joystick.init()
	
		joy_x_axis = joystick.get_axis(0)
		joy_y_axis = joystick.get_axis(1)
	except:
		is_joystick = False
		is_mouse = True

	for event in pygame.event.get():	#Attente des evenements
		if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
			continuer = 0
		if event.type == MOUSEMOTION and is_mouse: #Si mouvement de souris
			#On change les coordonnees du Reticule
			Reticulte_x = event.pos[0]-L_Reticule/2
			Reticulte_y = event.pos[1]-H_Reticule/2
		if (event.type == MOUSEBUTTONDOWN or (event.type == KEYDOWN and event.key == K_SPACE)) and is_mouse :
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
	#Re-collage
	fenetre.blit(fond, (0,0))	
	fenetre.blit(Reticule, (Reticulte_x, Reticulte_y))
	#Rafraichissement
	pygame.display.flip()
