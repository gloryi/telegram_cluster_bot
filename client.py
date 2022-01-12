from autobahn.twisted.websocket import WebSocketClientProtocol, \
	WebSocketClientFactory
import json
import random
import time
import yfinance as yf
import numpy as np
from datetime import timedelta
import pandas as pd
from talib import RSI
from collections import namedtuple
#import sys



#bad solution

TOKEN_NAME = "UNKNOWN"
KILL_RECEIVED = False

class Payload():
	def __init__(self):
		self.random_words_list = ["Fuck!"]
		pass

	def wait_for_event(self):
		#while True:
		time.sleep(15)
		message = random.choice(self.random_words_list)
		return message


#Actually state machine
#Indicator scheme should descibe
#states to be created and relations between them
class indicator_scheme():
	def __init__(self, name, scheme):
		pass

	def switch_state(self, conditions):
		pass
		#conditions like moving averages

		#send conditios to current state

		#it's up to state to decide
		#initiate state switch or not

		#and to what state if so




class indicator_state():
	def __init__(self, name, linked):
		self.name = name
		self.linked = linked





class MarketStateMachine():
	def __init__(self):
		self.unknown = "UNKNOWN"
		self.intra_ma = "INTRA"
		self.below_ma = "BELOW"
		self.above_ma = "ABOVE"

		self.suspicious = "SUSPICIOUS"
		self.usual 		= "USUAL"
		self.rising 	= "RISING"
		self.falling 	= "FALLING"

		self.current_state = self.unknown

	def are_new_state_signal(self, new_state):
		if  self.current_state == self.unknown:
			print("SET INITIAL STATE OF ", new_state)
			self.current_state = new_state
			return self.usual

		elif self.current_state == new_state:
			print("STATE DOES NOT CHANGED: ", new_state)
			if new_state == "INTRA":
				return self.suspicious
			else:
				return self.usual

		elif (self.current_state == "BELOW" and new_state == "INTRA") or (self.current_state == "ABOVE" and new_state == "INTRA"):
			print("STATE CHANGED TO INTRA_STATE", new_state)
			self.current_state = new_state
			return self.suspicious

		else:
			self.current_state = new_state
			if self.current_state == "BELOW":
				print("STATE CHANGED FROM INTRA TO BELOW - FALLING")
				return self.falling

			else:
				print("STATE CHANGED FROM INTRA TO ABOVE - RISING")
				return self.rising


class MarketProcessingPayload(Payload):
	def __init__(self, token):
		self.token = token
		self.state = MarketStateMachine()
		self.random_words_list = ["Raising", "Falling down", "Crashing"]

	def fetch_market_data(self):
		data = yf.download(tickers = self.token,period = "1d",interval = "1m")[['Close']]
		data = data.reset_index()
		data = data['Close'].tolist()
		#print(data)
		return data

	def get_knot_idx(self, averages):
		knots = []
		for higher_avg, lower_avg in zip(averages[:0:-1], averages[-2::-1]):
			knots.append(higher_avg.value/lower_avg.value)
		print("MA KNOTS = ", knots)
		max_knot = max(knots)

		return max_knot -1.0


	def do_some_ta(self, prices):
		CUR_PRICE_IDX = 0

		ma = lambda period: ma_metadata(sum(prices[- period:])/period, period)
		ma_metadata = namedtuple('ma_metadata', 'value index')
		current_price = prices[-1]
		indexes_of_interest = [30,50,100,200]
		averages = [ma(i) for i in indexes_of_interest]
		averages.append(ma_metadata(current_price, CUR_PRICE_IDX))


		layout = sorted(averages, key = lambda x: x.value)

		output_string = ""

		for l in layout:
			output_string += "\nMOVING AVERAGE[{}] = {} |".format(l.index, l.value)

		print(output_string)

		new_state = "UNKNOWN"
		print(layout[0].value)
		print(current_price)
		print(layout[0].value == current_price)
		if(layout[0].value == current_price):
			new_state = "BELOW"
			print("BELOW TRIGGER")

		elif(layout[-1].value == current_price):
			new_state = "ABOVE"
			print("ABOVE TRIGGGER")
		else:
			new_state = "INTRA"
			print("INTRA TRIGGER")

		signal_type = self.state.are_new_state_signal(new_state)

		knot_idx = self.get_knot_idx(averages)


		return signal_type, knot_idx

#TODO Refactor Completely

	def wait_for_event(self):
		message = ""
		time_for_next_update = 30
		while True:
			time.sleep(time_for_next_update)
			market_data = self.fetch_market_data()
			market_situation, knot_idx = self.do_some_ta(market_data)

			if market_situation == "USUAL":
				time_for_next_update = 120
			elif market_situation == "SUSPICIOUS":
				time_for_next_update = 30
			else:
				time_for_next_update = 60

			rsi = [RSI(np.asarray(market_data), timeperiod=20)[-i] for i in range(1,10)]
			mx_rsi = max(rsi)
			mn_rsi = min(rsi)
			print(f"RSI = {mx_rsi}//{mn_rsi}", )
			if(market_situation == "USUAL" or market_situation == "SUSPICIOUS" or (market_situation=="RISING" and mn_rsi>45.0) or (market_situation=="FALLING" and mx_rsi<55)):
				continue
			#rsi_value = RSI(market_data, timeperiod=14)
			rsi_message = "it's strong BUY signal" if mn_rsi <= 30 else "it's strong SELL signal" if mx_rsi >=70 else "maybe HOLD this time, you know, it's a little bit risky..."
			knot_message = "it's possible STRONG turinig point" if knot_idx < 0.3 else "it may be WEAK turning point"
			message = self.token + " is " + market_situation + " at " + str(market_data[-1]) + "\nRSI is " + str(rsi) + " | {}//{}".format(mn_rsi,mx_rsi) + " so " + rsi_message +"\nKNOT is " + str(knot_idx) + " means " + knot_message
			break	
		return message








class MyClientProtocol(WebSocketClientProtocol):

	def __init__(self, *args, **kwards):
		super(MyClientProtocol, self).__init__(*args, **kwards)
		self.payload = MarketProcessingPayload(TOKEN_NAME)


	def onConnect(self, response):
		print("Connected to bot server: {0}".format(response.peer))

	def onConnecting(self, transport_details):
		print("Connecting to bot server with status of: {}".format(transport_details))
		return None  # ask for defaults

	def current_milli_time(self):
		return round(time.time() * 1000)


	def onOpen(self):
		print("WebSocket connection open.")

		def send_task():
			if KILL_RECEIVED:
				return
			#for message in self.payload.wait_for_event():
			message_to_server = self.payload.wait_for_event()
				#print("sending random message {}".format(random.randint(10**5, 10**10)))
				#str_task = "some randowm text"
			self.sendMessage(message_to_server.encode('utf8'))
			self.factory.reactor.callLater(2, send_task)

		send_task()



	def onMessage(self, payload, isBinary):
		grabber_msg = payload.decode('utf8')
		print("RECEIVED ", grabber_msg)
		if grabber_msg == "KILL":
			global KILL_RECEIVED
			KILL_RECEIVED = True 
			self.sendClose()
		#print("Some go wrong! Server is not inteneded to answer clients!: ", grabber_msg)
		return


	def onClose(self, wasClean, code, reason):
		print("Connection wint bot dispatcher closed: {0}".format(reason))





if __name__ == '__main__':

	import sys

	from twisted.python import log
	from twisted.internet import reactor

	TOKEN_NAME = sys.argv[1]

	log.startLogging(sys.stdout)

	factory = WebSocketClientFactory("ws://127.0.0.1:9001")
	factory.protocol = MyClientProtocol
	#factory_state = WebSocketClientFactory("ws://127.0.0.1:9001")
	#factory_state.protocol = StateUpdateProtocol

	reactor.connectTCP("127.0.0.1", 9000, factory)
	#reactor.connectTCP("127.0.0.1", 9001, factory_state)
	try:
		reactor.run()
	except Exception:
		print("Proably sigterm was received")
		KILL_RECEIVED = True