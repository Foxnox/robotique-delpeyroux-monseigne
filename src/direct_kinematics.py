from math import *
from Vertex import *

#Length of the three subparts of the robot leg
L1 = 51.0
L2 = 63.7
L3 = 93.0

Alpha = radians(20.69)	#Get the radian angle for alpha
Beta = radians(5.06)	#Get the radian angle for beta

# Check if the given float match with radian (between 2PI and -2PI)
def radValidation (radian):
	return (radian <= 2 * pi and radian >= -2 * pi)

# Direct kinamatics for our considered robot (specific of our leg setting)
def leg_dk(theta1, theta2, theta3, l1=L1, l2=L2, l3=L3, alpha = Alpha, beta = Beta):
	if radValidation(theta1) and radValidation(theta2) and radValidation(theta3) and radValidation(alpha) and radValidation(beta):
		#Storing all the sinus and cosinus into variable in order to simplify and run the calculation only once
		c_1 = cos(theta1)
		c_2 = cos(theta2)
		c_2_3 = cos(theta2 + theta3)
		c_a = cos(alpha)
		c_b = cos(beta)
		s_1 = sin(theta1)
		s_2 = sin(theta2)
		s_2_3 = sin(theta2 + theta3)
		s_a = sin(alpha)
		s_b = sin(beta)

		#calculation of the projections and the differences due to the robot setting
		projection_delta = (l2 * (1 - c_a)) + (l3 * (1 - s_b)) 
		projection = l1 + (l2 * c_2) + (l3 * c_2_3)
		
		#Calculation of the final position
		Theorique = Vertex((projection * c_1), (projection * s_1), ((l2 * s_2) + (l3 * s_2_3)))
		Delta = Vertex((c_1*projection_delta), (s_1*projection_delta), ((l2 * s_a) + (l3 * c_b)))
		Final = Theorique - Delta
		
		print (str(Final))
	else:
		print ("Invalide Theta")


leg_dk(radians(0), radians(0), radians(0))
leg_dk(radians(90), radians(0), radians(0))
leg_dk(radians(180), radians(-30.501), radians(-67.819))
leg_dk(radians(0), radians(-30.645), radians(38.501))
