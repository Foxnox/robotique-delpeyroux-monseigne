import itertools
import time
import numpy
import inverse_kinematics
import direct_kinematics
from contextlib import closing
import pypot.robot

def get_position (angles):
	pos = direct_kinematics.leg_dk(angles[0], angles[1], angles[2])
	return [ pos.posx, pos.posy, pos.posz ]
	
def get_angles (pos):
	angles = inverse_kinematics.leg_ik(pos[0], pos[1], pos[2])
	return [ angles.posx, angles.posy, angles.posz ]
	
def megabot_goto (megabot, leg, pos, duration):
	angles = get_angles(pos)
	motors = [m.name for m in leg]
	cmd = dict(zip(motors, angles))
	megabot.goto_position(cmd, duration)


if __name__ == '__main__':
	with closing(pypot.robot.from_json('config.json')) as megabot:
		for m in megabot.motors : 
			m.compliant = False;

		megabot_goto(megabot, megabot.leg1, [50, 0, -150], 2)
			
		
		