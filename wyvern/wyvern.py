from struct import *
import time 
import os 
from os import path 
import mmap 
from wyvern import resources
import sys 
import pandas as pd 
import gettext 

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

def read_tlk(tlk):
	with open(tlk,"r+b") as f:
		# HEADER
		sigver = f.read(8).decode('ascii')
		if sigver != 'TLK V1  ':
			raise ValueError('Invalid TLK signature')
		f.seek(8)
		lang_id = unpack('H',f.read(2))[0]
		#print(lang_id)
		f.seek(10)
		strcount = unpack('L',f.read(4))[0]
		#print(strcount)
		f.seek(14)
		stroffset = unpack('L',f.read(4))[0]
		#print((stroffset-0x12)/strcount)
		entryoffset = 0x12		
		tlk_entries = list()
		for i in range(0,strcount):
			offset = entryoffset + 0x1a * i
			f.seek(offset)
			bitfield = unpack('H',f.read(2))[0]
			# Split bit field into 3 flags 
			has_text = bool(bitfield & 1)
			has_sound = bool((bitfield > 1) & 1)
			has_token = bool((bitfield > 2) & 1)
			f.seek(offset + 0x2)
			# This removes trailing whitespace; be sure to return upon creation of final dialog.tlk. 
			soundres = unpack('8s',f.read(8))[0].decode('ascii').rstrip('\0')
			f.seek(offset + 0xa)
			vol_variance = unpack('L',f.read(4))[0]
			f.seek(offset + 0xe)
			pitch_variance = unpack('L',f.read(4))[0]
			f.seek(offset + 0x12)
			stroffset_rel = unpack('L',f.read(4))[0]
			f.seek(offset + 0x16)
			str_length = unpack('L',f.read(4))[0]
			f.seek(stroffset + stroffset_rel)
			string = unpack(str(str_length)+'s',f.read(str_length))[0].decode('utf-8')

			tlk_entries.append((string,soundres,vol_variance,pitch_variance,has_text,has_sound,has_token,stroffset_rel,str_length))
			#print(resname,restype,bifindex,resindex)

		string_table = pd.DataFrame(tlk_entries,columns=['String','SoundRes','Volume_Variance','Pitch_Variance','Text?','Sound?','Tokens?','Offset_Rel','Length'])

		return string_table

def save_to_override(name,data):
	file = open(path.join(path.abspath(path.dirname(sys.argv[0])),'override',name),'wb')
	file.write(data)
	file.close()

def get_resource_raw(resource):
	# this returns the bytes making up the desired resource (as found in keydata)
	return keydata.get(resource.upper())

def get_resource(resource):
	location = locate_resource(resource)
	
	if location == 'keydata': 
		data = get_resource_raw(resource)
	elif location == 'override':
		data = open(path.join(path.abspath(path.dirname(sys.argv[0])),'override',resource),'rb').read()
	else: 
		print('ERROR: {} not found.'.format(resource))
		return None 
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
		print('ERROR: {} not found in /override/.'.format(resource))
		file = None
	return file

def add_new_string(string,sound_res='',has_tokens=False,volume_variance=0,pitch_variance=0):
	if string: 
		has_text = True
	else:
		has_text = False
	if sound_res: 
		has_sound = True
	else: 
		has_sound = False 

	global new_strings
	new_strings = new_strings.append({'String': string,'SoundRes':sound_res,'Volume_Variance':volume_variance,'Pitch_Variance':pitch_variance,'Text?':has_text,'Sound?':has_sound,'Tokens?':has_tokens,'Offset_Rel':-1,'Length':len(string)},ignore_index=True)
	# at some point, this should return the index for this string in new_tlk, so it can be used in functions, etc. 

def get_string(strref):
	return dialog_table.loc[strref,'String']

def change_string(strref,string):
	# This function allows you to change strings in the original dialog.tlk. 
	# Use add_new_string() to add new strings and <table operations, for now> to change new strings. 
	dialog_table.loc[strref,'String'] = string
	dialog_table.loc[strref,'Length'] = len(string)

def update_dialog_tlk():
	# this should be run at the end of the installer 
	# it does the following 
	# 1) calculates the offsets for each new string 
	# 2) merges the existing dialog table with the new strings 
	# 3) writes to a byte file
	# 4) saves to dialog.tlk location
	#offset = dialog_table['Offset_Rel'].iloc[-1] + dialog_table['Length'].iloc[-1]
	header_length = 0x12
	new_tlk = pd.concat([dialog_table,new_strings],ignore_index=True)
	
	# This updates the offsets of every string based on length. 
	new_tlk['Offset_Rel'] = (26*len(new_tlk)+header_length) + new_tlk.shift(periods=1).fillna(value=0)['Length'].astype(int).cumsum()
	length = new_tlk['Offset_Rel'].iloc[-1] + new_tlk['Length'].iloc[-1]
	dialog_bytes = bytearray(length)

	# header
	dialog_bytes[:8] = 'TLK V1  '.encode('ascii')
	dialog_bytes[0x8:0xa] = (0).to_bytes(2,'little') # this will eventually update with lang_id from dialog.tlk
	dialog_bytes[0xa:0xe] = len(new_tlk).to_bytes(4,'little')
	dialog_bytes[0xe:0x12] = (26*len(new_tlk)+header_length).to_bytes(4,'little')
	
	for index, row in new_tlk.iterrows(): 
		offset = header_length + 0x1a * index
		dialog_bytes[offset:offset+0x2] = (4*row['Tokens?'] + 2*row['Sound?'] + 1*row['Text?']).to_bytes(2,'little')
		dialog_bytes[offset+0x2:offset+0xa] = pack('8s', row['SoundRes'].encode('ascii'))
		dialog_bytes[offset+0xa:offset+0xe] = int(row['Volume_Variance']).to_bytes(4,'little')
		dialog_bytes[offset+0xe:offset+0x12] = int(row['Pitch_Variance']).to_bytes(4,'little')
		dialog_bytes[offset+0x12:offset+0x16] = int(row['Offset_Rel']).to_bytes(4,'little')
		dialog_bytes[offset+0x16:offset+0x1a] = int(row['Length']).to_bytes(4,'little')
		dialog_bytes[(26*len(new_tlk)+header_length)+row['Offset_Rel']:(26*len(new_tlk)+header_length)+row['Offset_Rel']+row['Length']] = pack(str(row['Length'])+'s', row['String'].encode('utf-8'))

	file = open(path.join(path.abspath(path.dirname(sys.argv[0])),'lang/en_US','dialog.tlk'),'wb')
	file.write(dialog_bytes)
	file.close()

def backup_tlk_file(): 
	# this will eventually allow the automatic saving of the original dialog.tlk file 
	pass
	
def load_tlk_from_backup(): 
	# this will allow the restoration of the backup for dialog.tlk file 
	pass 



# This sets up some important data objects for further access by functions. 
# Read game data
global keydata 
keydata = read_key('chitin.key')

# Read dialog.tlk 
global dialog_table 
dialog_table = read_tlk('lang/en_US/dialog.tlk')

# Create new string table
global new_strings 
new_strings = pd.DataFrame(columns=['String','SoundRes','Volume_Variance','Pitch_Variance','Text?','Sound?','Tokens?','Offset_Rel','Length'])
