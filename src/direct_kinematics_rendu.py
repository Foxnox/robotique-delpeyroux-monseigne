from math import *

def isNumber (number):
	return isinstance(number, (int, float))

##########DEBUT DE LA CLASSE VERTEX##########
class Vertex:
	#Arguments
	posx = 0.0
	posy = 0.0
	posz = 0.0

	def __init__(self, posx=0.0, posy=0.0, posz=0.0):
		if (isNumber(posx) and isNumber(posy) and isNumber(posz)):
			self.posx = float(posx)
			self.posy = float(posy)
			self.posz = float(posz)
		else:
			print("Vertex Invalide")

	#Surcharge str
	def __str__(self):
		return ("(%.1f, %.1f, %.1f)" % (self.posx,self.posy,self.posz))

	#Surcharge +=
	def __iadd__(self, other):
		if isNumber(other):
			other = Vertex(other, other, other)
		if isinstance(other, Vertex):
			self.posx += other.posx
			self.posy += other.posy
			self.posz += other.posz
			return self
		else:
			return NotImplemented

	#Surcharge +
	def __add__(self, other):
		if isNumber(other):
			other = Vertex(other, other, other)
		temp = Vertex()
		if isinstance(other, Vertex):
			temp.posx = self.posx + other.posx
			temp.posy = self.posy + other.posy
			temp.posz = self.posz + other.posz
			return temp
		else:
			return NotImplemented

	#Surcharge -=
	def __isub__(self, other):
		if isNumber(other):
			other = Vertex(other, other, other)
		if isinstance(other, Vertex):
			self.posx -= other.posx
			self.posy -= other.posy
			self.posz -= other.posz
			return self
		else:
			return NotImplemented

	#Surcharge -
	def __sub__(self, other):
		if isNumber(other):
			other = Vertex(other, other, other)
		temp = Vertex()
		if isinstance(other, Vertex):
			temp.posx = self.posx - other.posx
			temp.posy = self.posy - other.posy
			temp.posz = self.posz - other.posz
			return temp
		else:
			return NotImplemented

	#Surcharge ==
	def __eq__(self, other):
		if isinstance(other, Vertex):
			return (self.posx == other.posx and self.posy == other.posy and self.posz == other.posz)
		else:
			return NotImplemented
##########FIN DE LA CLASSE##########

"""
##########PARTIE TEST##########
P1 = Vertex()
print ("Ceci est P1 " + str(P1))
P2 = Vertex(0, 0, 0)
print ("Ceci est P2 " + str(P2))
P3 = Vertex(10, 12, -20)
print ("Ceci est P3 " + str(P3))
P4 = P3 + P3
print ("Ceci est P4 " + str(P4))
P5 = P3 - P3
print ("Ceci est P5 " + str(P5))
P6 = P1 + P4
print ("Ceci est P6 " + str(P6))
P6 += P4
print ("Ceci est P6 " + str(P6))
P6 -= P4
print ("Ceci est P6 " + str(P6))
print (P6 == P1)
print (P6 == P6)
P6+=1
print ("Ceci est P6 " + str(P6)+ "\n")
"""

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
