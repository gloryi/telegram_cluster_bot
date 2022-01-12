from ExternalClusterBase import *



import socket

HOST = '127.0.0.1'  # The server's hostname or IP address  

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, TEST_PORT))
	while True:
		req = input(" <<< ")
		#if req.lower == "done":
		#	s.close()
		#	break
		s.sendall(req.encode(encoding='utf-8'))
		resp = s.recv(2048).decode()
		data = json.loads(resp)
		print("Responded with", data["message"])
		if "done" in data["type"].lower():
			#s.close()
			break
    	#data = s.recv(1024)

#print('Received', repr(data))