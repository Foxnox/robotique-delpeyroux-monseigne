from math import *
from Vertex import *

#Length of the three subparts of the robot leg
L1 = 51.0
L2 = 63.7
L3 = 93.0

Alpha = 20.69	#Contrainte mecanique sur Theta 2
Beta = 5.06		#Contrainte mecanique sur Theta 3

# Check if the given float match with radian (between 2PI and -2PI)
def radValidation (radian):
	return (radian <= 2 * pi and radian >= -2 * pi)

# Direct kinamatics for our considered robot (specific of our leg setting)
def leg_dk(theta1, theta2, theta3, l1=L1, l2=L2, l3=L3, alpha = Alpha, beta = Beta):
	Angle = Vertex(theta1,theta2,theta3)
	#Modification de theta 2 et theta 3 en fonction des contraintes mecaniques
	theta2  +=  alpha
	theta3	=	90-(alpha+beta+theta3)
	#print "Angles : " + str(theta1) + " ; " + str(theta2) + " ; " + str(theta3)
	theta1=radians(theta1)
	theta2=-radians(theta2)
	theta3=-radians(theta3)
		
	#Storing all the sinus and cosinus into variable in order to simplify and run the calculation only once
	c_1 = cos(theta1)
	c_2 = cos(theta2)
	c_2_3 = cos(theta2 + theta3)
	s_1 = sin(theta1)
	s_2 = sin(theta2)
	s_2_3 = sin(theta2 + theta3)

	#calculation of the projections and the differences due to the robot setting
	projection = l1 + (l2 * c_2) + (l3 * c_2_3)
	
	#Calculation of the final position
	Final = Vertex((projection * c_1), (projection * s_1), ((l2 * s_2) + (l3 * s_2_3)))
	
	return Final


leg_dk(0, 0, 0)
leg_dk(90, 0, 0)
leg_dk(180, -30.501, -67.819)
leg_dk(0, -30.645, 38.501)
