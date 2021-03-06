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
	

def leg_ik(x, y, z, l1=L1, l2=L2, l3=L3, alpha = Alpha, beta = Beta):
	
	l_proj = sqrt(x*x + y*y)
	d13 = l_proj - l1
	d = sqrt(z*z + d13*d13)
	
	if (d13 == 0):
		a = 0
	else : 
		a = atan(z/d13)
		
	if (d==0):
		b = 0
	else:
		b = al_kashi(l3, l2, d)
	
	if (x == 0):
		theta1 = 0
	else:
		theta1 = atan(y/x)
		
	theta2 = b + a
	theta3 = pi - al_kashi(d, l3, l2)
	
	angle = Vertex(degrees(theta1), degrees(theta2), degrees(theta3))
	
	print(str(angle))
	
leg_ik(118.79, 0.0, -115.14)
leg_ik(0.0, 118.79, -115.14)
leg_ik(-64.14, 0.0, -67.79)
leg_ik(203.23, 0.0, -14.30)
