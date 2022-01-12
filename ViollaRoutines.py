from collections import namedtuple
import os
from Core.Planner import *
from Core.ClusterController import *

ALLOW_NEW_USERS  = False
TOKEN 			 = "TELEGRAM_TOKEN"
PATH_TO_CLUSTERS = os.path.join(os.getcwd(), "Clusters")
PATH_TO_PLANNER  = os.path.join(PATH_TO_CLUSTERS, "Planner")



#Maybe add some more
class MindState():
	Idle 	    = "IDLE"
	Busy		= "BUSY"
	# TODO Probably already not actual
	Responding  = "RESPONDING"
	Speaking 	= "TALKING"

class MindReflection():
	Busy 		 = "Busy"
	DoingThis 	 = "DoingThis"
	NotDoingThis = "NotDoingThis"


class Mood():
	Neutral    = "Neutral"
	Angry      = "Cynic"
	Cold 	   = "Cold"
	Blaming    = "Blaming"
	Supportive = "Supportive"
	Undefined  = "Undefined"

Phrase = namedtuple("Phrase", "mood phrase")


class Topics():
	Awake 		= "Awake"
	InTheMiddle = "InTheMiddleOfSomething"
	Error 		= "Exception"

#TODO Move all of above into core clusters
#TODO Make linguistics core cluster
#TODO Make Mood core cluster
#TODO Make Mind reflection core cluster
#TODO Make Mind State core cluster
#TODO Violla routines should be removed and integrated into core clusters somehow

CoreCluster = namedtuple("CoreCluster", "Cluster description")

# TODO even worse dependencies
DEDUCTION = ClusterController()
INTUITION = ClusterController()

CORE_CLUSTERS = []

#HARDCODE
#TODO get from core cluster config somehow
CORE_CLUSTERS.append(CoreCluster(Planner(DEDUCTION, 0, "/mnt/X/WORKSHOP/Violla/Core/Planner.json"),
	{"id":0, "name":"Planning", "keywords": ["Start", "What are you up for", "Think of", "Are you using", "Can you work with"]}))