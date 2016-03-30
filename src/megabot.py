import itertools
import time
import numpy
import inverse_kinematics
import direct_kinematics
import math
from contextlib import closing
import pypot.robot

center_pos = [100, 0, -100]

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

def leg_goto(leg, pos):
	angles = get_angles(pos)
	i = 0
	for m in leg :
		m.goal_position = angles[i]
		i += 1

class corrected_leg:
	leg = None
	delta_angle = 0
	
	def __init__(self, leg, delta_angle):
		self.leg = leg
		self.delta_angle = delta_angle
		
	def get_corrected_angle(self, initial_angle):
		return initial_angle - self.delta_angle
		
	def goto_angle_dist(self, angle, dist):
		my_angle = self.get_corrected_angle(angle)
		dy = math.sin(math.radians(my_angle)) * dist 
		dx = math.cos(math.radians(my_angle)) * dist
		
		goal_pos = [center_pos[0]+dx, center_pos[1]+dy, center_pos[2]]
		leg_goto(self.leg, goal_pos)
		 
	
class corrected_robot:
	legs = []
	
	def __init__(self, legs):
		self.legs = legs
	
	def goto_angle_dist(self, angle, dist):
		for l in self.legs:
			l.goto_angle_dist(angle, dist)
	
def position_centre (megabot, deltax, deltay, time):
	z=-100
	x=100
	y=0
	
	megabot_goto(megabot, megabot.leg1, [x+deltax, y-deltay, z], time)

	megabot_goto(megabot, megabot.leg3, [x+deltay, y-deltax, z], time)
	megabot_goto(megabot, megabot.leg5, [x-deltay, y+deltax, z], time)


	megabot_goto(megabot, megabot.leg4, [x-deltax, y+deltay, z], time)

	megabot_goto(megabot, megabot.leg2, [x+deltay, y-deltax, z], time)
	megabot_goto(megabot, megabot.leg6, [x-deltay, y+deltax, z], time)
	
def position_avant (megabot):
	z=-100
	x=100
	y=0
	delta=50
	
	megabot_goto(megabot, megabot.leg1, [x, y, z], 0.1)

	megabot_goto(megabot, megabot.leg3, [x, y-delta, z], 0.1)
	megabot_goto(megabot, megabot.leg5, [x, y+delta, z], 0.1)


	megabot_goto(megabot, megabot.leg4, [x+delta, y, z], 0.1)

	megabot_goto(megabot, megabot.leg2, [x, y, z], 0.1)
	megabot_goto(megabot, megabot.leg6, [x, y, z], 0.1)

def position_arriere (megabot):
	z=-100
	x=100
	y=0
	delta=50
	
	megabot_goto(megabot, megabot.leg1, [x+delta, y, z], 0.1)

	megabot_goto(megabot, megabot.leg3, [x, y, z], 0.1)
	megabot_goto(megabot, megabot.leg5, [x, y, z], 0.1)


	megabot_goto(megabot, megabot.leg4, [x, y, z], 0.1)

	megabot_goto(megabot, megabot.leg2, [x, y+delta, z], 0.1)
	megabot_goto(megabot, megabot.leg6, [x, y-delta, z], 0.1)


def make_circle(megabit):
	z=-100
	x=100
	y=0
	delta=50
	

if __name__ == '__main__':
	#On va maintenant utiliser un fichier de configuration
	#Il nous permettra de limiter nos demandes aux angles valides
	with closing(pypot.robot.from_json('config.json')) as megabot:
		for m in megabot.motors : 
			m.compliant = False;

		leg1 = corrected_leg(megabot.leg1, 0)
		leg2 = corrected_leg(megabot.leg2, -90)
		leg3 = corrected_leg(megabot.leg3, -90)
		leg4 = corrected_leg(megabot.leg4, -180)
		leg5 = corrected_leg(megabot.leg5, 90)
		leg6 = corrected_leg(megabot.leg6, 90)
			
		robot = corrected_robot([leg1, leg2, leg3, leg4, leg5, leg6])

		position_centre(megabot, 0,0,0.2)
		
		time.sleep(3)
		angle = 0
		while True:
			robot.goto_angle_dist(angle, 30)
			angle += 20
			if (angle == 360):
				angle = 0
			time.sleep(0.8)


		
		
		
		
		