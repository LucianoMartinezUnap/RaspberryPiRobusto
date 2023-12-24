#! /usr/bin/python

import http.client
import json

class Connection2DB:
	def __init__(self):
		pass
	def Post2DB(Url, Port, EndPoint, Key, Value):
		Conn = http.client.HTTPConnection(Url, Port, timeout=10)
		headers = {'Content-type': 'application/json'}
		json_data = json.dumps({Key: Value})
		Conn.request('POST', EndPoint, json_data, headers)
		response = Conn.getresponse()
		return response
		#print(f"response: {response.read().decode()}")
	def Post2DBDict(Url, Port, EndPoint, Dictionary):
		Conn = http.client.HTTPConnection(Url, Port, timeout=10)
		headers = {'Content-type': 'application/json'}
		json_data = json.dumps(Dictionary)
		Conn.request('POST', EndPoint, json_data, headers)
		response = Conn.getresponse()
		return response
