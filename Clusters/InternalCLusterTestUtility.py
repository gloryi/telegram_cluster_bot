from InternalClusterBase import *

				# with os.open.open(self._stream_to, os.O_SYNC | os.O_CREAT | os.O_RDWR) as stream_to, os.open(self._stream_from, os.O_RDONLY) as stream_from:
				# #	s.connect(('127.0.0.1', self.violla_port))

				# 	while True:
				# 		os.write(stream_to, idea)
				# 		violla_responce = os.read(in2, 2048)
				# 		idea = self.dispatch(violla_responce)
				# 		#VIOLLA WILL CLOSE LINK BY HERSELF ON "DONE"
				# #		s.sendall(idea.encode(encoding='UTF-8'))
				# 		#violla_responce = ""
				# 		#while True:
				# #		violla_responce = s.recv(2048).decode()
				# 		#violla_responce+=responce_part
				# 		#if not responce_part:
				# 		#break
				# 			#violla_responce     =   
				# 		#if not violla_responce:
				# 		#	continue

				# #		print("violla say", violla_responce)
				# 		# TODO make version not requiring direct send call

				# 		idea 				= self.dispatch(violla_responce)


stream_from   = os.open(stream_FROM_violla, os.O_SYNC | os.O_CREAT | os.O_RDWR)
stream_to     = os.open(stream_TO_violla, os.O_RDONLY)

# with os.open(stream_FROM_violla, os.O_SYNC | os.O_CREAT | os.O_RDWR) as stream_from, os.open(stream_TO_violla, os.O_RDONLY) as stream_to:
while True:
	request = os.read(stream_to, 2048).decode()
	data 				= json.loads(request)
	print("Responded with", data["message"])
	if "done" in data["type"].lower():
		os.close(stream_to)
		os.close(stream_from)
		break
	print(request)
	payload_resolution  = input(" <<< ")
	os.write(stream_from, payload_resolution.encode(encoding='utf-8'))



# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
# 	s.bind(('127.0.0.1', TEST_VIOLLA_PORT))
# 	s.listen()
# 	while True:
# 		print("Waiting for requests from Clusters")
# 		violla_link, violla_addr = s.accept()
# 		try:
# 			with violla_link:
# 				print("Violla asked for something from ", violla_addr)
# 				#WHILE CONECTION?
# 				while True:
# 					#VIOLLA WILL CLOSE LINK BY HERSELF ON "DONE"
# 					#TODO be carefull with byte like objects ~ file // picture
# 					request 			= violla_link.recv(2048).decode()
# 					data 				= json.loads(request)
# 					print("Responded with", data["message"])
# 					if "done" in data["type"].lower():
# 					#s.close()
# 						violla_link.shutdown(socket.SHUT_WR)
# 						violla_link.close()
# 						break
# 					print(request)
# 					payload_resolution  = input(" <<< ")

# 					violla_link.sendall(payload_resolution.encode(encoding='utf-8'))
# 		except Exception as e:
# 			print(e)