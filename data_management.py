


def create_block(name,firstName,entitle):
	nameFirstnameEntitle = name + '_' + firstName + '_' + entitle
	path = "./{}_{}/".format(name.replace(" ","-"),firstName.replace(" ","-"))

	if len(nameFirstnameEntitle) < 64:
		nameFirstnameEntitle = str(nameFirstnameEntitle).zfill(64)

	else:
		nameFirstnameEntitle = str(nameFirstnameEntitle)[0:64]

	fichier = open("{}timestamp_sign.tsr".format(path), "rb")

	timestamp_ascii = ''
	while 1:
		c = fichier.read(1)
		if c : 
			timestamp_ascii += hex(c[0])[2:].zfill(2)
		else :
			break

	block = nameFirstnameEntitle + timestamp_ascii
	return block




def cut_block(block):
	information = block[:64]
	timestamp_ascii = block[64:]


	while (information[0]== '0'):
		information = information[1:]

	
	cut_block = [information,timestamp_ascii]
	information = cut_block[0].split('_')
	name = information[0]
	firstName = information[1]
	entitle = information[2]
	return(name, firstName, entitle, timestamp_ascii)


