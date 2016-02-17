import itertools
import time
import numpy
import pypot.dynamixel
import inverse_kinematics
import direct_kinematics

def get_position (angles):
	pos = direct_kinematics.leg_dk(angles[2], angles[1], angles[0])
	return [ pos.posx, pos.posy, pos.posz ]
	
def get_angles (pos):
	angles = inverse_kinematics.leg_ik(pos[0], pos[1], pos[2])
	return [ angles.posz, angles.posy, angles.posx ]
	
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
	# we first open the Dynamixel serial port
	with pypot.dynamixel.DxlIO('/dev/ttyUSB0', baudrate=1000000) as dxl_io:

		# we can scan the motors
		ids = [10, 11, 12]
		
		# we power on the motors
		dxl_io.disable_torque(ids)
		# we get the current positions
		
		pos = dxl_io.get_present_position(ids)
		print 'Current pos (angles):', pos
		
		space_pos = get_position(pos)
		print 'Current pos (in space - DK):', space_pos
		
		angles_pos = get_angles(space_pos)
		print 'Current pos (angles - IK):', angles_pos
		
		
		
		while True : 
			target = [200, 0, 0]
			target[0] = float(raw_input("Please enter a X coordinate: "))
			target[1] = float(raw_input("Please enter a Y coordinate: "))
			target[2] = float(raw_input("Please enter a Z coordinate: "))
			print ""
			goto(dxl_io, target, ids)
		# we send these new positions
		#dxl_io.set_goal_position(pos)
		
		#sinusoide(dxl_io, 10, 0.5, found_ids)
		