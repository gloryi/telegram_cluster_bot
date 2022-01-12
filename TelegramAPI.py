from API import *
import telegram
import time

#TODO Set target API from config

class TelagramBotWrapper(API_Wrapper):
	def __init__(self, *args, **kwards):
		#get token from config file
		self.bot = telegram.Bot(token=TOKEN)
		self.registred_users = {}
		self.update_users_list()
		self.processed_ids = set()
		#TODO this is terrible HARDCODE
		self.init = True

	def init_known_users(self, file_path = "known_users.csv"):
		known_users_set = {}
		with open(file_path, 'r') as users_list:
			for line in users_list:
				_user_name , _user_id = line.split(",")
				known_users_set[int(_user_id)] = _user_name
		return known_users_set

	def add_new_user(self, new_user_name, new_user_id, file_path="known_users.csv"):
		with open(file_path, 'a') as users_list:
			users_list.write(f"{new_user_name},{new_user_id}\n")

	def check_last_update(self):

		updates = self.bot.get_updates()
		if(len(updates)>0):

			l_u = updates[-1]
			request_text = l_u['message']['text']
			request_id = l_u['message']['message_id']
			if self.init:
				self.init = False
				self.processed_ids.add(request_id)
				return ""

			if request_id not in self.processed_ids:
				#TODO STORE THIS DATA LOCALLY
				self.processed_ids.add(request_id)
				return request_text
		return ""


	def update_users_list(self):
		self.registred_users = self.init_known_users()
		#HARDCODE - terrible
		return

		updates = self.bot.get_updates()

		users_blacklist = set()

		for i, u in enumerate(updates):
			chat_data = u['message']['chat']
			username = chat_data['username']
			user_id  = chat_data['id']
			if user_id not in self.registred_users and ALLOW_NEW_USERS:
				self.registred_users[user_id] = username
				self.add_new_user(username, user_id)
			#Remember wther user were blacklisted. If so - probably responce once
			elif user_id not in self.registred_users:
				users_blacklist.add(user_id)
				
		for blacklisted_user_id in users_blacklist:
			self.bot.send_message(text=f'Access denied', chat_id = blacklisted_user_id)

		del users_blacklist

		for user_id in self.registred_users:
			username = self.registred_users[user_id]
			self.bot.send_message(text=f'Initialized for {username}.', chat_id = user_id)

	def send_update(self, update_message):
		for user_id in self.registred_users:
			username = self.registred_users[user_id]
			self.bot.send_message(text=update_message, chat_id = user_id)
