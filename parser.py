import re
import binascii

def parse(data, port, origin):
	#print ("[{}({})] -> {}".format(origin, port, data.hex()))
	print ("[{}({})] -> {}".format(origin, port, data.decode('utf-8')))

def modify(data):
	#new_data = binascii.hexlify(data)+b"\x0a"
	
	new_data = ""
	for i in data.decode("utf-8").split("\n"):
		new_data += re.sub("^User-Agent:+[\x20-\x7F]*","User-Agent: Modified-Through-Proxy\n",i)
	new_data = new_data.encode('utf-8')
	
	#new_data = data
	return new_data
