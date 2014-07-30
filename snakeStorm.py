"""
snakeStorm Storm API Library

An attempt at a psuedo-clean room implementation of a Storm API Library to learn python

Jason Gillman Jr. <jason@rrfaae.com>
"""

import requests
import json

class snakeStorm:

	def __init__(self, username, password, method, parameters = None, version = 'v1'):	
		self.username		= username
		self.password		= password
		self.method			= method
		self.parameters		= parameters
		self.version		= version

		self.baseURI		= 'https://api.stormondemand.com'
		self.fullURI		= self.baseURI + '/' + self.version + '/' + self.method + '.json'

	def testing(self):
		print self.fullURI
