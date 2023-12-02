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
		#print(f"response: {response.read().decode()}")
		Conn.close()

	def GetProviderConfirmation(RutProvider, Url, Endpoint):
		Conn = http.client.HTTPConnection(Url)
		Headers = {'Content-type': 'application/json'}
		Payload = json.dumps({"nfc": RutProvider})
		
		try:
			Conn.request('POST', Endpoint, body = Payload, headers=Headers)
			Response = Conn.getresponse()
			#Conn.close()
			#print(f"longitud : {len(Response.read().decode())}  palabra: {Response.read().decode()}")
			return Response
		except Exception as e:
			print(f"Ha sucedido un error: {e}")
		#finally:
			#Conn.close()
