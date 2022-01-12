import os
from pathlib import Path
import sys
import random
#HARDCODE
# TODO Fix this with something appropriate
# TODO Probably planner should register that path
sys.path.append('/mnt/X/WORKSHOP/Violla/Clusters')
from ExternalClusterBase import *


class Cluster(ExternalCluster):
	def __init__(self, *args):
		super().__init__(*args)
		self.wait_phrases = ["You\'d better answer", "How long should i wait.", "You either answering me or not.", "I\'ll not wait forever."]

	#TODO definitely not oop style
	def dispatch(self, request):
		if "no responce" in request.lower():
			return json.dumps({"type":"info", "message": random.choice(self.wait_phrases)})

		if "Fine" in request.lower():
			return json.dumps({"type":"done", "message": "Okay, it's over for now."})
		#print("Child method called")
		return json.dumps({"type":"info", "message": "echo "+request})

	def configure(self):
		...


if __name__ == '__main__':

	#TODO - find a better way to send description to module
	if TEST:
		_id, port, variation = TEST_ID, TEST_PORT, TEST_VARIATION
	else:
		_id, port, variation = sys.argv[1:4]
		
	cluster = Cluster(_id, int(port), variation)
	cluster.act()

#c = Cluster(0, 4048, "some_path", "variation")

#print(c.null_action())

	#def __call__(self, violla_message):
	#	#TODO define all phrases in module lingusitcs JSON file
	#	return "Well.... Just repeating " + violla_message + " . So i'm definitely get it."