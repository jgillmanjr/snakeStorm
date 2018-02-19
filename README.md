snakeStorm
==========
A python module for working with Liquid Web's StormAPI.

### Requirements ###
Requires the [requests](https://pypi.python.org/pypi/requests) package.

### Quick Start Example ###

To install: `pip install snakeStorm`

The following will get a grab the first 25 Storm servers on your account.

```
import snakeStorm
from pprint import pprint

client = snakeStorm.client('username', 'password')

client.endpoint.storm.server.list()

pprint(client.endpoint.storm.server.list.result)
```

Or if you wanted 99 records per page:
```
client.endpoint.storm.server.list(page_size=99)
```

### The Rest of the Story ###

#### Calling API Methods ###
Basically, when a `Client` object is instantiated, it pulls a list of
methods by way of the source JSON document that's actually used
for building the API documentation.

From the method list, an "attribute path", if you will, is created off of
the `endpoint` attribute, as demonstrated in the above example. You can
either directly call the attribute as previously shown, or if desired,
you can call the `request` method.

Either of these ways allow passing in parameters via `kwargs`.

#### Returns & Accessing the Results ####
The return is a boolean indicating the success of the API call.

A few things will cause this to return false:
* A non-200 status code
* The `error` key being present in the returned result dictionary
* The returned content isn't able to be parsed by the `json()` method

If the returned content isn't able to be parsed (a good situation where
this would happen is an authentication failure), the `result_text` of
the method object will still be accessible.

Additionally, the raw `Response` object is available by way of the
`raw_result` attribute of the method object. See the documentation for
[requests](http://docs.python-requests.org/en/master/) for more information.

If JSON parsing was successful (remember, you can still have an error),
the result will be transformed into a dictionary named `result`.