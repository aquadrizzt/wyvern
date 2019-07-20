from wyvern import wyvern
import os 
import sys 
from struct import pack 

class Resource: 
	# name, type, location, size 
	# read/write for byte, short, long, res, string (32)

	def __init__(self,resource,version=1.0):
		# resource is a string: [name].[ext]
		ressplit = resource.split('.')
		self.resource = resource
		self.resref = ressplit[0]
		self.ext = ressplit[1]
		self.version = version

		if wyvern.get_resource_raw(resource):
			self.data = wyvern.get_resource_raw(resource)
			self.size = len(self.data)
		else:
			self.data = None 
			self.size = 0
		

	def save_as(self,name):
		file = open(os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])),'override',name),'wb')
		file.write(self.data)
		file.close()

	def read_ascii(self,offset,length=8):
		# offset is a number (in decimal or 0x.. format)
		return self.data[offset:offset+length].decode('ascii')

	def write_ascii(self,offset,value,length=8):
		# offset is a number (in decimal or 0x.. format)
		data = bytearray(self.data)
		data[offset:offset+length] = pack(str(length)+'s',value.encode('ascii'))
		self.data = bytes(data)

	def read_byte(self,offset,signed=False):
		# offset is a number (in decimal or 0x.. format)
		return int.from_bytes(self.data[offset:offset+1],'little',signed=signed)

	def write_byte(self,offset,value):
		# offset is a number (in decimal or 0x.. format)
		data = bytearray(self.data)
		data[offset:offset+1] = value.to_bytes(1,'little')
		self.data = bytes(data)

	def read_short(self,offset,signed=False):
		# offset is a number (in decimal or 0x.. format)
		return int.from_bytes(self.data[offset:offset+2],'little',signed=signed)

	def write_short(self,offset,value):
		# offset is a number (in decimal or 0x.. format)
		data = bytearray(self.data)
		data[offset:offset+2] = value.to_bytes(2,'little')
		self.data = bytes(data)

	def read_long(self,offset,signed=False):
		# offset is a number (in decimal or 0x.. format)
		return int.from_bytes(self.data[offset:offset+4],'little',signed=signed)

	def write_long(self,offset,value):
		# offset is a number (in decimal or 0x.. format)
		data = bytearray(self.data)
		data[offset:offset+4] = value.to_bytes(4,'little')
		self.data = bytes(data)