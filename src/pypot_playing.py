import itertools
import time
import numpy
import pypot.dynamixel
import inverse_kinematics
import direct_kinematics

def get_position (angles):
	pos = direct_kinematics.leg_dk(angles[0], angles[1], angles[2])
	return [ pos.posx, pos.posy, pos.posz ]
	
def get_angles (pos):
	angles = inverse_kinematics.leg_ik(pos[0], pos[1], pos[2])
	return [ angles.posx, angles.posy, angles.posz ]
	
def goto (dxl_io, pos, ids):
	angles = get_angles(pos)
	cmd = dict(zip(ids, angles))
	dxl_io.set_goal_position(cmd)

def sinusoide (dxl_io, a, f, ids) : 
	initial_time = time.time()
	while True : 
		pos = dict(zip(ids, itertools.repeat(a * numpy.sin( 2 * numpy.pi * f * (time.time()-initial_time)))))
		dxl_io.set_goal_position(pos)

def change_id (dxl_io, old_id, new_id):
	print "Scanning existing Ids ..."
	found_ids = dxl_io.scan()
	if new_id in found_ids : 
		print "Id " + str(new_id) + " already exist !"
		return old_id
	else :
		print "Changing the id " + str(old_id) + " by " + str(new_id)
		dxl_io.change_id({old_id : new_id})
		return new_id

if __name__ == '__main__':
	# On ouvre le port
	with pypot.dynamixel.DxlIO('/dev/ttyUSB0', baudrate=1000000) as dxl_io:
		
		#Test pour trouver les IDs cela ne marche plus si un cable est deffectueux (il ne trouvera rien)
		#found_ids = dxl_io.scan()
		#print found_ids
		
		# Normalement ce sont les bonnes ids 
 		ids = [[11, 12, 13], [21, 22, 23], [31, 32, 33], [41, 42, 43], [51, 52, 53], [61, 62, 63]]

		# Au cas ou on doit changer les IDs
		#dxl_io.change_id(dict(zip(ids, found_ids)))
		
		found_ids = dxl_io.scan()
		print found_ids
		
		# On allume les moteurs
		for i in xrange(0, 6):
			print i
			dxl_io.disable_torque(ids[i])
		
		# Recuperation de la position actuelle
		# pos = dxl_io.get_present_position(ids)
		# print 'Position actuelle (angles):', pos
		# 
		# space_pos = get_position(pos)
		# print 'Position actuelle (in space - DK):', space_pos
		# 
		# angles_pos = get_angles(space_pos)
		# print 'Position actuelle (angles - IK):', angles_pos
		
		
		# Petit test ou on change la position d'une pate avec une suite de position target
		#targets = [[170, -45, 35], [170, -45, 0], [170, -45, 35], [170, 0, 35], [170, 0, 0], [170, 0, 35], [170, 45, 35], [170, 45, 0], [170, 45, 35]]
		# while True:
		# 	for target in targets : 
		# 		goto(dxl_io, target, ids)
		# 		time.sleep(0.25)
		
		
		while True : 
			target = [200, 0, 0]
			nb = int(raw_input("Veuillez entrer un numero de pate : "))
			target[0] = float(raw_input("Veuillez entrer une position sur X : "))
			target[1] = float(raw_input("Veuillez entrer une position sur Y : "))
			target[2] = float(raw_input("Veuillez entrer une position sur Z : "))
			print ""
			goto(dxl_io, target, ids[nb])		# On part sur la nouvelle position
		
		# Petit test ou on change la position sur une sinusoide en fonction du temps 
		#sinusoide(dxl_io, 10, 0.5, found_ids)
		