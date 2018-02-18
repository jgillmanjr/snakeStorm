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

More detailed documentation to follow