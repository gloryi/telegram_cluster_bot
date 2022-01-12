import time
import os
import signal

#MARKETS_MODEL = "WEEKEND"
MARKETS_MODEL = "INTRAWEEK"
#MARKETS_MODEL = "TEST"

market_models = {}

market_models["WEEKEND"] = ["ETH-USD", "ATOM1-USD", "OMG-USD", "SHIB-USD"]
market_models["INTRAWEEK"] = ["ETH-USD", "GLD", "^GSPC", "^RUT", "SB=F"]
market_models["TEST"] = ["ETH-USD"]

list_of_tokens = market_models[MARKETS_MODEL]

project_path = "/mnt/X/WORKSHOP/btc/CSHV"

casted_processes = []

p = subprocess.Popen(["python3", project_path+"/server.py"])#,"-r","some.file"])
casted_processes.append(p)

#time.sleep(10)

for token in list_of_tokens:
	p = subprocess.Popen(["python3", project_path+"/client.py", token, "MarketsPayload"])
	casted_processes.append(p)

try:
	while True:
		time.sleep(1)

except KeyboardInterrupt:
	print("=" * 50)
	print("Stopping system")
	print("=" * 50)

	#process_controller.stop()
	for p in casted_processes:
		#os.killpg(pid, signal.SIGTERM)
		p.terminate()

	print("=" * 50)
	print("System is stopped")
	print("=" * 50)
