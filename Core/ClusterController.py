from Core.ClustersBridge import *
from datetime import datetime
import threading
import time
# TODO move it to ViollaRoutines
from collections import namedtuple
import socket

# TODO move it to Violla routines
# Write decission making model
# As core cluster

# TODO move it to Violla routines
class DEDUCTION_TYPE():
	IDEA    = "IDEA"
	CLUSTER = "CLUSTER"

# Reflect if message to sent was inward
# Cover if message to sent was outward
class IDEA_DIRECTION():
	REFLECT = "REFLECT"
	COVER   = "COVER"

deduction = namedtuple('Deduction', 'type object')

class IDEA_TYPE():
	# TODO figure out why there is selected
	# and active
	# maybe there are could be multiple selected
	# and only one active
	SELECTED = 'SELECTED'
	ACTIVE   = 'ACTIVE'
	NEW      = 'NEW'
	DELAYED  = 'DELAYED'
	DENIED   = 'DENIED'

class idea():
	def __init__(self, cluster, idea_type, idea_direction, inner_memory):
		self.cluster 	  = cluster
		self.date 		  = datetime.now()
		self.idea_type    = idea_type
		self.direction    = idea_direction
		self.inner_memory = inner_memory



class ClusterController():
	def __init__(self):
		self.clusters 	   = []
		self.ideas_queue   = []
		# TODO delegate it's to Violla
		self.active_idea   = None
		self.perception_t  = threading.Thread(target = self.accumulate_ideas)
		self.perception_t.start()
		self.avaliable_ports = [_ for _ in range(2048, 65535)]
		self.last_provided_id = 18 # TODO - change this magic number to something else

		
	def parse_description(self, description, link=None):
		bridge = ClusterDescription()
		#print("not error")
		#print(description.__class__)
		if "port" in description:
			bridge.port = description["port"]
			# TODO generate socket processing function
			# TODO and set it as link
			# TODO fix hardcode
			bridge.set_callback(self.register_idea_callback)
			bridge.set_link(_type=description["type"])
			#if description["type"] == "External":
			#	bridge.set_link("External")
			#elif description["type"] == "Internal"
			#	bridge.set_link("")
			#else:
				# TODO void link, somehow telling that something is wrong
			#	bridge.set_link(...)
		else:
			#set core cluster generator func
			bridge.set_link(link=link)

		#print(bridge.port)
		#print(description)
		bridge.id   = description["id"]
		#print(bridge.id)
		#print("not error")
		for keyword in description["keywords"]:
			bridge.add_keyword(keyword)

		bridge.controller = self

		bridge.name = description["name"]

		return bridge

	# def parse_core(self, description):
	# 	bridge = CoreClusterDescription()
	# 	bridge.id   = description["id"]
	# 	for keyword in description["keywords"]:
	# 		bridge.add_keyword(keyword)
	# 	return bridge

	def give_id(self):
		self.last_provided_id +=1
		return self.last_provided_id


	def check_port(self, _port):
		port_is_free = False
		a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		location = ("127.0.0.1", _port)
		result_of_check = a_socket.connect_ex(location)

		if result_of_check != 0:
   			port_is_free = True

		a_socket.close()
		#time.sleep(2)

		return port_is_free

	# TODO better ports handling
	def give_port(self):
		while True:
			port = self.avaliable_ports.pop()
			if self.check_port(port):
				return port
		#return self.avaliable_ports.pop()

	def register_cluster(self, description, link = None):
		#TODO It's just json now. Change it later
		#self.clusters.append(description)
		bridge = self.parse_description(description, link)
		self.clusters.append(bridge)

	# def register_core_cluster(self, description):
	# 	bridge = self.parse_core(description)
	# 	self.core_clusters.append(bridge)

	# TODO Actually how to deuce it?
	def deduce_link(self, args):
		# return link
		...

	# TODO in thread - process active connections. Save in queue
	# Violla will ask from time to time for new incomes
	# TODO make it different for core and regular clusters
	def accumulate_ideas(self):
		while True:
			time.sleep(10)
			# set up TCP server
			# wait for connections
			# on connection wrap it to idea
			# with setup of connection link
			# TODO - regular processing
			
			#_l = self.deduce_link(...)
			#_i = idea(_l)
			#self.ideas_queue.append(_i)
			#...


	# So the protocol is:
	# Idea is generator like callable
	# On external - set up connection
	# Wait for message - call -> send to cluster
	#
	# On internal
	# Wait for approval or deny
	# Violla says about it and it's become external like
	#
	# On core
	# Act just like all of above
	# Except this is child objects of Violla
	# instead of independednt processes
	#
	# BTW core clusters processing are take place in
	# separate class instance


	#TODO post procrss ideas after Violla make some decissions
	def sort_ideas(self):
		ideas_queue_updated = []
		for idea in self.ideas_queue:
			if idea.idea_type == IDEA_TYPE.ACTIVE:
				self.active_idea = ideas
			else:
				ideas_queue_updated.append(idea)
		self.ideas_queue = ideas_queue_updated


	def focus(self, idea_type):
		return list(filter(lambda _: _.idea_type==idea_type, self.ideas_queue))


	# Actually internal cluster just internaly triggered
	# Next it act's like external cluster
	# So internal and external clusters processing are quite the same
	# Internal cluster just had to be properly initialized with connection
	# TODO tweak from idea direction
	def decide_on_ideas(self):
		for idea in self.ideas_queue:
			yield idea
			decision = yield
			#if decision == IDEA_TYPE.SELECTED:
			#	self.active_idea = idea
			#if decision == IDEA_TYPE.DENIED:

			idea.idea_type = yield
		#for idea in self.ideas_queue:

		#return self.ideas_queue


	# TODO made this valid processing method
	# For external and internally called for internal
	# with approval

	# TODO strictly for external
	# TODO maybe not only for them
	# TODO do something with parameters duplicates
	def register_idea(self, cluster, idea_type = IDEA_TYPE.NEW, idea_direction = IDEA_DIRECTION.REFLECT, inner_memory=""):
		print("cluster ", str(cluster.id), " registerd")
		_i = idea(cluster, idea_type, idea_direction, inner_memory)
		self.ideas_queue.append(_i)

	def register_idea_callback(self, cluster, idea_type = IDEA_TYPE.NEW, idea_direction = IDEA_DIRECTION.COVER, inner_memory = ""):
		print("cluster ", str(cluster.id), " registerd")
		_i = idea(cluster, idea_type, idea_direction, inner_memory)
		self.ideas_queue.append(_i)		


	def close(self, idea):
		self.ideas_queue.remove(idea)

	# TODO remove somehow
	#def thik_of(self, cluster, message):
	#	_i = idea(cluster)
		#...
		# set up connection with cluster
		# get it's procesing link
		# append link to ideas
		# mark as top priority idea
		#return cluster.link
		#...



	#TODO - Better deduction with inderect compare
	#TODO - refactor code
	def deduce_cluster(self, message):
		print(message)
		for _i in self.ideas_queue:
			for key in _i.cluster.keywords:
				if key in message:
					return deduction(DEDUCTION_TYPE.IDEA, _i)

		for _k in self.clusters:
			for key in _k.keywords:
				if key in message:
					return deduction(DEDUCTION_TYPE.CLUSTER, _k)
		print("returns just none")
		return None
		#TODO - mve it into Linguistic base module
		#actually deprecate all text message anywere except there are
		#raise Exception("I don't know what this is supposed to mean.")

	def introspect_clusters(self):
		cluster_names = [_k.name for _k in self.clusters]
		return cluster_names



	# def deduce_core(self, message):
	# 	#TODO obvious DRY violation
	# 	for k in self.core_clusters:
	# 		for key in k.keywords:
	# 			if key in message:
	# 				return k		

	def __call__(self, message):
		return self.deduce_cluster(message)
