"""
Storm API Library

An attempt at a psuedo-clean room implementation of a Storm API Library to learn python

Jason Gillman Jr. <jason@rrfaae.com>
"""
import json

import requests

def listApiMethods(apiVersion = 'bleed'):
	""" Return a sorted list of API methods as they would need to be specified in the method parameter.
	Example: storm/config/list """

	methodList = []
	apiDocs = requests.request('GET', 'https://www.stormondemand.com/api/docs/' + apiVersion + '/docs.json').json()
	for (groupName,group) in apiDocs.items():
		for (methodName, methodSpecs) in group['__methods'].items():
			methodList.append(groupName + '/' + methodName)
	return sorted(methodList)

def methodInputParams(apiMethod, apiVersion = 'bleed'):
	""" Return a dict of any input parameters that the specified API method will take. Empty dict if no input parameters exist for the method. """
	apiDocs = dict((k.lower(), v) for k, v in requests.request('GET', 'https://www.stormondemand.com/api/docs/' + apiVersion + '/docs.json').json().items())
	methodGroup = '/'.join(apiMethod.lower().rsplit('/')[:-1]) # The "group" the method belongs to
	methodEnd = apiMethod.lower().rsplit('/')[-1:][0] # The last part of the method

	methodParams = apiDocs[methodGroup]['__methods'][methodEnd]['__input']
	return methodParams

class method:
	""" The class that defines API specific data, such as parameters. """

	def __init__(self, apiMethod, stormConnection, parameters = None):
		""" Creates a method object. Will need to pass in the Storm API method you want to use (such as Storm/Config/list) as well as the connection object.
		Parameters can be passed in now or later if required. """
		if parameters is None:
			self.parameters		= {}
		else:
			self.parameters			= parameters
		self.stormConnection	= stormConnection
		self.apiMethod			= apiMethod
		self.result				= None

	def addParams(self, **params):
		""" Add parameters. If a parameter is already set, it will be overwritten. """
		for (key,value) in params.items():
			self.parameters[key] = value

	def changeConn(self, stormConnection):
		""" Update the connection object without having to recreate the method object. """
		if isinstance(stormConnection, connection): # Only change if it's a connection object
			self.stormConnection = stormConnection

	def clearParams(self):
		""" Remove all set parameters. """
		self.parameters = {}

	def inputParams(self):
		""" Essentially a wrapper for methodInputParams() that automagically passes in the method in use and the version of the connection object. """
		return methodInputParams(self.apiMethod, self.stormConnection.version)

	def listParams(self):
		""" A holdover from me being used to having variable visibility. """
		return self.parameters

	def removeParams(self, *params):
		""" Remove specific parameters by key. """
		for key in params:
			if self.parameters.has_key(key):
				del self.parameters[key]

	def request(self):
		""" Make the request and return the result. """
		self.result = self.stormConnection.request(parameters = self.parameters, apiMethod = self.apiMethod)
		return self.result

class connection:

	def __init__(self, username, password, version = 'bleed', baseURI = 'https://api.stormondemand.com', apiPort = 443, verify = True):
		""" Creates a connection object for use by method objects. username and password required at a minimum """
		self.username		= username
		self.password		= password
		self.version		= version
		self.verify			= verify

		self.baseURI		= baseURI
		self.apiPort		= apiPort
		self.apiFormat		= 'json'

		## Specific properties for the last request ##
		self.lastResult		= None # Store the result of the last Storm API Call here
		self.lastMethod		= None # The last API method called
		self.lastParams		= {} # The last set of parameters used
		self.lastURI		= None # Full URI of the last call

	def returnMethod(self, apiMethod, parameters = None):
		""" Returns a method object"""
		if 'snakeStorm' not in locals():
			import snakeStorm
		return snakeStorm.method(apiMethod = apiMethod, stormConnection = self, parameters = parameters)

	def call(self, apiMethod, parameters = None):
		""" Instantly calls the requested method without needing to instantiate and manually call"""
		return self.returnMethod(apiMethod = apiMethod, parameters = parameters).request()

	def request(self, parameters, apiMethod):
		""" Send the request to the Storm API. """
		method = self.lastMethod = apiMethod
		fullURI = self.lastURI = '%s:%s/%s/%s.%s' % (self.baseURI, str(self.apiPort), self.version, method, self.apiFormat)
		self.lastParams = {} ## Clean out
		try:
			## Do we have params or not? ##
			if len(parameters) > 0: # We have parameters - make a POST
				postData = {}
				postData['params'] = self.lastParams = parameters
				self.lastResult = requests.post(fullURI, data = json.dumps(postData), auth = (self.username, self.password), verify = self.verify).json()
			else: # No parameters - make a GET
				self.lastResult = requests.request('GET', fullURI, auth = (self.username, self.password), verify = self.verify).json()
		except Exception as e:
			self.lastResult = {'snakeStormError': 'There was an error with the request. Check your credentials?'}

		return self.lastResult
