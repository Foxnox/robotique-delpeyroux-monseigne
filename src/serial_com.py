#!/usr/bin/python
# -*- coding: utf-8 -*-

import serial
import math

class Data:
	start = 0xff
	id = 0x00
	lenght = 0x00
	instruction = 0x00
	param1 = 0x00
	param2 = 0x00
	param3 = 0x00
	checksum = 0x00
	data = ''
	
	def __init__(self, start = 0xff, id = 0x00, lenght = 0x00, instruction = 0x00, param1 = 0x00, param2 = 0x00, param3 = 0x00):
		self.start = start
		self.id = id
		self.lenght = lenght
		self.instruction = instruction
		self.param1 = param1
		self.param2 = param2
		self.param3 = param3
		self.checksum = id + lenght + instruction
		self.data = chr(start) + chr(start) + chr(id) + chr(lenght) + chr(instruction)
		if lenght > 2
			self.data +=chr(param1)
			self.checksum += param1
			if lenght > 3
				self.data +=chr(param2)*
				self.checksum += param2
				if lenght > 4
					self.data +=chr(param3)
					self.checksum += param3
					
		self.checksum = ~(self.checksum) & 255
		self.data += self.checksum

def open_serial(port, baud, to):
	ser = serial.Serial(port=port, baudrate=baud, timeout=to)
	if ser.isOpen():
		return ser
	else:
		print 'SERIAL ERROR'

def close(ser):
	ser.close()

def write_data(ser, data):
	ser.write(data)

def read_data(ser, size=1):
	return ser.read(size)

def to_hex(val):
	return chr(val)

def decode_data(data):
	res = ''
	for d in data:
		res += hex(ord(d)) + ' '
	return res

def get_checksum(value):
	ret = ~value & 255
	return ret

def ping_all_ids (serial_port):	
	for i in range(254):
		start = 0xff
		id = i
		lenght = 0x02
		instruction = 0x01
		param1 = 0x00
		param2 = 0x00
		checksum = get_checksum(id + lenght + instruction)
		
		#Transformation en Char des caracteres Hexa
		data_start = to_hex(start)
		data_id = to_hex(id)
		data_lenght = to_hex(lenght)
		data_instruction = to_hex(instruction)
		data_param1 = to_hex(param1)
		data_param2 = to_hex(param2)
		data_checksum = to_hex(checksum)
		
		# Concatenation de tout ces Char
		data = data_start + data_start + data_id + data_lenght + \
		data_instruction + data_checksum	
	
		write_data(serial_port, data)		#print decode_data(data)
		d = read_data(serial_port, 6)		# read the status packet (size 6)
		print str(i) + " : " + decode_data(d)

def read_pos (serial_port, target):
	start = 0xff
	id = target
	lenght = 0x04		# lenght = 2 + nombres de parametres
	instruction = 0x02	# action de lecture, prend 2 parametres
	param1 = 0x03		# adresse de la position
	param2 = 0x01		# taille de la position en memoire
	checksum = get_checksum(id + lenght + instruction + param1 + param2)

	#Transformation en Char des caracteres Hexa
	data_start = to_hex(start)
	data_id = to_hex(id)
	data_lenght = to_hex(lenght)
	data_instruction = to_hex(instruction)
	data_param1 = to_hex(param1)
	data_param2 = to_hex(param2)
	data_checksum = to_hex(checksum)
	# Concatenation de tout ces Char
	data = data_start + data_start + data_id + data_lenght + \
	data_instruction + data_checksum	
	
	write_data(serial_port, data)		#print decode_data(data)
	d = read_data(serial_port, 6)		# read the status packet (size 6)
	print decode_data(d)

def write_pos (serial_port, target, value):
	start = 0xff
	id = target
	lenght = 0x05 			# lenght = 2 + nombres de parametres
	instruction = 0x03 		# action d'ecriture, prend 2 parametres
	param1 = 0x1e 			# adresse de la position
	param2 = value & 255	# taille de la position en memoire
	param3 = value >> 8		#
	checksum = get_checksum(id + lenght + instruction + param1 + param2)
	
	#Transformation en Char des caracteres Hexa
	data_start = to_hex(start)
	data_id = to_hex(id)
	data_lenght = to_hex(lenght)
	data_instruction = to_hex(instruction)
	data_param1 = to_hex(param1)
	data_param2 = to_hex(param2)
	data_checksum = to_hex(checksum)
	# Concatenation de tout ces Char
	data = data_start + data_start + data_id + data_lenght + \
	data_instruction + data_checksum	
	
	write_data(serial_port, data)		#print decode_data(data)
	d = read_data(serial_port, 6)		# read the status packet (size 6)
	print decode_data(d)

if __name__ == '__main__':

	# Ouverture du port USB0 a uen frequence de 1000000Hz (1MHz) et un timeout de 0.1 
	serial_port = open_serial('/dev/ttyUSB0', 1000000 , 0.1)
	read_pos(serial_port, 14)