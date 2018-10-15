import requests
import time

def run(device,method):
	if device == 'kitchen_lights':
		run_kitchen_lights(method)


def run_kitchen_lights(method):
	if method == 'on':
		requests.get("http://192.168.0.29/setLevel?pin=8&level=256")
	elif method == 'off':
		requests.get("http://192.168.0.29/setLevel?pin=8&level=0")
	elif method == 'flash':
		requests.get("http://192.168.0.29/setLevel?pin=8&level=256")
		time.sleep(1)
		requests.get("http://192.168.0.29/setLevel?pin=8&level=0")
		time.sleep(1)
		requests.get("http://192.168.0.29/setLevel?pin=8&level=256")
		time.sleep(1)
		requests.get("http://192.168.0.29/setLevel?pin=8&level=0")
		time.sleep(1)
		requests.get("http://192.168.0.29/setLevel?pin=8&level=256")
		time.sleep(1)
		requests.get("http://192.168.0.29/setLevel?pin=8&level=0")
		time.sleep(1)
		requests.get("http://192.168.0.29/setLevel?pin=8&level=256")
