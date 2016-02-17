import itertools
import time
import numpy
import pypot.dynamixel
import inverse_kinematics
import direct_kinematics

def get_position (dxl_io, theta1, theta2, theta2):
	direct_kinematics.leg_dk(theta1, theta2, theta3)

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
	# we first open the Dynamixel serial port
	with pypot.dynamixel.DxlIO('/dev/ttyUSB0', baudrate=1000000) as dxl_io:

		# we can scan the motors
		found_ids = [10, 11, 12]
		
		# we power on the motors
		dxl_io.enable_torque(found_ids)

		# we get the current positions
		print 'Current pos:', dxl_io.get_present_position(found_ids)

		#	found_ids[0] -> 3 (ID inscrite sur le moteur)
		#	found_ids[1] -> 14 (ID inscrite sur le moteur)
		#	found_ids[2] -> 17 (ID inscrite sur le moteur) 
		# we create a python dictionnary: {id0 : position0, id1 : position1...}
		ids = { found_ids[0] : 11, found_ids[1] : 12, found_ids[2] : 10}
		#print 'Cmd:', pos
		
		i = 0
		final_ids = found_ids[:]
		for key, value in ids.iteritems() : 
			final_ids[i] = change_id(dxl_io, key, value)
			i += 1

		print "Final Ids : ", final_ids
		# we send these new positions
		#dxl_io.set_goal_position(pos)
		
		#sinusoide(dxl_io, 10, 0.5, found_ids)
		
		time.sleep(1)  # we wait for 1s

		# we power off the motors
		dxl_io.disable_torque(final_ids)
		time.sleep(1)  # we wait for 1s