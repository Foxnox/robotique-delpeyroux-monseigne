import math

L1 = 51.0
L2 = 63.7
L3 = 93.0

Alpha = math.radians(20.69)
Beta = math.radians(5.06)

def radian_validation (radian):
	return (radian <= 2 * math.pi and radian >= -2 * math.pi)

def leg_dk(theta1, theta2, theta3, l1=L1, l2=L2, l3=L3, alpha = Alpha, beta = Beta):
	x = y = z = "error"
	if radian_validation(theta1) and radian_validation(theta2) and radian_validation(theta3) and radian_validation(alpha) and radian_validation(beta):
		c_2 = math.cos(theta2)
		d_12 = L2 * c_2;
		
		c_2_3 = math.cos(theta2 + theta3)
		d_23 = L3 * c_2_3
		
		planContribution = (L1 + (L2 * c_2) + (L3 * c_2_3)) 
		
		c_1 = math.cos(theta1)
		c_a = math.cos(alpha)
		s_a = math.sin(alpha)
		c_b = math.cos(beta)
		s_b = math.sin(beta)
		delta_x = (-1 * (L2 * (1 - c_a) * c_1) - (L3 * (1 - s_b) * c_1))
		x = (planContribution * c_1) + delta_x
		
		s_1 = math.sin(theta1)
		delta_y = (-1 * (L2 * (1 - c_a) * s_1) - (L3 * (1 - s_b) * s_1))
		y = (planContribution * s_1) + delta_y
		
		s_2 = math.sin(theta2)
		s_2_3 = math.sin(theta2 + theta3)
		delta_z = -1 * (L2 * s_a) - (L3 * c_b)
		z = (L2 * s_2) + (L3 * s_2_3) + delta_z
	
	print ("["+ str(x) +", " + str(y) + ", " + str(z) +"]")


leg_dk(math.radians(0), math.radians(0), math.radians(0))
leg_dk(math.radians(90), math.radians(0), math.radians(0))
leg_dk(math.radians(180), math.radians(-30.501), math.radians(-67.819))
leg_dk(math.radians(0), math.radians(-30.645), math.radians(38.501))