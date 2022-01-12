import os
from pathlib import Path
import sys
import time
#HARDCODE
# TODO Fix this with something appropriate
# TODO Probably planner should register that path
sys.path.append('/mnt/X/WORKSHOP/Violla/Clusters')
from InternalClusterBase import *
import random


class Cluster(InternalCluster):
	def __init__(self, *args):
		self.random_phrases = ["I'm bored.", "Boring...", "There's nothing going on.", "...", "This place is such a mess.", "This is not what i'm supposed to do with my life.", "This is your fault."]
		super().__init__(*args)
		# TODO mpve into linguistics
		

	def dispatch(self, request):
		if "fine" in request.lower():
			return json.dumps({"type":"done", "message": "Fine. Do whatever you want."})
		# TODO define as sort of constant
		if "no responce" in request.lower():
			return json.dumps({"type":"info", "message": "Don't ignore me I'm serious."})
		#print("Child method called")
		return json.dumps({"type":"info", "message": random.choice(["I do't wanna hear a thing.", "It's a... No."])})

	def payload(self):
		while True:
			#TODO Set this parameters from config
			time.sleep(random.randint(1,5))
			phrase = random.choice(self.random_phrases)
			yield json.dumps({"type":"info", "message": phrase})



if __name__ == '__main__':

	#TODO - find a better way to send description to module
	#TODO - find a better way to run module in test mode

	if TEST:
		_id, violla_port , variation = TEST_CLUSTER_ID, TEST_VIOLLA_PORT, TEST_CLUSTER_CONFIG
	else:
		_id, violla_port, variation = sys.argv[1:4]

	cluster = Cluster(_id, int(violla_port), variation)
	cluster.act()
