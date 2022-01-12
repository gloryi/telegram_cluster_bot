#from clusters import cluster_deducer
#TODO from API import api
#TODO move all imports to some other place
#from ConsoleAPI 	 import *
from TelegramAPI	 import *
import Core.LinguisticsBase
from Core.LinguisticsBase import Semantics
import time
import subprocess
import os
from ViollaRoutines import MindState
from ViollaRoutines import MindReflection
from ViollaRoutines import Mood       as _M
from ViollaRoutines import Phrase     as _P
from ViollaRoutines import Topics 	  as _T
from ViollaRoutines import PATH_TO_PLANNER, PATH_TO_CLUSTERS
from ViollaRoutines import CORE_CLUSTERS
from ViollaRoutines import DEDUCTION
from ViollaRoutines import INTUITION
#TODO rewrite all "import *"
from Core.ClusterController import *
#TODO Move to ViollaRoutines
import threading
import json
from Core.Planner import *
import random


#for multi users launch another copy of violla
#or multi copies of general processing threads
#with separation for users inside of clusters
#or just multiple versions of clusters





class Violla():
	def __init__(self):
		#TODO move it to some other place
		self.last_heard 	 = ""
		self.mindState 		 = MindState.Idle
		self.mood 			 = _M.Cold
		#TODO MAKE API CALLS ABSTRACT
		self.interface 		 = TelagramBotWrapper()
		#self.interface       = CLIBotWrapper()
		self.semantics       = Semantics()
		self.deduction 		 = DEDUCTION
		self.intuition		 = INTUITION

		# TODO Fix This later
		self.patience 		 = random.randint(100,250)

		self.assemble_core()
		#self.planner 		 = Planner()
		#self.planner_cluster = None
		#self.start_planning()

		#launch acting client-like and server like threads
		self.say(_T.Awake)
		

		#TODO Launch Planner cluster

	# TODO Make all parts of Violla clusters // modules which could be easylly be
	# loaded and unloaded
	def assemble_core(self):
		for core_cluster in CORE_CLUSTERS:
			self.intuition.register_cluster(core_cluster.description, link = core_cluster.Cluster)

	# TODO all Violla methods should be void like
	# No returns
	# So no recursion exception processing isuses
	def confidence(f, *args, **kwards):
		def confident_action(self, *args, **kwards):
			try:
				return f(self, *args, **kwards)
			except Exception as e:
				#print(repr(e))
				self.say(message=str(e))
				self.say(topic=_T.Error)
		return confident_action


	#TODO probably delete
	#@confidence
	#def start_planning(self):
		#TODO - probably move to some other place. But planner cluster is special to Violla
		#And it's supposed to be always up
		#Launchlib maybe
	#	self.say(message=PATH_TO_PLANNER)
	#	self.say(message=PATH_TO_CLUSTERS)
	#	p = subprocess.Popen(["python3", PATH_TO_PLANNER+"/cluster.py", PATH_TO_CLUSTERS])
		#TODO description to launch params maybe
		#TODO keywords from linguistsics base
		#or all of above from planner params
	#	planner_description = open(os.path.join(PATH_TO_PLANNER,"description.json"))
	#	planner_description = json.load(planner_description)
	#	self.deduction.register_cluster(planner_description)

		

	@confidence
	def think(self, topic, message):
		return self.semantics(topic, message, self.mood)


	@confidence
	#TODO Synchronisation
	# ONLY BYSY//IDLE
	# TODO process security
	def setMind(self, mind_state):
		self.mindState = mind_state
		return MindReflection.DoingThis
		#if self.mindState != MindState.Idle:
		#	return MindReflection.Busy
		#else:
		#	self.mindState = mind_state
		#	return MindReflection.DoingThis

	@confidence
	def say(self, topic=None, message=None, think_loudly=False):
		# TODO rewrite
		if(think_loudly):
			if(random.randint(1,100000)>99985):
				self.interface.send_update(self.think(topic, message))
		else:
			self.interface.send_update(self.think(topic, message))


	@confidence
	def listen(self):
		#TODO - better parsing. Return class instead of just string.
		#TODO - rewrite from altered ClusterController
		new_request = self.interface.check_last_update()
		if new_request:
			return new_request

	
	def listening(self):
		while True:
			heared = self.listen()
			if heared:
				yield heared
			time.sleep(1)
			
	@confidence
	def act(self):
		internal_motive_flow = threading.Thread(target = self.internal_motive)
		external_motive_flow = threading.Thread(target = self.external_motive)

		internal_motive_flow.start()
		external_motive_flow.start()

		internal_motive_flow.join()
		external_motive_flow.join()


	def select_motives(self, idea_type):
		# TODO refactor on namings "idea//motive//etc"
		return self.intuition.focus(idea_type) + self.deduction.focus(idea_type)

	@confidence
	def process_active_motive(self, motive):
		# TODO probably replace with async approach
		# TODO switch to constant reflection with timer updates
		# TODO with patience
		#while True:
		# TODO patience and motives reentrance processing
		if motive.direction == IDEA_DIRECTION.REFLECT:
			print("Asking cluster for some responce on " + motive.inner_memory)
			#TODO wrap everything
			motive.inner_memory = motive.cluster.link.actor.send(motive.inner_memory)
			next(motive.cluster.link.actor)
			motive.direction = IDEA_DIRECTION.COVER
			# TODO more explicit way to clear buffer and change motive state
			#motive.inner_memory = ""

		elif motive.direction == IDEA_DIRECTION.COVER:
			# TODO dispatch motive responce
			# it could be done
			# or ask for some additional data
			# or just idle ???
			# TODO linguistics
			# print("Probably place of exception 1")
			# print(motive.cluster.link.actor)
			# motive_reflection = next(motive.cluster.link.actor)
			# print(motive_reflection)
			# if not motive_reflection:
			# 	motive_reflection = next(motive.cluster.link.actor)
			# print("Probably place of exception 2")
			# print(motive_reflection)
			# motive.inner_memory = motive_reflection
			# print(motive.inner_memory)

			# print("Probably place of exception 3")
			# TODO check on "Done"
			# if not done - rise up this question
			# TODO make namedtuple
			if motive.inner_memory:
				data = json.loads(motive.inner_memory)
				if(data["type"]!="done"):
					self.say(message = random.choice(["Listen. ", "Let me see. ", "So... ", "Well. ", "You know... ", "Hey. ", "Be focused. "]) + data["message"])
					motive.inner_memory = ""
				else:
					self.say(message = data["message"])
					self.setMind(MindState.Idle)
					#TODO wrap everything
					motive.cluster.controller.close(motive)

			else:
				if self.last_heard:
					motive.direction    = IDEA_DIRECTION.REFLECT
					motive.inner_memory = self.last_heard
					self.last_heard = ""
				else:
					self.patience-=1
					# TODO Patience
					# TODO Linguistics
					# ESCALATE MODULE LOGICS BY HERSELF
					#self.say(message = "I'm waiting...", think_loudly=True)
					# On done switch to IDLE
					#if not done
					# TODO start patience mechanism
					if self.patience    == 0:
						self.patience   = random.randint(100,250)
						self.last_heard = "No responce"



	# TODO internal motive is processing itself
	# TODO add sort of events instead of time.sleep
	# TODO Move it to some module. i.e. refactor
	# TODO new become selected if there are no too much of selected
	# TODO selected with most priority become actuall
	# TODO work with actuall untill "Done"
	@confidence
	def internal_motive(self):
		while True:
			time.sleep(1)
			# TODO complete state machine
			# focus on intuition
			# focus on deduction
			# psocess active
			# if no active process selected
			# if no selected process new
			# if no new process delayed
			# if no delayed proces denied
			# TODO merge deduction and intuition
			active_motives = self.select_motives(IDEA_TYPE.ACTIVE)
			if not active_motives:
			# TODO to linguistics
			# or more like sort of self-reflection core cluster
				self.say(message="So... we're up for nothing.", think_loudly=True)
			elif len(active_motives)>1:
				raise Exception("Somehow now i'm on multiple tasks. This is definitely not ok.")
			else:
				# TODO write a config or some logics to control number of such a messages
				self.say(message="I'm up for something.", think_loudly=True)
				self.process_active_motive(active_motives[0])
				continue

			# TODO Condition for changing idea type



			selected_motives = self.select_motives(IDEA_TYPE.SELECTED)

			if not selected_motives:
				self.say(message="I have no plans...", think_loudly=True)
			else:
				for motive in selected_motives:
					#TODO select the most actual one
					#TODO all into linguistics
					self.say(message=random.choice(["About... ", "Speaking of. ", "And. "]) + idea.cluster.name, think_loudly=True)

					self_reflection = self.setMind(MindState.Busy)
					if(self_reflection == MindReflection.DoingThis):
						motive.idea_type = IDEA_TYPE.ACTIVE
					
					#TODO correct cycle processing
				continue

			new_motives = self.select_motives(IDEA_TYPE.NEW)

			if not new_motives:
				self.say(message="No intentions...", think_loudly=True)
			else:
				self.say(message="All i have now is just some intentions...", think_loudly=True)
				for idea in new_motives:
					# TODO check if it's still actuall
					# TODO select only valid ones
					#self.say(message="So... " + idea.cluster.name + "...")#\n" + "We're stopped when you said \"" + idea.inner_memory + "\".")
					idea.idea_type = IDEA_TYPE.SELECTED
				continue

			denied_motives = self.select_motives(IDEA_TYPE.DENIED)

			if not denied_motives:
				self.say(message="I'm open to just any activities...", think_loudly=True)

			delayed_motives = self.select_motives(IDEA_TYPE.DELAYED)

			if not delayed_motives:
				self.say(message="I tracked... Well... Nothing.", think_loudly=True)



			#time.sleep(10)
			#TODO update with altered cluster controller
		#	...
			#self.deduction.check()

		#run in thread
		#act like server

	# TODO Horisontal refactoring



	@confidence
	def deduce(self, request):
		# TODO move to violla routines
		cluster_reflection = None
		cluster_reflection = self.intuition(request)
		#print(cluster_reflection)
		if not cluster_reflection:
			cluster_reflection = self.deduction(request)
			#print(cluster_reflection)
			if not cluster_reflection:
				print("Method just returning None type object")
				return None
		#TODO - make it confident
		#raise Exception("I don't know what this is supposed to mean.")
		return cluster_reflection


	# TODO it's not processing
	# just registration of external events -> search for cluster -> register it's as idea
	def external_motive(self):
		for request in self.listening():
			print("*"+request)

			# TODO detect wether it's related to some other cluster
			if self.mindState == MindState.Busy:
				self.last_heard = request
				continue


			#TODO wrap try -> catch -> blame into
			#class with context manager
			#with target function as a parameter
			#TODO change this if to something else
			#maybe use telegram "/" sentinel in some form
			deduction = self.deduce(request)
			# It could be unknown cluster -> send error
			# Or ask processor wether such cluster exists
			# ...
			# It could be known cluster
			# but not idea
			# wrap to idea ...
			# wait
			# ...
			# It could be idea
			# ...
			# active   -> send request for it
			# delayed  -> decide what to do
			# denied   -> ignore
			# new 	   -> if there is no active ideas - make it active

			# TODO if there are an active idea
			# interpret this as message for idea
			# and not as invocation of a new idea

			if not deduction:
				# TODO into linguistics
				self.say(message="I don't know what this is supposed to mean.")
				#raise Exception("I don't know what this is supposed to mean.")
				#TODO fix this
				#time.sleep(1)
				# TODO Raise as exception
				#print("Unknown phrase. It's neither idea nor cluster")
				continue

			if deduction.type == DEDUCTION_TYPE.CLUSTER:
				print("Cluster")
				deduction.object.register_as_idea(idea_type=IDEA_TYPE.NEW, idea_direction=IDEA_DIRECTION.REFLECT, inner_memory = request)
			if deduction.type == DEDUCTION_TYPE.IDEA:
				print(deduction.object.idea_type)
				print("Idea")
				# TODO raise exception - cause it's already an idea
				# Sort of "i know"
				# TODO And that's it
				# External motive should not trigger immediately
				# TODO just somehow "freeze" initial message in idea
				# TODO check wether it's right moment
				# Register as idea and process immediately
				# Register as idea and set status of delayed
				# Or register as idea and set status of denied
				# Controller will clean it later
				# TODO Check for duplicates or whatever
				# TODO Probably not wery correct eay to handle this
				# HARDCODE just for now it's active status
				#cluster.register_as_idea()

			#else:
			#	print("Cluster not found")
			



			...
		#run in thread
		#act client like



if __name__ == '__main__':
	v = Violla()
	v.act()
