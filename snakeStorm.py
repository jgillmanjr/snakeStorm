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
		self.apiPort		= 443
		self.apiFormat		= 'json'
		self.fullURI		= '%s:%s/%s/%s.%s' % (self.baseURI, str(self.apiPort), self.version, self.method, self.apiFormat)

	## Local Parameter Methods ##
	def addParam(self, key, value):
		""" Add a single parameter. If already set, it will be overwritten"""
		self.parameters[key] = value

	def addParams(self, paramDict):
		""" Add multiple parameters. If a parameter is already set, it will be overwritten. """
		if type(paramDict) is dict:
			for (key,value) in paramDict.iteritems():
				self.parameters[key] = value

	def clearParams(self):
		""" Remove all set parameters """
		self.parameters = None

	def listParams(self):
		""" A holdover from me being used to having variable visibility """
		return self.parameters

	def removeParam(self, key):
		""" Remove a specific parameter by key """
		if self.parameters.has_key(key):
			del self.parameters[key]
