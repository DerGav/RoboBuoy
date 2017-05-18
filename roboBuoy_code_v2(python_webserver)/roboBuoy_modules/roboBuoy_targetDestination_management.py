# this file contains python code to manage roboBuoy's target destinations

import pickle

# For now lets hardcode all possible targets in this list.
# In future they should be read from a file or database.
#
# List entries are objects which contain a 'group_name'
# and another list of 'coordinates' which are part of that group.
# Coordinate objects contain a 'target_name' plus 'Lat' and 'Long' values
target_destinations = [
	{'group_name' : 'Desal Plant Site Characterization',
	 'coordinates': [
	{'target_name': 'DESAL - A', 'Lat': 36.615505, 'Long': -121.894724},
	{'target_name': 'DESAL - B', 'Lat': 36.615785, 'Long': -121.894876},
	{'target_name': 'DESAL - C', 'Lat': 36.616061, 'Long': -121.895023},
	{'target_name': 'DESAL - D', 'Lat': 36.616301, 'Long': -121.895218},
	{'target_name': 'DESAL - E', 'Lat': 36.616558, 'Long': -121.895371}
	]
	},

	{'group_name' : 'CSUMB Pool',
	 'coordinates': [
	{'target_name': 'North side of CSUMB pool',
	'Lat': 36.651503, 'Long': -121.807078},
	{'target_name': 'South side of CSUMB pool',
	'Lat': 36.651364, 'Long': -121.807128}
	]
	},

	{'group_name' : 'Other Locations',
	 'coordinates': [
	{'target_name': 'Squid Mops',
	'Lat': 36.36621 , 'Long': -121.53171 },
	{'target_name': 'Sand Dollar Bed',
	'Lat': 36.623883, 'Long': -121.907348},
	{'target_name': 'Carmel River Canyon',
	'Lat': 36.535028, 'Long': -121.938936}
	]
	}
]

# function designed to be called from another file to get the target list
# for now this simply returns the list above
def get_target_destinations():
	return target_destinations

def load_target_destinations():
	print("load_target_destinations")
	#reload object from file
	save_file = open("target_destinations.txt", 'rb')
	if save_file:
		target_destinations = pickle.load(save_file)
		save_file.close
		return target_destinations
	else:
		return []

def save_target_destinations(targt_destinations):
	#open file
	save_file = open("target_destinations.txt",'wb')
	if save_file:
		#write to it
		pickle.dump(target_destinations, save_file)
		save_file.close()
		return "success"
	else:
		return "error"
if __name__ == '__main__':
	global target_destinations
	save_target_destinations(target_destinations)
	new = load_target_destinations()
	print new
