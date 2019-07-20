from wyvern.resources.Resource import Resource
from wyvern import wyvern

CRE_V1_Fields = {
	0x08: ('strref','long_name'),
	0x0c: ('strref','short_name'),
	0x10: ('dword','flags'), # this will be expanded later
	0x14: ('dword','xp_value'),
	0x18: ('dword','xp'),
	0x1c: ('dword','gold'),
	0x20: ('dword','status_flags'),
	0x24: ('word','hp_current'),
	0x26: ('word','hp_max'),
	0x28: ('dword','animation'),
	0x2c: ('byte','color_metal'),
	0x2d: ('byte','color_minor'),
	0x2e: ('byte','color_major'),
	0x2f: ('byte','color_skin'),
	0x30: ('byte','color_leather'),
	0x31: ('byte','color_armor'),
	0x32: ('byte','color_hair'),
	0x33: ('byte','eff_version'),
	0x34: ('resref','portrait_small'),
	0x3c: ('resref','portrait_large'),
	0x44: ('signed byte','reputation'),
	0x45: ('byte','skill_hide'),
	0x46: ('signed word','ac_natural'),
	0x48: ('signed word','ac_effective'),
	0x4a: ('signed word','ac_crushing_mod'),
	0x4c: ('signed word','ac_missile_mod'),
	0x4e: ('signed word','ac_piercing_mod'),
	0x50: ('signed word','ac_slashing_mod'),
	0x52: ('byte','thac0'),
	0x53: ('byte','num_attacks'),
	0x54: ('byte','save_vs_death'),
	0x55: ('byte','save_vs_wands'),
	0x56: ('byte','save_vs_poly'),
	0x57: ('byte','save_vs_breath'),
	0x58: ('byte','save_vs_spells'),
	0x59: ('byte','res_fire'),
	0x5a: ('byte','res_cold'),
	0x5b: ('byte','res_electricity'),
	0x5c: ('byte','res_acid'),
	0x5d: ('byte','res_magic'),
	0x5e: ('byte','res_magic_fire'),
	0x5f: ('byte','res_magic_cold'),
	0x60: ('byte','res_slashing'),
	0x61: ('byte','res_crushing'),
	0x62: ('byte','res_piercing'),
	0x63: ('byte','res_missile'),
	0x64: ('byte','skill_detect_illusion'),
	0x65: ('byte','skill_set_traps'),
	0x66: ('byte','lore'),
	0x67: ('byte','skill_pick_locks'),
	0x68: ('byte','skill_stealth'),
	0x69: ('byte','skill_find_traps'),
	0x6a: ('byte','skill_pick_pockets'),
	0x6b: ('byte','fatigue'),
	0x6c: ('byte','intoxication'),
	0x6d: ('byte','luck'),
	#0x7b: ('byte','pstee_prof_unspent'),
	#0x7c: ('byte','pstee_inventory_slots'),
	0x7d: ('byte','bgee_nightmare_mode_active'),
	0x7e: ('byte','bgee_translucency'),
	0x7f: ('byte','rep_change_on_kill'),
	0x80: ('byte','rep_change_on_join'),
	0x81: ('byte','rep_change_on_leave'),
	0x82: ('byte','turn_undead_lvl'),
	0x83: ('byte','skill_tracking'),
	#0x84: ('char array','bgee_tracking_target')
	0xa4: ('strref','sound_initial_meeting'),
	0xa8: ('strref','sound_morale'),
	0xac: ('strref','sound_happy'),
	# I'll add sounds in later 
	0x234: ('byte','level_class_1'),
	0x235: ('byte','level_class_2'),
	0x236: ('byte','level_class_3'),
	0x237: ('byte','sex'),
	0x238: ('byte','strength'),
	0x239: ('byte','strength_ex'),
	0x23a: ('byte','intelligence'),
	0x23b: ('byte','wisdom'),
	0x23c: ('byte','dexterity'),
	0x23d: ('byte','constitution'),
	0x23e: ('byte','charisma'),
	0x23f: ('byte','morale'),
	0x240: ('byte','morale_break'),
	0x241: ('byte','racial_enemy'),
	0x242: ('word','morale_recovery'),
	0x244: ('dword','kit'),
	0x248: ('resref','script_override'),
	0x250: ('resref','script_class'),
	0x258: ('resref','script_race'),
	0x260: ('resref','script_general'),
	0x268: ('resref','script_default'),
	0x270: ('byte','id_enemy_ally'),
	0x271: ('byte','id_general'),
	0x272: ('byte','id_race'),
	0x273: ('byte','id_class'),
	0x274: ('byte','id_specific'),
	0x275: ('byte','id_gender'),
	0x276: ('byte','id_object_1'),
	0x277: ('byte','id_object_2'),
	0x278: ('byte','id_object_3'),
	0x279: ('byte','id_object_4'),
	0x27a: ('byte','id_object_5'),
	0x27b: ('byte','id_alignment'),
	0x27c: ('word','global_identifier'),
	0x27e: ('word','local_identifier'),
	0x280: ('char array','death_var'), 
	# I'll add in spell/item/effect handling later 
	0x2cc: ('resref','dialog_file')



}

class CRE(Resource):
	def __init__(self,resource,version=1.0,**kwargs):
		# resource is a string: [name].[ext]
		ressplit = resource.split('.')
		self.resource = resource
		self.resref = ressplit[0]
		self.ext = ressplit[1]
		self.version = version

		if wyvern.get_resource_raw(resource):
			# If the resource already exists, populate fields with values. 
			self.data = wyvern.get_resource_raw(resource)
			self.size = len(self.data)
			if self.version == 1.0: 
				for key in CRE_V1_Fields: 
					datatype,var = CRE_V1_Fields[key]
					if datatype == 'strref': 
						setattr(self,var,self.read_long(key))
					elif datatype == 'dword': 
						setattr(self,var,self.read_long(key))
					elif datatype == 'word': 
						setattr(self,var,self.read_short(key))
					elif datatype == 'byte':
						setattr(self,var,self.read_byte(key))
					elif datatype == 'resref':
						setattr(self,var,self.read_ascii(key))
					elif datatype == 'char array': 
						setattr(self,var,self.read_ascii(key,length=32))
					# signed needs handling for negatives
					elif datatype == 'signed byte': 
						setattr(self,var,self.read_byte(key,True))
					elif datatype == 'signed word':
						setattr(self,var,self.read_short(key,True))
		else:
			self.data = None 
			self.size = 0

				
