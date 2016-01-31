import math

L1 = 51.0
L2 = 63.7
L3 = 93.0

Alpha = math.radians(20.69)	#Conversion des degrés en radian
Beta = math.radians(5.06)	#Conversion des degrés en radian

def radian_validation (radian):
	return (radian <= 2 * math.pi and radian >= -2 * math.pi)

def leg_dk(theta1, theta2, theta3, l1=L1, l2=L2, l3=L3, alpha = Alpha, beta = Beta):
	x = y = z = "error"
	if radian_validation(theta1) and radian_validation(theta2) and radian_validation(theta3) and radian_validation(alpha) and radian_validation(beta):
		#Calcul des différents cosinus et sinus
		c_1 = math.cos(theta1)
		c_2 = math.cos(theta2)
		c_2_3 = math.cos(theta2 + theta3)
		c_a = math.cos(alpha)
		c_b = math.cos(beta)
		s_1 = math.sin(theta1)
		s_2 = math.sin(theta2)
		s_2_3 = math.sin(theta2 + theta3)
		s_a = math.sin(alpha)
		s_b = math.sin(beta)
		#Calcul des projections
		projection_delta = (l2 * (1 - c_a)) + (l3 * (1 - s_b)) 
		projection = l1 + (l2 * c_2) + (l3 * c_2_3) 
		delta_x = c_1*projection_delta
		delta_y = s_1*projection_delta
		delta_z = (l2 * s_a) + (l3 * c_b)
		#Calcul de la position
		x = (projection * c_1) - delta_x
		y = (projection * s_1) - delta_y
		z = (l2 * s_2) + (l3 * s_2_3) - delta_z
	
	print ("["+ str(x) +", " + str(y) + ", " + str(z) +"]")


leg_dk(theta1=math.radians(0), theta2=math.radians(0), theta3=math.radians(0))
leg_dk(theta1=math.radians(90), theta2=math.radians(0), theta3=math.radians(0))
leg_dk(theta1=math.radians(180), theta2=math.radians(-30.501), theta3=math.radians(-67.819))
leg_dk(theta1=math.radians(0), theta2=math.radians(-30.645), theta3=math.radians(38.501))