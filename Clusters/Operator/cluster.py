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
		self.wait_phrases = ["You\'d better answer", "How long should i wait.", "You either answering me or not.", "I\'ll not wait forever.", "You asked me to do this and now not answering."]
		self.resolution_phrases = ["I hope you'll complete just any of that.", "Write does not mean do it. You know.", "Remember about priorities. Just mentioned. Nevermind.", "I doubt that it's really so important, but i'll process it anyway."]
		self.end_phrases = ["I hope so.", "We\'ll see.", "Suppose.", "Whatever.", "You're terrible."]
		self.recall_prases = ["This is what you tracked.", "Some of your useless staff.", "Are you really planning to do all of this?"]

	#TODO definitely not oop style
	def dispatch(self, request):

		if "no responce" in request.lower():
			return json.dumps({"type":"info", "message": random.choice(self.wait_phrases)})


		if "ok" in request.lower():
			return json.dumps({"type":"done", "message": random.choice(self.end_phrases)})


		if "write" in request.lower() or "log" in request.lower():
			# TODO fix hardcodes
			request = request.lower()
			task = request.replace("write","").replace("log","")
			tags = [".wk", ".op", ".b"]
			#TODO better parsing
			token = ".ud"
			for tag in tags:
				if tag in task:
					token = tag
					task = task.replace(tag, "")
					break

			task = task.replace("  "," ")
			record_id     = get_last_record_id("/mnt/X/WORKSHOP/Violla/Clusters/Operator/log.csv")
			log_responce("/mnt/X/WORKSHOP/Violla/Clusters/Operator/log.csv", record_id, entry_a=task, entry_b=token, b_required=True)

			return json.dumps({"type":"info", "message": random.choice(self.resolution_phrases)})

		if "remember" in request.lower() or "recall" in request.lower():
			records = get_records("/mnt/X/WORKSHOP/Violla/Clusters/Operator/log.csv")

			tags = [".wk", ".op", ".b"]

			print(records)

			#records_filtered = 

			selected_tag = "ud"

			for tag in tags:
				if tag in request:
					selected_tag = tag
					break

				#for record in records:
					#print(record[0])
					#print(tag)
					#print(record[0]==tag)
			records = list(filter(lambda _: _[0]==selected_tag, records))

			print(records)

			if "random" in request.lower():
				records = random.sample(records, random.randint(5,8)%len(records))

			if "last" in request.lower():
				records = records[-random.randint(5,8):]

			if "first" in request.lower():
				records = records[:random.randint(5,8)]

			records_formatted = "\n".join([r[1] for r in records])

			return json.dumps({"type":"info", "message": random.choice(self.resolution_phrases)+records_formatted})




			


		#print("Child method called")
		return json.dumps({"type":"info", "message": "I don't really get it, you know "+request})

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