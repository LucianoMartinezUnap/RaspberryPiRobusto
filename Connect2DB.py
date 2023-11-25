#! /usr/bin/python

#from functools import singledispatchmethod 
import http.client
import json

class Connection2DB:

	def __init__(self):
		pass

	#@singledispatchmethod
	def Post2DB(Url, Port, EndPoint, Key, Value):
		Conn = http.client.HTTPConnection(Url, Port, timeout=10)
		headers = {'Content-type': 'application/json'}
		foo = {Key: Value}
		json_data = json.dumps(foo)
		Conn.request('POST', EndPoint, json_data, headers)
		response = Conn.getresponse()
		print(" ")
		print(response.read().decode())
		#print(f"Connection {Key} was made Successfuly")
		Conn.close()
	"""
	@Post2DB.register
	def _(Url, Port, EndPoint, Key: dict, Value= None):
		Conn = http.client.HTTPConnection(Url, Port, timeout=10)
		headers = {'Content-type': 'application/json'}
		json_data = json.dumps(Key)
		Conn.request('POST', EndPoint, json_data, headers)
		response = Conn.getresponse()
		print(" ")
		print(response.read().decode())
		Conn.close()
	"""
	def GetProviderConfirmation(RutProvider, Url, Endpoint):
		 # Create a connection to the server
    		Conn = http.client.HTTPConnection(Url)  # Replace with your server domain

	    	# Define the headers for the request
    		Headers = {'Content-type': 'application/json'}

    		# Create the request payload
    		Payload = json.dumps({"nfc": RutProvider})

    		try:
	        	# Send the POST request
	        	Conn.request("POST", Endpoint, body=Payload, headers=Headers)

		        # Get the response from the server
		        Response = Conn.getresponse()

	        	# Check if the request was successful (status code 200)
	        	if Response.status == 200:
                                        print("Iniciando reconocimiento facial")
                                        return True
	        	else:
                                        print(f"Error: {Response.status} - {Response.reason}")
                                        return False

	    	except Exception as e:
                        print(f"An error occurred: {e}")

	    	finally:
                        Conn.close()
