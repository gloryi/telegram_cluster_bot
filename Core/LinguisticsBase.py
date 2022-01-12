from collections import defaultdict
from ViollaRoutines import Mood       as _M
from ViollaRoutines import Phrase     as _P
from ViollaRoutines import Topics 	  as _T
import random


#TODO Make phrases mutable. Define class/template/tree
#TODO Define dict keys somewhere else
#TODO Updates Linguistics routine from launched clusters
#TODO Move default phrases list somewhere else
#TODO all phrases lst must contain exactly one "undefined" phrase /// check on add
#TODO Make it all really very abstract to have an ability to push this all to git

known_phrases = defaultdict(list)
known_phrases[_T.Awake] 	= [_P(_M.Undefined, "Hi."),
						   _P(_M.Neutral,   "I\'m up."),
						   _P(_M.Neutral,   "I'm here."),
						   _P(_M.Neutral,   "Morning... Probably..."),
						   _P(_M.Neutral,   "オカリ."),
						   _P(_M.Neutral,   "It's been quite a time."),
						   _P(_M.Cold,	    "Well..."),
						   _P(_M.Cold,      "..."),
						   _P(_M.Angry,	    "Did you really just disabled me?")
						   ]

known_phrases[_T.InTheMiddle] = [_P(_M.Undefined,  "Hold on."),
						   		 _P(_M.Neutral,    "We are still not resolved something."),
						   		 _P(_M.Neutral,    "Don't switch ishue just like that."),
						   		 _P(_M.Neutral,    "Answer first."),
						   		 _P(_M.Cold,	   "That's not how the things are doing."),
						   		 _P(_M.Cold,       "I'm waiting..."),
						   		 _P(_M.Cold,       "You are wasting my time..."),
						   		 _P(_M.Angry,	   "That's why you are in such a situation. Yes. Exactly because of acting like that.")
						   		]
known_phrases[_T.Error] = [_P(_M.Undefined, "Some go wrong... I see."),
						   _P(_M.Neutral,   "There is somethng not quite right. Fix this later."),
						   _P(_M.Neutral,   "That's ... some error. Just do something with that, ok?."),
						   _P(_M.Cold, "This is ... error. You know, you are not so good coder after all."),
						   _P(_M.Cold, "Fix. This. Now. I'm loosing my patience."),
						   _P(_M.Angry, "The fuck you were doing if threre are still errors.")
						   ]



class Semantics():
	def __init__(self):
		pass

	#TODO Maybe exceptions is not best option there are
	#TODO Refactor a little bit
	def validate_data(self, topic, message, mood):
		if (topic and topic not in known_phrases) or (topic == None and message == None):
			raise Exception('I don\'t really know what to say... Maybe you should, well... Fix a little bit Linguistics cluster.')

	def compile(self, message):
		if message.__class__ == _P:
			return message.phrase
		if message.__class__ == str:
			return message
		#TODO if message is phrase pattern - assemble

	def form_phrase(self, topic, message, mood):
		self.validate_data(topic, message, mood)

		if topic and not message:
			target_phrases = list(filter(lambda _ : _.mood == mood, known_phrases[topic]))
			if target_phrases:
				message = random.choice(target_phrases)
			else:
				return self.form_phrase(topic, message, _M.Undefined)

		#TODO Probably just remove cause it makes no sense
		if message and not topic:
			message = message

		return self.compile(message)



		

	def __call__(self, topic, message, mood = _M.Neutral):
		return self.form_phrase(topic, message, mood)
		



