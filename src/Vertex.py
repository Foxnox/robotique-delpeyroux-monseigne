import math

#Class Vertex
class Vertex:
	#Arg
	posx = 0
	posy = 0
	posz = 0

	def __init__(self, posx=0, posy=0, posz=0):
		self.posx = posx
		self.posy = posy
		self.posz = posz

	#Surcharge str
	def __str__(self):
		return ("("+ str(self.posx) +", " + str(self.posy) + ", " + str(self.posz) +")")

	#Surcharge +=
	def __iadd__(self, other):
		self.posx += other.posx
		self.posy += other.posy
		self.posz += other.posz
		return self

	#Surcharge +
	def __add__(self, other):
		temp = Vertex()
		temp.posx = self.posx + other.posx
		temp.posy = self.posy + other.posy
		temp.posz = self.posz + other.posz
		return temp

	#Surcharge -=
	def __isub__(self, other):
		self.posx -= other.posx
		self.posy -= other.posy
		self.posz -= other.posz
		return self

	#Surcharge -
	def __sub__(self, other):
		temp = Vertex()
		temp.posx = self.posx - other.posx
		temp.posy = self.posy - other.posy
		temp.posz = self.posz - other.posz
		return temp

P1 = Vertex()
print "Ceci est P1 " + str(P1)+ "\n"
P2 = Vertex(0, 0, 0)
print "Ceci est P2 " + str(P2)+ "\n"
P3 = Vertex(10, 12, -20)
print "Ceci est P3 " + str(P3)+ "\n"
P4 = P3 + P3
print "Ceci est P4 " + str(P4)+ "\n"
P5 = P3 - P3
print "Ceci est P5 " + str(P5)+ "\n"
P6 = P1 + P4
print "Ceci est P6 " + str(P6)+ "\n"
P6 += P4
print "Ceci est P6 " + str(P6)+ "\n"
P6 -= P4
print "Ceci est P6 " + str(P6)+ "\n"