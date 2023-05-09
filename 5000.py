def unicode():
	msg=''
	for i in range(random.randint(150, 200)):
		msg += chr(random.randint(0x1000,0x3000))
	return msg
