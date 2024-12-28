# Client

## Client

In order to instantiate a client, one must import the SensuServer and SensuClient classes.  A SensuServer defines the parameters for accessing a given Sensu server.  The SensuClient is the wrapper that provides a simpler interface for talking to the server.

## Classes

### SensuServer

```python
from fawlty.sensu_server import SensuServer
```

The fields supported by a SensuServer when being instantiated:

  * `host` (required) The hostname or IP address of the Sensu server
  * `port` Integer representing the port number to connect to.  (_Default: 8080_)
  * `use_ssl`: Boolean indicating whether the connection should be ssl encrypted. (_Default: False_)
  * `ignore_cert`: Boolean indicating if the remote certificate validation should be performed.  Set to True when connecting to a server using a self-signed certificate, to avoid errors. (_Default: False_)

### SensuClient

```python
from fawlty.sensu_server import SensuServer
from fawlty.sensu_client import SensuClient
```

For the most part, after creating a client instance, direct action with it will be minimal.  The primary use will be to pass to resource classes and objects.

Currently, login only supports username/password and not an API token.   After instantiation (which requires a (#SensuServer) object), the `login` method of the instance will establish a session with the Sensu API.

After login, the API will provide a session token which will be tracked by the client object in the `token` attribute.  The client object will attempt to refresh a token if it is discovered to be close to expiration.  If the application code wishes to refresh a token, it can do so by calling the `refresh_token` method of the client instance.


## Sample code

```python
from fawlty.client import SensuClient
from fawlty.sensu_server import SensuServer
import fawlty.resources

s = SensuServer(host="localhost")
client = SensuClient(server=s)
client.login("basil", "fawlty")

# Add a namespace
new_ns = sensu.resources.namespace.Namespace(
    name="sybil"
)
new_ns.set_client(client)
new_ns.create()

# Get the list of all namespaces
namespaces = fawlty.resources.namespace.Namespace.get(client=client)
print(f"Namespaces: {namespaces})
```
