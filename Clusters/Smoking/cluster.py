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

		self.count = 0

		self.offer_phrases = ["You can smoke. You waited... Enough, i guess. Will you?",
								"Smoke. Go for it... Ready?",
								"It's a legite cigarette offer. Btw sounds really wierd. Are you up for it?"
								]

		self.wait_phrases = ["You\'d better answer, or wait till next time.",
							 "How long should i wait. I'll close this.",
							 "You either answering me or not. If not i'll count is as refuse.",
							 "I\'ll not wait forever. Time is ticking."]

		self.accept_phrases = ["Go for it. Do it. Do whatever you want.",
								"Does this really makes you whole?",
								"Were you waiting for it? So go for it.",
								"Cursed.",
								"You can't even handle such a thing. So ehat are you capable of? Nothing?",
								"Do you remember Belwest? Do you really remember or just pretend?"]


		self.reject_phrases = ["You stand this time. Could you stand another?.",
								"And why? Do you really beleive you could quit? We'll see.",
								"One more round of suffering? I found it interesting to inspect.",
								"It's some progress. Indeed.",
								"But don't even try to lie to me."]

		self.record_phrases 	= ["Interesting...",
									"I hope my notes will help you. Or not. I don't really mind.",
									"Such pathetic. Pathetic enough to record that."]

		self.doubt_phrases		= ["You're really make such a decission? Once again. You decide ...",
									"Sure about that? Your final decision is ...",
									"It's allowed, but could you deny such an offer? You set your mind to...",
									"Isn't it's pathetic to deal with this like that? Anyway. I wanna hear it once again."]

		self.abort_phrases 		= ["I will no wait. So you know the rules.",
									"Better luck next time.",
									"Forget about it.",
									"You know, you'll hate yourself if you'll broke this rule.",
									"I hope you'll suffer from abstinention."]
		self.sent_message = ""
		super().__init__(*args)
		# TODO mpve into linguistics
		

	def dispatch(self, request):
		#print("Dispatching ", request)

		if "no responce" in request.lower():
			abort_chance = random.randint(1,101)
			if abort_chance < 70:
				return json.dumps({"type":"info", "message": random.choice(self.wait_phrases)})
			else:
				return json.dumps({"type":"done", "message": random.choice(self.abort_phrases)})


		#if "ok" in request.lower():
		#TODO Log responce

		is_accepted = True

		if "yes" in request.lower():
			is_accepted = True

		if "no" in request.lower():
			is_accepted = False

		if "yes" not in request.lower() and "no" not in request.lower():
			return json.dumps({"type":"info", "message": random.choice(self.wait_phrases)})


		not_so_sure_chance  =  random.randint(1,101)
		print(not_so_sure_chance)
		if not_so_sure_chance > 80:
			return json.dumps({"type":"info", "message": random.choice(self.doubt_phrases)})
		else:
			if is_accepted:
				self.count+=1
				return json.dumps({"type":"done", "message": random.choice(self.accept_phrases) + f" Anyway it's number {self.count} since uptime."})
			else:
				return json.dumps({"type":"done", "message": random.choice(self.reject_phrases) + f" Anyway we hold at {self.count} since uptime."})



	def payload(self):
		while True:

			time.sleep(random.randint(5500,6500))

			phrase = random.choice(self.offer_phrases)

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
