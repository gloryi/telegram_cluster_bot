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
		# TODO move all in linguistics
		self.random_curses = ["Do you feel cursed enough?",
							  "Do you really feel cursed enough?"
							  "Do you feel broken enoung?",
							  "Do you really feel broken enoung?",
							 "Do you realy feel useless enough?",
							 "Do you feel useless enough?",
							 "Do you feel hopeless enough?",
							 "Do you really feel hopeless enough?",
							 "This is your fault. This is all your fault.",
							 "You were one who betray. Not one who were betrayed."]

		self.random_phrases = ["There is no time at all. You're late. Always have been. Just like then.",
								"Do a check... Tell me why it's not. Prove it.",
								"Reflect yourself. Now. And i don't wanna hear a regular story. I need insights."
								, "Do a \"screenshot\". Now. Make a note or a two on that.",
								"Burn this moment into retina of your eyes."]
		self.random_glyphs = "ヌフアウエオヤユヨホヘタテイスカンナニラセムチトシハキクマノリレケツサソヒコミモネルメ"
		self.wait_phrases = ["You\'d better answer",
							"How long should i wait.",
							"You either answering me or not.",
							"I\'ll not wait forever.",
							"Don't you find this simlar to your falut?"]
		self.resolution_phrases = ["I hope so.", "We\'ll see.", "Suppose."]
		self.record_phrases 	= ["I'll record this.", "Writing your nonsence. Nevermind.", "Such pathetic. Pathetic enough to record that."]
		self.doubt_phrases		= ["I don't really beleive you.", "This is not a joke.", "That was really weak self-reflection, you know.", "I'm not so sure about that."]
		self.abort_phrases 		= ["You missed your opportunity to confess.", "It's over. I'll not wait forever.", "I'm bored of waiting.", "I'm not your assistant. Do it yourself."]
		self.sent_message = ""
		super().__init__(*args)
		# TODO mpve into linguistics
		

	def dispatch(self, request):
		#print("Dispatching ", request)

		if "no responce" in request.lower():
			abort_chance = random.randint(1,101)
			if abort_chance < 65:
				return json.dumps({"type":"info", "message": random.choice(self.wait_phrases)})
			else:
				return json.dumps({"type":"done", "message": random.choice(self.abort_phrases)})
		#if "ok" in request.lower():
		#TODO Log responce
		not_so_sure_chance  =  random.randint(1,101)
		record_chance 	    =  random.randint(1,101)
		if not_so_sure_chance > 80:
			return json.dumps({"type":"info", "message": random.choice(self.doubt_phrases)})
		else:
			if record_chance  > 75:
				return json.dumps({"type":"done", "message": random.choice(self.resolution_phrases)})
			else:
				# TODO refactor
				record_id     = get_last_record_id("/mnt/X/WORKSHOP/Violla/Clusters/Operator/log.csv")
				log_responce("/mnt/X/WORKSHOP/Violla/Clusters/Operator/log.csv", record_id, entry_a=self.sent_message, entry_b=request, b_required=True)
				return json.dumps({"type":"done", "message": random.choice(self.record_phrases)})

			
		# TODO define as sort of constant

		#print("Child method called")
		#return json.dumps({"type":"info", "message": "I do't wanna hear a thing."})

	#TODO Make testing utilities more adequate
	def payload(self):
		#TODO Move it to some method
		wake_limit = 240
		while True:
			#sleep_frame = random.randint()
			#TODO define it from config
			#time.sleep(random.randint(180,300))
			time.sleep(random.randint(180,240))
			chance = random.randint(1,101)
			#TODO rewrite
			if chance <= 90:
				continue
			phrase = ""
			if chance >= 93:
				phrase = random.choice(self.random_phrases)
			elif chance >=96:
				phrase = random.choice(self.random_curses)
			else:
				phrase = "".join(random.sample(self.random_glyphs,random.randint(4,8)))

			self.sent_message = phrase
			yield json.dumps({"type":"info", "message": phrase})




if __name__ == '__main__':

	#TODO - find a better way to send description to module
	if TEST:
		_id, violla_port , variation = TEST_CLUSTER_ID, TEST_VIOLLA_PORT, TEST_CLUSTER_CONFIG
	else:
		_id, violla_port, variation = sys.argv[1:4]
	#_id, port, path_to_configuration, variation = sys.argv[1:5]
	cluster = Cluster(_id, int(violla_port), variation)
	cluster.act()
