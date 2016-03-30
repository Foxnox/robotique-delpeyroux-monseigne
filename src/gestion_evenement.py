import itertools
import time
import numpy
import inverse_kinematics
import direct_kinematics
import math

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
#BOUCLE INFINIE
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
	#Rafraichissement
	pygame.display.flip()
