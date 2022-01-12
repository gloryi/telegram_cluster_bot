from Core.CoreCluster import *
from Core.Plannerlib import *
import subprocess
		

#TODO make some sence in inheritance
class Planner(CoreCluster):
	# TODO make something with dependency of cluster_controller
	def __init__(self, cluster_controller, *args):
		super().__init__(*args)
		#TODO delegate VIOLLA say what dir is clusters dir
		#HARDCODE it's 0:21 ~ i'll accept such a hardcode for now
		self.cloud = IdeasCloud("/mnt/X/WORKSHOP/Violla/Clusters")
		self.cloud.reflect_ideas()
		# TODO Figure out wether planner should know something about intuition
		# TODO Figure out who should store launched process id
		self.cluster_controller = cluster_controller
		self.actor = self.act()
		self.running = {}

		# TODO Default launch list
		#self.start_process("Boring")
		#self.start_process("Echo")

		#self.actor.send(None)
		next(self.actor)

	def form_description(self, name, cluster_info, _port, _id):
		# TODO generate base dict in plannerlib and .update it with port, etc
		description = {}
		description["id"]	    = _id
		description["name"]     = name
		description["keywords"] = cluster_info.keywords
		description["port"] 	= _port
		description["type"]		= cluster_info.type
		return description


	def start_process(self, process_name):

		cluster = self.cloud.get_idea(process_name)

		if not cluster:
			return "If you want to work with " + process_name + " than write it. I don't know such cluster."

		path = cluster.path
		#HARDCODE
		#id, port, variation for now is just hardcodes
		# TODO set id and port from registrator and free ports pool
		# TODO distinguish between internal and external processes

		port = self.cluster_controller.give_port()
		_id  = self.cluster_controller.give_id()

		p = subprocess.Popen(["python3", path+"/cluster.py", str(_id), str(port), "default"])
		# TODO set as a sort of a description
		# TODO register launched process in cluster_controller
		self.running[process_name] = p

		self.cluster_controller.register_cluster(self.form_description(process_name, cluster, port, _id))
#
		#{"id":0, "name":"Planning", "keywords": ["Start", "What are you up for", "Think of", "Are you using", "Can you work with"]}


		return "Launched. Probably. Check that out."
		# TODO start
		# TODO set port
		# TODO generate description
		# TODO register in controller
		# TODO return done

	# TODO leave dispatch up to base class
	# Initialize with dispatcher instance
	def dispatch(self, request):
		#TODO add dispathing scheme
		#TODO unstrict string comparisons
		#TODO actually dispatch should be in some sort of config
		#together withmodule linguistics
		#"Think of", "Are you using", "Can you work with"
		print("Dispatching ", request)
		if "What are you up for" in request:
			#print("Getting ideas list")
			message = self.present_ideas()
			#TODO clarify protocol
			return json.dumps({"type":"info", "message":message})


		if "What are you thinking about" in request:
			message = self.list_clusters()
			print(message)
			return json.dumps({"type":"info", "message":message})


		if "start" in request.lower():
			# TODO set normal parsing scheme
			# Probably command objective should be json "objective" field
			cluster_to_start = request.split(" ")[-1]

			result = self.start_process(cluster_to_start)

			return json.dumps({"type":"info", "message":f"{result}."})

		if "no responce" in request.lower():
			return json.dumps({"type":"info", "message":f"I think that we were planning rigt now. If you're done just say taht."})



		if "close" in request.lower():
			return json.dumps({"type":"info", "message":"Just write some more of your code if you wnat to stop clusters."})
		if "ok" in request.lower():
			return json.dumps({"type":"done","message":"Whatever."})
		return self.null_action()

	# TODO patience? Probably not in Core
	# TODO leave act up for base class
	# Initialize with actor
	def act(self):
		while True:
			request = yield
			print("received " + request)
			# TODO make things like this more abstract
			# at least like realization in linguistics
			# TODO now it's just plain string return
			processed = self.dispatch(request)
			#print("returning\n"+ processed)
			yield processed
		#return "What?"

	def present_ideas(self, *args):
		print("Method called")
		self.cloud.reflect_ideas()
		return self.cloud.present_ideas()

	def present_variations(self, idea, *args):
		return self.cloud.present_variations(idea)

	def list_clusters(self):
		clusters = []
		#for cnt in self.cluster_controllers:
		clusters += self.cluster_controller.introspect_clusters()
		return ", ".join(clusters)