import os
from pathlib import Path
from collections import namedtuple
import json

idea_reflection = namedtuple('IdeaReflection', 'setup path keywords type')
setup 			= namedtuple('Setup',		   'variations')
variation  		= namedtuple('Variation',      'sub_name params_list')



class IdeasCloud():
	def __init__(self, clusters_folder):

		self.clusters_folder = clusters_folder
		self.known_ideas 	 = {}

	def parse_base_idea(self, idea):
		idea = json.load(idea)
		return idea["name"], idea["keywords"], idea["type"]


	def parse_variations(self, variations):
		#print("Not error")
		variations = json.load(variations)
		
		variants   = [variation(_["sub_name"],_["params"]) for _ in variations["variations"]]
		return variants



	def uncover_idea(self, path):
		curr_dir = os.getcwd()
		os.chdir(path)

		# TODO change tuple return to something else
		base_name, base_keywords, base_type = self.parse_base_idea(open("config.json"))
		#print(base)
		variations = self.parse_variations(open("ideas.json"))
		
		os.chdir(curr_dir)
		uncovered = (base_name, idea_reflection(setup(variations), path, base_keywords, base_type))
		print(uncovered)
		return uncovered

	def get_idea(self, name):
		if name in self.known_ideas:
			return self.known_ideas[name]
		else:
			return None


	def reflect_ideas(self):
		reflected = {}
		
		for _r, _d, _f in os.walk(self.clusters_folder):
			try:
				#TODO fix duplicate traversal
				#for d in _d maybe
				#TODO alter to generator expression
				for f in _f:
					if Path(f).suffix == ".cluster":
						uncovered = self.uncover_idea(_r)
						#print(uncovered)
						reflected[uncovered[0]]=uncovered[1]
			except Exception as e:
				print(e)
				continue
		#print(reflected)
		self.known_ideas.update(reflected)

	def present_ideas(self):
		print("Ideas cloud present_ideas working?")
		#print([_ for _ in self.known_ideas])
		known_ideas = "\n"+"\n".join([_ for _ in self.known_ideas])
		#print(known_ideas)
		return known_ideas#"\n".join([_ for _ in self.known_ideas])

	def present_variations(self, idea):
		return "\n".join([_.sub_name for _ in self.known_ideas[idea].setup.variations])