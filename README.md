snakeStorm
==========

A python module for working with Liquid Web's StormAPI.

###Requirements###
Requires the [requests](https://pypi.python.org/pypi/requests) package.

###Quick Start Example###

To install: `pip install snakeStorm`

The following will get a grab a listing of servers on your account as well as the first page of config listings.

```
import snakeStorm

ProductionPublic = {'username': 'yourUser', 'password': 'yourPass', 'version': 'bleed'}
stormConn = snakeStorm.connection(**ProductionPublic)

serverList = snakeStorm.method('storm/server/list', stormConn)
configList = snakeStorm.method('storm/config/list', stormConn)

print 'Server Listing'
print serverList.request()

print 'Config Listing'
print configList.request()
```

###Non-TL;DR Information###

Well, installation method still stands as above (or you could clone this repo, that works too).

####snakeStorm.connection####
The `snakeStorm.connection` object is what will be used to communicate with the Storm API.

The `snakeStorm.method` object will be created for each method you want to call (or you could have multiple copies of the same method if you wanted - for example, if you wanted to use different params).

For the connection object, you'll really only need to pass along the `username`, `password`, and optionally the `version` (currently `v1` and `bleed` are supported).

For the most part, you probably don't need to worry about calling the methods in there directly.

####snakeStorm.method####
For the method object, you'll pass along the method in the form seen above (or pulled from `snakeStorm.listApiMethods()`), as well as the connection object you created above.

I'm too lazy right now to do full docs, so take a look at `help(snakeStorm.method)`
