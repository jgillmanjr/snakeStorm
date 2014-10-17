"""
snakeStorm Storm API Library

An attempt at a psuedo-clean room implementation of a Storm API Library to learn python

Jason Gillman Jr. <jason@rrfaae.com>
"""

import requests
import json

def listApiMethods(apiVersion = 'v1'):
	methodList = {}
	apiDocs = requests.request('GET', 'https://www.stormondemand.com/api/docs/' + apiVersion + '/docs.json').json()
	for (groupName,group) in apiDocs.iteritems():
		methodList[groupName] = []
		for (methodName, methodSpecs) in group['__methods'].iteritems():
			methodList[groupName].append(methodName)
	return methodList

class snakeStorm:

	def __init__(self, username, password, method, parameters = {}, version = 'v1'):	
		self.username		= username
		self.password		= password
		self.method			= method
		self.parameters		= parameters
		self.version		= version

		self.baseURI		= 'https://api.stormondemand.com'
		self.apiPort		= 443
		self.apiFormat		= 'json'
		self.fullURI		= '%s:%s/%s/%s.%s' % (self.baseURI, str(self.apiPort), self.version, self.method, self.apiFormat)

		## Request specific variables ##
		self.lastCall		= None # Store the result of the last Storm API Call here
		self.postData		= {'params': None} # What will get sent if actually passing params

	## Local Parameter Methods ##
	def addParam(self, key, value):
		""" Add a single parameter. If already set, it will be overwritten"""
		self.parameters[key] = value

	def addParams(self, paramDict):
		""" Add multiple parameters. If a parameter is already set, it will be overwritten. """
		if isinstance(paramDict, dict):
			for (key,value) in paramDict.iteritems():
				self.parameters[key] = value

	def clearParams(self):
		""" Remove all set parameters """
		self.parameters = {}

	def listParams(self):
		""" A holdover from me being used to having variable visibility """
		return self.parameters

	def removeParam(self, key):
		""" Remove a specific parameter by key """
		if self.parameters.has_key(key):
			del self.parameters[key]

	## API Interaction Methods ##
	def request(self):
		""" Send the request to the Storm API """
		## Do we have params or not? ##
		if len(self.parameters) > 0:
			self.postData['params'] = self.parameters
			self.lastCall = requests.post(self.fullURI, data = json.dumps(self.postData), auth = (self.username, self.password)).json()
		else:
			self.postData['params'] = None
			self.lastCall = requests.request('GET', self.fullURI, auth = (self.username, self.password)).json()

		return self.lastCall # For immediate usage
