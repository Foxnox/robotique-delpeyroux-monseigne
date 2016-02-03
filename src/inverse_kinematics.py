from math import *
from Vertex import *

#Length of the three subparts of the robot leg
L1 = 51.0
L2 = 63.7
L3 = 93.0

Alpha = radians(20.69)	#Get the radian angle for alpha
Beta = radians(5.06)	#Get the radian angle for beta

# return opppisite angle of the side a of the tringle defined by a, b and c 
def al_kashi (a, b , c):
	return acos((b*b + c*c - a*a)/(2 * b * c))
	
# Inverse kinematic. Return the three angles (theta1, theta2, theta3) according the given position 
def leg_ik(x, y, z, l1=L1, l2=L2, l3=L3, alpha = Alpha, beta = Beta):
	l_max = l1+l2+l3
	l_proj = sqrt(x*x + y*y)
	if ((x*x + y*y + z*z) <= l_max*l_max):
		d13 = l_proj - l1
		d = sqrt(z*z + d13*d13)
	
		if (d13 == 0):
			a = 0
		else : 
			a = atan2(z, d13)
		
		if (d==0):
			b = 0
		else:
			b = al_kashi(l3, l2, d)
		
		if (x == 0):
			theta1 = pi/2
		elif (x < 0 and y == 0) :
			theta1=pi
		else:
			theta1 = atan2(y, x)
			
		theta2 = - (b + a + alpha)
		theta3 = - (pi - al_kashi(d, l3, l2) - ((pi/2) - alpha - beta))
			
		angle = Vertex(degrees(theta1), degrees(theta2), degrees(theta3))
		print("Voici les angles en degrees : " + str(angle))
	else:
		print("C'est pas une super pate extensible")

	
leg_ik(118.79, 0.0, -115.14)
leg_ik(0.0, 118.79, -115.14)
leg_ik(-64.14, 0.0, -67.79)
leg_ik(203.23, 0.0, -14.30)
