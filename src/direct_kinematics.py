import math

#Length of the three subparts of the robot leg
L1 = 51.0
L2 = 63.7
L3 = 93.0

Alpha = math.radians(20.69)	#Get the radian angle for alpha
Beta = math.radians(5.06)	#Get the radian angle for beta

# Check if the given float match with radian (between 2PI and -2PI)
def radian_validation (radian):
	return (radian <= 2 * math.pi and radian >= -2 * math.pi)

# Direct kinamatics for our considered robot (specific of our leg setting)
def leg_dk(theta1, theta2, theta3, l1=L1, l2=L2, l3=L3, alpha = Alpha, beta = Beta):
	x = y = z = "error"
	if radian_validation(theta1) and radian_validation(theta2) and radian_validation(theta3) and radian_validation(alpha) and radian_validation(beta):
		#Storing all the sinus and cosinus into variable in order to simplify and run the calculation only once
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

		#calculation of the projections and the differences due to the robot setting
		projection_delta = (l2 * (1 - c_a)) + (l3 * (1 - s_b)) 
		projection = l1 + (l2 * c_2) + (l3 * c_2_3) 
		delta_x = c_1*projection_delta
		delta_y = s_1*projection_delta
		delta_z = (l2 * s_a) + (l3 * c_b)
		
		#Calculation of the final position
		x = (projection * c_1) - delta_x
		y = (projection * s_1) - delta_y
		z = (l2 * s_2) + (l3 * s_2_3) - delta_z
	
	print ("["+ str(x) +", " + str(y) + ", " + str(z) +"]")


leg_dk(theta1=math.radians(0), theta2=math.radians(0), theta3=math.radians(0))
leg_dk(theta1=math.radians(90), theta2=math.radians(0), theta3=math.radians(0))
leg_dk(theta1=math.radians(180), theta2=math.radians(-30.501), theta3=math.radians(-67.819))
leg_dk(theta1=math.radians(0), theta2=math.radians(-30.645), theta3=math.radians(38.501))