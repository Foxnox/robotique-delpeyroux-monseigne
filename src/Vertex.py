import math

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
		return ("(%.1f, %.1f, %.1f" % (self.posx,self.posy,self.posz))

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