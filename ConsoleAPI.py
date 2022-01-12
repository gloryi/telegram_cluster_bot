from API import *
#import telegram

#TODO Set target API from config
import asyncio
from aioconsole import ainput, aprint
import aconsole
import threading
import time


class bcolors:
    HEADER    = '\033[95m'
    OKBLUE    = '\033[94m'
    OKCYAN    = '\033[96m'
    OKGREEN   = '\033[92m'
    WARNING   = '\033[93m'
    FAIL      = '\033[91m'
    ENDC      = '\033[0m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'

class CLIBotWrapper(API_Wrapper):
	def __init__(self, *args, **kwards):
		self.received_messages = []
		self.messages_to_send = []

		self.console_t = threading.Thread(target=self.async_console_prcessor)
		self.console_t.start()


	def check_last_update(self):
		if self.received_messages:
			return self.received_messages.pop()
		return ""

	def send_update(self, update_message):
		print(bcolors.OKGREEN + update_message + bcolors.ENDC)
		self.messages_to_send.append(update_message)


	async def check_updates(self):
		while True:
			console_phrase =  await ainput('')
			self.received_messages.append(console_phrase)

	async def send_updates(self):
		while True:
			if not self.messages_to_send:
				time.sleep(2)
				continue
			await aprint(bcolors.OKGREEN + self.messages_to_send.pop() + bcolors.ENDC)

	def async_console_prcessor(self):
		loop = asyncio.new_event_loop()
		asyncio.set_event_loop(loop)
		loop.create_task(self.check_updates())

		loop.run_forever()
