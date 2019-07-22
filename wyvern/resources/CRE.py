from wyvern.resources.Resource import Resource
from wyvern import wyvern
from struct import pack 
import pandas as pd 

CRE_V1_Fields = {
	# variable name: (datatype,offset)
	'long_name': ('strref',0x08),
	'short_name': ('strref',0x0c),
	'flags': ('dword',0x10), # this will be expanded later
	'xp_value': ('dword',0x14),
	'xp': ('dword',0x18),
	'gold': ('dword',0x1c),
	'status_flags': ('dword',0x20),
	'hp_current': ('word',0x24),
	'hp_max': ('word',0x26),
	'animation': ('dword',0x28),
	'color_metal': ('byte',0x2c),
	'color_minor': ('byte',0x2d),
	'color_major': ('byte',0x2e),
	'color_skin': ('byte',0x2f),
	'color_leather': ('byte',0x30),
	'color_armor': ('byte',0x31),
	'color_hair': ('byte',0x32),
	'eff_version': ('byte',0x33),
	'portrait_small': ('resref',0x34),
	'portrait_large': ('resref',0x3c),
	'reputation': ('signed byte',0x44),
	'skill_hide': ('byte',0x45),
	'ac_natural': ('signed word',0x46),
	'ac_effective': ('signed word',0x48),
	'ac_crushing_mod': ('signed word',0x4a),
	'ac_missile_mod': ('signed word',0x4c),
	'ac_piercing_mod': ('signed word',0x4e),
	'ac_slashing_mod': ('signed word',0x50),
	'thac0': ('byte',0x52),
	'num_attacks': ('byte',0x53),
	'save_vs_death': ('byte',0x54),
	'save_vs_wands': ('byte',0x55),
	'save_vs_poly': ('byte',0x56),
	'save_vs_breath': ('byte',0x57),
	'save_vs_spells': ('byte',0x58),
	'res_fire': ('byte',0x59),
	'res_cold': ('byte',0x5a),
	'res_electricity': ('byte',0x5b),
	'res_acid': ('byte',0x5c),
	'res_magic': ('byte',0x5d),
	'res_magic_fire': ('byte',0x5e),
	'res_magic_cold': ('byte',0x5f),
	'res_slashing': ('byte',0x60),
	'res_crushing': ('byte',0x61),
	'res_piercing': ('byte',0x62),
	'res_missile': ('byte',0x63),
	'skill_detect_illusion': ('byte',0x64),
	'skill_set_traps': ('byte',0x65),
	'lore': ('byte',0x66),
	'skill_pick_locks': ('byte',0x67),
	'skill_stealth': ('byte',0x68),
	'skill_find_traps': ('byte',0x69),
	'skill_pick_pockets': ('byte',0x6a),
	'fatigue': ('byte',0x6b),
	'intoxication': ('byte',0x6c),
	'luck': ('byte',0x6d),
	#0x7b: ('byte','pstee_prof_unspent'),
	#0x7c: ('byte','pstee_inventory_slots'),
	'bgee_nightmare_mode_active': ('byte',0x7d),
	'bgee_translucency': ('byte',0x7e),
	'rep_change_on_kill': ('byte',0x7f),
	'rep_change_on_join': ('byte',0x80),
	'rep_change_on_leave': ('byte',0x81),
	'turn_undead_lvl': ('byte',0x82),
	'skill_tracking': ('byte',0x83),
	#0x84: ('char array','bgee_tracking_target')
	'sound_initial_meeting': ('strref',0xa4),
	'sound_morale': ('strref',0xa8),
	'sound_happy': ('strref',0xac),
	# I'll add sounds in later 
	'level_class_1': ('byte',0x234),
	'level_class_2': ('byte',0x235),
	'level_class_3': ('byte',0x236),
	'sex': ('byte',0x237),
	'strength': ('byte',0x238),
	'strength_ex': ('byte',0x239),
	'intelligence': ('byte',0x23a),
	'wisdom': ('byte',0x23b),
	'dexterity': ('byte',0x23c),
	'constitution': ('byte',0x23d),
	'charisma': ('byte',0x23e),
	'morale': ('byte',0x23f),
	'morale_break': ('byte',0x240),
	'racial_enemy': ('byte',0x241),
	'morale_recovery': ('word',0x242),
	'kit': ('dword',0x244),
	'script_override': ('resref',0x248),
	'script_class': ('resref',0x250),
	'script_race': ('resref',0x258),
	'script_general': ('resref',0x260),
	'script_default': ('resref',0x268),
	'id_enemy_ally': ('byte',0x270),
	'id_general': ('byte',0x271),
	'id_race': ('byte',0x272),
	'id_class': ('byte',0x273),
	'id_specific': ('byte',0x274),
	'id_gender': ('byte',0x275),
	'id_object_1': ('byte',0x276),
	'id_object_2': ('byte',0x277),
	'id_object_3': ('byte',0x278),
	'id_object_4': ('byte',0x279),
	'id_object_5': ('byte',0x27a),
	'id_alignment': ('byte',0x27b),
	'global_identifier': ('word',0x27c),
	'local_identifier': ('word',0x27e),
	'death_var': ('char array',0x280), 
	'spells_known_offset': ('offset',0x2a0),
	'spells_known_count': ('dword',0x2a4),
	'spells_memorized_info_offset': ('offset',0x2a8),
	'spells_memorized_info_count': ('dword',0x2ac),
	'spells_memorized_offset': ('offset',0x2b0),
	'spells_memorized_count': ('dword',0x2b4),
	'item_slots_offset': ('offset',0x2b8),
	'items_offset': ('offset',0x2bc),
	'items_count': ('dword',0x2c0),
	'effects_offset': ('offset',0x2c4),
	'effects_count': ('dword',0x2c8),
	'dialog_file': ('resref',0x2cc),
	

}

# CRE_V1_Slots provides the offset from the item_slots_offset to the actual item slot of interest. 
CRE_V1_Slots = {
	'helmet': (0x00),
	'armor': (0x02),
	'shield': (0x04),
	'gloves': (0x06),
	'ring_left': (0x08),
	'ring_right': (0x0a),
	'amulet': (0x0c),
	'belt': (0x0e),
	'boots': (0x10),
	'weapon_1': (0x12),
	'weapon_2': (0x14),
	'weapon_3': (0x16),
	'weapon_4': (0x18),
	'quiver_1': (0x1a),
	'quiver_2': (0x1c),
	'quiver_3': (0x1e),
	'quiver_4': (0x20),
	'cloak': (0x22),
	'quick_1': (0x24),
	'quick_2': (0x26),
	'quick_3': (0x28),
	'inventory_1': (0x2a),
	'inventory_2': (0x2c),
	'inventory_3': (0x2e),
	'inventory_4': (0x30),
	'inventory_5': (0x32),
	'inventory_6': (0x34),
	'inventory_7': (0x36),
	'inventory_8': (0x38),
	'inventory_9': (0x3a),
	'inventory_10': (0x3c),
	'inventory_11': (0x3e),
	'inventory_12': (0x40),
	'inventory_13': (0x42),
	'inventory_14': (0x44),
	'inventory_15': (0x46),
	'inventory_16': (0x48),
	'magical_weapon': (0x4a),
	'selected_weapon': (0x4c),
	'selected_ability': (0x4e),
}

Creature_Flags = { 
	# flag: bit 
	'show_long_name_tooltip': 0, 
	'no_corpse': 1,
	'permanent_corpse': 2, 
	'original_class_fighter': 3, 
	'original_class_mage': 4, 
	'original_class_cleric': 5, 
	'original_class_thief': 6, 
	'original_class_druid': 7, 
	'original_class_ranger': 8,
	'fallen_paladin': 9,
	'fallen_ranger': 10,
	'exportable': 11,
	'hide_injury_status': 12, 
	# IESDP and NI disagree on what bit 13 represents
	'moves_between_areas': 14,
	'was_in_party': 15,
	# unsure about bit 16/17
	# bit 18/19 unused
	'disable_exploding_death': 20, 
	# bit 21 unused 
	'ignore_nightmare_mode': 22,
	'disable_tooltip': 23, 
	'track_allegiance': 24,
	'track_general': 25, 
	'track_race': 26,
	'track_class': 27,
	'track_specific': 28,
	'track_gender': 29, 
	'track_alignment': 30, 
	'uninterruptible': 31,
}

class CRE(Resource):


	def __init__(self,resource,version=1.0,**kwargs):
		# resource is a string: [name].[ext]
		ressplit = resource.split('.')
		self.resource = resource
		self.resref = ressplit[0]
		self.ext = ressplit[1]
		self.version = version

		# These are intentionally inaccessible outside of this function. 
		# Use the databases, not these. 
		spells_known_list = list()
		items_list = list()
		memorized_info_list = list()
		memorized_spell_list = list()

		if wyvern.get_resource_raw(resource):
			# If the resource already exists, populate fields with values. 
			self.data = wyvern.get_resource_raw(resource)
			self.size = len(self.data)
			if self.version == 1.0: 

				# main creature info 
				for key in CRE_V1_Fields: 
					datatype,offset = CRE_V1_Fields[key]
					if datatype == 'strref': 
						setattr(self,key,self._read_long(offset,signed=True))
					elif datatype == 'dword': 
						setattr(self,key,self._read_long(offset))
					elif datatype == 'word': 
						setattr(self,key,self._read_short(offset))
					elif datatype == 'byte':
						setattr(self,key,self._read_byte(offset))
					elif datatype == 'resref':
						setattr(self,key,self._read_ascii(offset))
					elif datatype == 'char array': 
						setattr(self,key,self._read_ascii(offset,length=32))
					elif datatype == 'offset':
						setattr(self,key,self._read_long(offset))
					elif datatype == 'signed byte': 
						setattr(self,key,self._read_byte(offset,True))
					elif datatype == 'signed word':
						setattr(self,key,self._read_short(offset,True))
				'''
				# to be dealt with later	
				for key in Creature_Flags: 
					bit = Creature_Flags[key]
					if (self.flags > bit) & 1: 
						setattr(self,key,1)
					else:
						setattr(self,key,0)
				'''
				# known spells 
				for i in range(0,self.spells_known_count):
					offset = self.spells_known_offset + i*0xc
					resname = self._read_ascii(offset)
					level = self._read_short(offset+0x8)+1
					spell_type = self._read_short(offset+0xa)
					spells_known_list.append([resname,level,spell_type])
				
				self.spells_known_table = pd.DataFrame(spells_known_list,columns=['SpellRes','Level','Type'])

				# memorization info 
				for i in range(0,self.spells_memorized_info_count):
					offset = self.spells_memorized_info_offset + i*0x10
					level = self._read_short(offset)+1
					max_memorizable = self._read_short(offset+0x2)
					cur_memorizable = self._read_short(offset+0x4)
					spell_type = self._read_short(offset+0x6) 
					spell_index = self._read_long(offset+0x8)
					spell_count = self._read_long(offset+0xc)
					memorized_info_list.append([level,max_memorizable,cur_memorizable,spell_type,spell_index,spell_count])
				
				self.memorized_info_table = pd.DataFrame(memorized_info_list,columns=['Level','Maximum','Current','Type','Index','Count'])
				
				# memorized spells 
				for i in range(0,self.spells_memorized_count):
					offset = self.spells_memorized_offset + i*0xc
					resname = self._read_ascii(offset)
					flags = self._read_long(offset+0x8)
					memorized = flags & 1 
					disabled = (flags > 1)  & 1
					memorized_spell_list.append([resname,memorized,disabled])
				
				self.memorized_spell_table = pd.DataFrame(memorized_spell_list,columns=['SpellRes','Memorized','Disabled'])
				
				# items 
				for i in range(0,self.items_count):
					offset = self.items_offset + i*0x14
					resname = self._read_ascii(offset)
					duration = self._read_short(offset+0x8)
					charges_1 = self._read_short(offset+0xa)
					charges_2 = self._read_short(offset+0xc)
					charges_3 = self._read_short(offset+0xe)
					flags = self._read_long(offset+0x10)
					identified = flags & 1 
					unstealable = (flags > 1) & 1 
					stolen = (flags > 1) & 1 
					undroppable = (flags > 1) & 1 
					items_list.append([resname,duration,charges_1,charges_2,charges_3,identified,unstealable,stolen,undroppable])
					
				self.items_table = pd.DataFrame(items_list,columns=['ItemRes','Duration','Charges_1','Charges_2','Charges_3','Identified','Unstealable','Stolen','Undroppable'])
				
				# inventory slot use 
				for key in CRE_V1_Slots: 
					offset = CRE_V1_Slots[key] + self.item_slots_offset
					setattr(self,key,self._read_short(offset,True))
						
		else:
			if self.version == 1.0: 
				for key in CRE_V1_Fields: 
					datatype,offset = CRE_V1_Fields[key]
					if datatype == 'strref': 
						setattr(self,key,-1)
					elif datatype == 'dword': 
						setattr(self,key,0)
					elif datatype == 'word': 
						setattr(self,key,0)
					elif datatype == 'byte':
						setattr(self,key,0)
					elif datatype == 'resref':
						setattr(self,key,'None')
					elif datatype == 'char array': 
						setattr(self,key,'')
					elif datatype == 'offset':
						setattr(self,key,0x2d4)
					# signed needs handling for negatives
					elif datatype == 'signed byte': 
						setattr(self,key,0)
					elif datatype == 'signed word':
						setattr(self,key,0)

				for key in CRE_V1_Slots: 
					offset = CRE_V1_Slots[key] + self.item_slots_offset
					if (key == 'selected_weapon') or (key == 'selected_ability'):
						setattr(self,key,0)
					else: 
						setattr(self,key,-1)

				# You only need to setup the empty dataframes. 
				self.items_table = pd.DataFrame(items_list,columns=['ItemRes','Duration','Charges_1','Charges_2','Charges_3','Identified','Unstealable','Stolen','Undroppable'])
				self.memorized_spell_table = pd.DataFrame(memorized_spell_list,columns=['SpellRes','Memorized','Disabled'])
				self.spells_known_table = pd.DataFrame(spells_known_list,columns=['SpellRes','Level','Type'])
				self.memorized_info_table = pd.DataFrame(memorized_info_list,columns=['Level','Maximum','Current','Type','Index','Count'])


	def update_data(self): 
		# This function will update the bytecode with any changes made using the fields. 
		length = self.item_slots_offset + 0x50
		self.data = bytearray(length)
		self.data[:8] = 'CRE V1.0'.encode('ascii')
		if self.version == 1.0: 
			for key in CRE_V1_Fields: 
				datatype,offset = CRE_V1_Fields[key]
				if datatype == 'strref': 
					self.data[offset:offset+4] = getattr(self,key).to_bytes(4,'little',signed=True)
				elif datatype == 'dword': 
					self.data[offset:offset+4] = getattr(self,key).to_bytes(4,'little')
				elif datatype == 'word': 
					self.data[offset:offset+2] = getattr(self,key).to_bytes(2,'little')
				elif datatype == 'byte':
					self.data[offset:offset+1] = getattr(self,key).to_bytes(1,'little')
				elif datatype == 'resref':
					self.data[offset:offset+8] = pack('8s', getattr(self,key).encode('ascii'))
				elif datatype == 'char array': 
					self.data[offset:offset+32] = pack('32s', getattr(self,key).encode('ascii'))
				elif datatype == 'offset':
					self.data[offset:offset+4] = getattr(self,key).to_bytes(4,'little')
				elif datatype == 'signed byte': 
					self.data[offset:offset+1] = getattr(self,key).to_bytes(1,'little',signed=True)
				elif datatype == 'signed word':
					self.data[offset:offset+2] = getattr(self,key).to_bytes(2,'little',signed=True)

			for key in CRE_V1_Slots: 
				offset = CRE_V1_Slots[key] + self.item_slots_offset
				self.data[offset:offset+2] = getattr(self,key).to_bytes(2,'little',signed=True)

			for index, row in self.spells_known_table.iterrows(): 
				offset = self.spells_known_offset + index*0xc
				self.data[offset:offset+8] = pack('8s', row['SpellRes'].encode('ascii'))
				self.data[offset+0x8:offset+0xa] = int((row['Level']-1)).to_bytes(2,'little')
				self.data[offset+0xa:offset+0xc] = row['Type'].to_bytes(2,'little')
			
			for index, row in self.memorized_info_table.iterrows(): 
				offset = self.spells_memorized_info_offset + index*0x10
				self.data[offset:offset+0x2] = int((row['Level']-1)).to_bytes(2,'little')
				self.data[offset+0x2:offset+0x4] = int(row['Maximum']).to_bytes(2,'little')
				self.data[offset+0x4:offset+0x6] = int(row['Current']).to_bytes(2,'little')
				self.data[offset+0x6:offset+0x8] = int(row['Type']).to_bytes(2,'little')
				self.data[offset+0x8:offset+0xc] = int(row['Index']).to_bytes(4,'little')
				self.data[offset+0xc:offset+0x10] = int(row['Count']).to_bytes(4,'little')
			

			for index, row in self.memorized_spell_table.iterrows(): 
				offset = self.spells_memorized_offset + index*0xc
				self.data[offset:offset+8] = pack('8s', row['SpellRes'].encode('ascii'))
				self.data[offset+0x8:offset+0xc] = (2*row['Disabled']+1*row['Memorized']).to_bytes(4,'little')
			
			for index, row in self.items_table.iterrows(): 
				offset = self.items_offset + index*0x14
				self.data[offset:offset+8] = pack('8s', row['ItemRes'].encode('ascii'))
				self.data[offset+0x8:offset+0xa] = row['Duration'].to_bytes(2,'little')
				self.data[offset+0xa:offset+0xc] = row['Charges_1'].to_bytes(2,'little')
				self.data[offset+0xc:offset+0xe] = row['Charges_2'].to_bytes(2,'little')
				self.data[offset+0xe:offset+0x10] = row['Charges_3'].to_bytes(2,'little')
				self.data[offset+0x10:offset+0x14] = (8*row['Undroppable']+ 4*row['Stolen'] + 2*row['Unstealable']+1*row['Identified']).to_bytes(4,'little')
		
		self.data = bytes(self.data)
		

	def set_minimum_stats(self): 
		# This function sets current and max HP and all ability scores to 1 
		# This prevents generated creatures from dying immediately on load. 
		setattr(self,'hp_max',1)
		setattr(self,'hp_current',1)
		setattr(self,'strength',1)
		setattr(self,'dexterity',1)
		setattr(self,'constitution',1)
		setattr(self,'intelligence',1)
		setattr(self,'wisdom',1)
		setattr(self,'charisma',1)

	def pretty_print(self): 
		# This shows the creature data in a human-readable format in the command line.
		# I need to expand this to cover all stats. 
		# Format should evoke a character sheet. 
		print('-----------------------------------------------------') 
		print('{} [{} v{}]'.format(self.resref,self.ext.upper(),self.version))
		print('{} ({})'.format(wyvern.get_string(getattr(self,'long_name')),wyvern.get_string(getattr(self,'short_name'))))
		print('Str {} ({}) / Dex {} / Con {} / Int {} / Wis {} / Cha {}'.format(getattr(self,'strength'),getattr(self,'strength_ex'),getattr(self,'dexterity'),getattr(self,'constitution'),getattr(self,'intelligence'),getattr(self,'wisdom'),getattr(self,'charisma')))
		print('HP {}/{} / AC {}'.format(getattr(self,'hp_current'),getattr(self,'hp_max'),getattr(self,'ac_effective')))
		print('-----------------------------------------------------')