snakeStorm
==========

A python module for working with Liquid Web's StormAPI.

###Requirements###
Requires the [requests](https://pypi.python.org/pypi/requests) package.

###Quick Start Example###

To install: `pip install snakeStorm`

The following will get a grab a listing of servers on your account, as well as the first page of SSD config listings.

```
import snakeStorm

connectionDetails = {'username': 'yourUser', 'password': 'yourPass', 'version': 'bleed'}
stormConn = snakeStorm.connection(**connectionDetails)

serverList = stormConn.call('storm/server/list')
configList = stormConn.call('storm/config/list', {'category': 'ssd'})

print 'Server Listing'
print serverList.request()

print 'Config Listing'
print configList.request()
```

###Non-TL;DR Information###

Well, installation method still stands as above (or you could clone this repo, that works too).

####snakeStorm.connection(username, password, version = 'bleed', baseURI = 'https://api.stormondemand.com', apiPort = 443, verify = True)####
A `snakeStorm.connection` object is really all you need to worry about.

You'll really only need to about the `username`, `password`, and optionally, the `version` (currently `v1` and `bleed` are supported, `bleed` being the default) parameters.

#####call(apiMethod, parameters)#####
This method is the quickest way to call the API. Pass in the method and any parameters, and get a dictionary returned.

#####returnMethod(apiMethod, parameters)#####
Returns a `snakeStorm.method` class.

####snakeStorm.method(apiMethod, stormConnection, parameters = None)####
There are a few handy methods available when you are working with a `snakeStorm.method` object.

#####addParams(**params)#####
Allows additional parameters to be added after instantiation. If a parameter exists already, it will be overwritten.

#####clearParams()#####
Clear out any existing parameters

#####inputParams()#####
Returns a dict describing the available input parameters for the API method.

#####removeParams(*params)#####
Remove the list of parameters passed in.

#####request()#####
Make the call to the API.