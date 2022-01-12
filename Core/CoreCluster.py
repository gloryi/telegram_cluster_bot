import json

#TODO claridy this
#Behavioural logic
#But a fundamental one
class CoreCluster():
	def __init__(self, _id, path_to_configuration):
		self._id                = _id
		self.payload_module     =  None
		#self.actor = self.act()
		#self.set_logics(path_to_configuration)

	def set_logics(self, path_to_configuration):
		#TODO define wether it's really needed for core cluster
		raise NotImplementedError

	def act(self):
		#TODO force realizations to define this as
		#coroutine
		raise NotImplementedError
		#while True:
		#	to_process = yield
		#	process_result = self.payload_module.process(to_process)
		#	yield process_result

	# TODO path to dispatching scheme
	def dispatch(self, request):
		#TODO make it abstract ->> force to write realization
		raise NotImplementedError

	def null_action(self, *args):
		# TODO move to linguistics
		# TODO define all messages by constants of module semantics
		# and send Violla only keys
		return json.dumps({"type":"info", "message":"Sometimes it's so hard to understand you..."})
