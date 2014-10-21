"""
snakeStorm Storm API Library

An attempt at a psuedo-clean room implementation of a Storm API Library to learn python

Jason Gillman Jr. <jason@rrfaae.com>
"""
import requests
import json

methods = {}
connection = None


def initialize(username, password, version = 'v1'):
	""" 'Initializes' the module and generates the API method classes. """
	methodList = listApiMethods(version)

	for x in methodList:
		methods[x.lower()] = stormMethod(x)

	global connection
	connection = stormConnection(username, password, version)

def listApiMethods(apiVersion = 'v1'):
	""" Return a sorted list of API methods as they would need to be specified in the method parameter.
	Example: storm/config/list"""

	methodList = []
	apiDocs = requests.request('GET', 'https://www.stormondemand.com/api/docs/' + apiVersion + '/docs.json').json()
	for (groupName,group) in apiDocs.iteritems():
		for (methodName, methodSpecs) in group['__methods'].iteritems():
			methodList.append(groupName + '/' + methodName)
	return sorted(methodList)

class stormMethod:
	""" The class that defines API specific data, such as parameters. """

	def __init__(self, apiMethod):
		#print 'Object for the ' + apiMethod + ' Storm API method created!'
		self.parameters = {}
		self.result = None
		self.apiMethod = apiMethod

	def addParams(self, **params):
		""" Add parameters. If a parameter is already set, it will be overwritten. """
		for (key,value) in params.iteritems():
				self.parameters[key] = value

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
		""" Call the specified API method """
		self.result = connection.request(parameters = self.parameters, apiMethod = self.apiMethod)

class stormConnection:

	def __init__(self, username, password, version = 'v1'):
		""" Instantiate the snakeStorm class. At a mininimum you'll need to specify the username, password, and method. """
		self.username		= username
		self.password		= password
		self.version		= version
		self.verify			= True

		self.baseURI		= 'https://api.stormondemand.com'
		self.apiPort		= 443
		self.apiFormat		= 'json'

		## Request specific variables ##
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
	def changeBase(self, baseURI = 'https://api.stormondemand.com', apiPort = 443, verify = True):
		""" You probably won't need this method... """
		self.baseURI	= baseURI
		self.apiPort	= apiPort
		self.verify 	= verify
