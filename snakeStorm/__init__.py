"""
Storm API Library

An attempt at a psuedo-clean room implementation of a Storm API Library to learn python

Jason Gillman Jr. <jason@rrfaae.com>
"""
import requests
import json

def listApiMethods(apiVersion = 'v1'):
	""" Return a sorted list of API methods as they would need to be specified in the method parameter.
	Example: storm/config/list """

	methodList = []
	apiDocs = requests.request('GET', 'https://www.stormondemand.com/api/docs/' + apiVersion + '/docs.json').json()
	for (groupName,group) in apiDocs.iteritems():
		for (methodName, methodSpecs) in group['__methods'].iteritems():
			methodList.append(groupName + '/' + methodName)
	return sorted(methodList)

class method:
	""" The class that defines API specific data, such as parameters. """

	def __init__(self, apiMethod, stormConnection, parameters = {}):
		""" Creates a method object. Will need to pass in the Storm API method you want to use (such as Storm/Config/list) as well as the connection object.
		Parameters can be passed in now or later if required. """
		self.parameters			= parameters
		self.stormConnection	= stormConnection
		self.apiMethod			= apiMethod
		self.result				= None

	def addParams(self, **params):
		""" Add parameters. If a parameter is already set, it will be overwritten. """
		for (key,value) in params.iteritems():
				self.parameters[key] = value

	def changeConn(self, stormConnection):
		""" Update the connection object without having to recreate the method object. """
		if isinstance(stormConnection, connection): # Only change if it's a connection object
			self.stormConnection = stormConnection

	def clearParams(self):
		""" Remove all set parameters. """
		self.parameters = {}

	def listParams(self):
		""" A holdover from me being used to having variable visibility. """
		return self.parameters

	def removeParams(self, *params):
		""" Remove specific parameters by key """
		for key in params:
			if self.parameters.has_key(key):
				del self.parameters[key]

	def request(self):
		""" Make the request and return the result """
		self.result = self.stormConnection.request(parameters = self.parameters, apiMethod = self.apiMethod)
		return self.result

class connection:

	def __init__(self, username, password, version = 'v1', baseURI = 'https://api.stormondemand.com', apiPort = 443, verify = True):
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

	## API Interaction Methods ##
	def request(self, parameters, apiMethod):
		""" Send the request to the Storm API. """
		method = self.lastMethod = apiMethod
		fullURI = self.lastURI = '%s:%s/%s/%s.%s' % (self.baseURI, str(self.apiPort), self.version, method, self.apiFormat)
		## Do we have params or not? ##
		if len(parameters) > 0: # We have parameters - make a POST
			postData = {}
			postData['params'] = self.lastParams = parameters
			self.lastResult = requests.post(fullURI, data = json.dumps(postData), auth = (self.username, self.password), verify = self.verify).json()
		else: # No parameters - make a GET
			self.lastResult = requests.request('GET', fullURI, auth = (self.username, self.password), verify = self.verify).json()

		return self.lastResult

	## Misc. Methods ##
	def changeBase(self, username, password, version = 'v1', baseURI = 'https://api.stormondemand.com', apiPort = 443, verify = True):
		""" You probably won't need this method... """
		self.baseURI	= baseURI
		self.apiPort	= apiPort
		self.verify 	= verify
		self.version	= version
		self.username	= username
		self.password	= password
