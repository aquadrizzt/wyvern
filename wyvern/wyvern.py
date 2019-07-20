from struct import *
import time 
import os 
from os import path 
import mmap 
import matplotlib 
import matplotlib.pyplot as plt 
from wyvern import resources

ResourceTypeID = {
	1 : 'BMP',
	2 : 'MVE', 
	4 : 'WAV',
	5 : 'WFX',
	6 : 'PLT',
	952 : 'TGA',
	1000 : 'BAM',
	1001 : 'WED',
	1002 : 'CHU',
	1003 : 'TIS',
	1004 : 'MOS',
	1005 : 'ITM',
	1006 : 'SPL',
	1007 : 'BCS',
	1008 : 'IDS',
	1009 : 'CRE',
	1010 : 'ARE',
	1011 : 'DLG',
	1012 : '2DA',
	1013 : 'GAM',
	1014 : 'STO',
	1015 : 'WMP',
	1016 : 'EFF',
	1017 : 'BS',
	1018 : 'CHR',
	1019 : 'VVC',
	1020 : 'VEF',
	1021 : 'PRO',
	1022 : 'BIO',
	1023 : 'WBM',
	1024 : 'FNT',
	1026 : 'GUI',
	1027 : 'SQL',
	1028 : 'PVRZ',
	1029 : 'GLSL',
	1030 : 'TOT',
	1031 : 'TOH',
	1032 : 'MENU',
	1033 : 'LUA',
	1034 : 'TTF',
	1035 : 'PNG',
	1100 : 'BAH',
	2050 : 'INI',
	2051 : 'SRC',
	2052 : 'MAZE',
	4094 : 'MUS',
	4095 : 'ACM',
}
			
def read_key(key):
	with open(key,"r+b") as f:
		# HEADER
		sigver = f.read(8).decode('ascii')
		if sigver != 'KEY V1  ':
			raise ValueError('Invalid KEY signature')
		f.seek(8)
		bifcount = unpack('L',f.read(4))[0]
		f.seek(12)
		rescount = unpack('L',f.read(4))[0]
		f.seek(16)
		bifoff = unpack('L',f.read(4))[0]
		f.seek(20)
		resoff = unpack('L',f.read(4))[0]
		#print(bifcount, rescount, bifoff, resoff)

		# resources
		keyresources = list()
		for i in range(0,rescount):
			f.seek(resoff + 14 * i)
			resname = unpack('8s',f.read(8))[0].decode('ascii')
			f.seek(resoff + 14 * i + 8)
			restype = unpack('H',f.read(2))[0] 
			f.seek(resoff + 14 * i + 10)
			reslocator = unpack('L',f.read(4))[0]
			bifindex = reslocator>>20
			reslocator_nobif = reslocator - (bifindex << 20)
			if reslocator_nobif >> 14:
				resindex = reslocator_nobif 
			else:
				resindex = reslocator_nobif
			keyresources.append((resname,restype,bifindex,resindex))
			#print(resname,restype,bifindex,resindex)

		# bifs 
		keybifs = list()
		bif_indices = dict()
		for i in range(0,bifcount):
			f.seek(bifoff + 12 * i)
			biflength = unpack('L',f.read(4))[0]
			f.seek(bifoff + 12 * i + 4)
			bifnameoff = unpack('L',f.read(4))[0]
			f.seek(bifoff + 12 * i + 8)
			bifnamelength = unpack('H',f.read(2))[0]
			f.seek(bifoff + 12 * i + 10)
			biflocflag = unpack('H',f.read(2))[0]
			f.seek(bifnameoff)
			bifname = unpack(str(bifnamelength-1)+'s',f.read(bifnamelength-1))[0].decode('ascii')
			#print(type(bifname))
			keybifs.append((bifname,i,biflength,biflocflag))
			bif_indices[i] = bifname
			# print(bifname, i, biflength,biflocflag)

		key_data = dict()
		# key_data[bifindex][resindex] returns the unpacked byte code of the resource numbered resindex in the the bif numbered bifindex

		for bif in keybifs: 
			key_data[bif[1]] = read_bif(bif[0])
		#print(key_data)

		res_data = dict()
		for res in keyresources:
			resname = res[0]
			restype = res[1]
			bifindex = res[2]
			resindex = res[3] 
			if ResourceTypeID.get(restype) == 'TIS':
				#filename = resname.rstrip('\x00').upper()+'.'+ResourceTypeID.get(restype)
				#res_data[filename] = key_data[bifindex][resindex]
				pass
			elif ResourceTypeID.get(restype):
				filename = resname.rstrip('\x00').upper()+'.'+ResourceTypeID.get(restype)
				res_data[filename] = key_data[bifindex][resindex]
			else: 
				if restype == 0: 
					pass
				else: 
					print('Invalid file type: ',resname, restype, format(restype,'03x'))

	return res_data 
	#print(resname,restype,bif_indices[bifindex])
	#print(resname,restype)

def read_bif(bif):
	# bif is the bif file (with .bif extension)
	with open(bif,"r+b") as f:
		#print(type(bif))
		# HEADER
		sigver = f.read(8).decode('ascii')
		if sigver != 'BIFFV1  ':
			raise ValueError('Invalid decompressed BIFF signature')
		f.seek(8)
		filecount = unpack('L',f.read(4))[0]
		f.seek(12)
		tsetcount = unpack('L',f.read(4))[0]
		f.seek(16)
		entryoff = unpack('L',f.read(4))[0]

		resources = list()
		key_resources = dict()
		# resources
		for i in range(0,filecount):
			f.seek(entryoff)
			reslocator = unpack('L',f.read(4))[0]
			f.seek(entryoff + 4)
			resoff = unpack('L',f.read(4))[0]
			f.seek(entryoff + 8)
			ressize = unpack('L',f.read(4))[0]
			f.seek(entryoff + 12)
			restype = unpack('H',f.read(2))[0]
			resources.append((reslocator,resoff,ressize,restype))
			f.seek(resoff)
			#key_resources[reslocator] = pack(str(ressize)+'s',f.read(ressize))
			#key_resources[reslocator] = repr(unpack(str(ressize)+'s',f.read(ressize))[0])
			key_resources[reslocator] = f.read(ressize)
			#print((reslocator,resoff,ressize,restype))
			entryoff = entryoff + 16
		

		tilesets = list()
		# tilesets 
		for i in range(0,tsetcount):
			f.seek(entryoff)
			reslocator = unpack('L',f.read(4))[0]
			f.seek(entryoff + 4)
			resoff = unpack('L',f.read(4))[0]
			f.seek(entryoff + 8)
			tilecount = unpack('L',f.read(4))[0]
			f.seek(entryoff + 12)
			tilesize = unpack('L',f.read(4))[0]
			f.seek(entryoff + 16)
			restype = unpack('H',f.read(2))[0]
			tilesets.append((reslocator,resoff,tilecount,tilesize,restype))
			#f.seek(resoff)
			#key_resources[reslocator] = f.read(ressize)
			entryoff = entryoff + 20

		return key_resources

		# do stuff with resources/tilesets here
		'''for resource in resources:
			f.seek(resource[1] + 716)
			dialog = unpack('8s',f.read(8))[0].decode('utf-8')
		'''
		#print(dialog)
	#print("Loaded:",bif)

#t = time.time()
#data = read_key('chitin.key')
def save_to_override(name,data):
	file = open(path.join(path.abspath(path.dirname(sys.argv[0])),'override',name),'wb')
	file.write(data)
	file.close()

def get_resource_raw(resource):
	# this returns the bytes making up the desired resource (as found in keydata)
	return keydata.get(resource.upper())

def get_resource(resource):
	data = get_resource_raw(resource)
	if data: 
		sig = data[:4].decode('ascii')
		ver = float(data[5:8].decode('ascii'))
		if sig == 'CRE ':
			parsed = resources.CRE.CRE(resource,ver)
		return parsed
	else:
		return None

def locate_resource(resource):
	if path.isfile('./override/'+resource):
		return 'override'
	elif keydata.get(resource.upper()): 
		return 'keydata'
	else: 
		return 'none'
		
def get_file(resource):
	# input resref.xyz
	# output filename of resref.xyz in override
	if path.isfile('./override/'+resource):
		#print('File in override')
		file = path.join(path.abspath(path.dirname(sys.argv[0])),'override',resource)
	else:
		#print('File not found')
		file = None
	#data = get_resource_raw(resource) 
	return file

	
global keydata 
keydata = read_key('chitin.key')
