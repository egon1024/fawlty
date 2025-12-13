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
  * `use_ssl`: Boolean indicating whether the connection should be SSL encrypted. (_Default: False_)
  * `ignore_cert`: Boolean indicating if remote certificate validation should be skipped. Set to `True` to disable SSL certificate verification entirely (not recommended for production). (_Default: False_)

#### SSL Certificate Handling

When `use_ssl=True` and `ignore_cert=False`, the client will verify SSL certificates using the system's CA certificate bundle. This allows connections to servers with certificates signed by custom CAs (such as self-signed certificates) as long as the CA certificate has been installed in the system's certificate store.

The client automatically searches for system CA bundles in common locations:

  * Environment variables: `REQUESTS_CA_BUNDLE`, `CURL_CA_BUNDLE`, `SSL_CERT_FILE`
  * Debian/Ubuntu: `/etc/ssl/certs/ca-certificates.crt`
  * RedHat/Fedora/CentOS: `/etc/pki/tls/certs/ca-bundle.crt`
  * OpenSUSE: `/etc/ssl/ca-bundle.pem`
  * macOS: `/usr/local/etc/openssl/cert.pem`, `/etc/ssl/cert.pem`

If no system CA bundle is found, the client falls back to the default certifi bundle included with the requests library.

### SensuClient

```python
from fawlty.sensu_server import SensuServer
from fawlty.sensu_client import SensuClient
```

For the most part, after creating a client instance, direct action with it will be minimal.  The primary use will be to pass to resource classes and objects.

Currently, login only supports username/password and not an API token.   After instantiation (which requires a (#SensuServer) object), the `login` method of the instance will establish a session with the Sensu API.

After login, the API will provide a session token which will be tracked by the client object in the `token` attribute.  The client object will attempt to refresh a token if it is discovered to be close to expiration.  If the application code wishes to refresh a token, it can do so by calling the `refresh_token` method of the client instance.


## Sample code

### Basic Usage (HTTP)

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

### SSL with Certificate Verification

```python
from fawlty.client import SensuClient
from fawlty.sensu_server import SensuServer

# Connect to a server with a valid SSL certificate
# (or a self-signed cert with CA installed in system certificate store)
s = SensuServer(host="sensu.example.com", port=8080, use_ssl=True)
client = SensuClient(server=s)
client.login("basil", "fawlty")
```

### SSL without Certificate Verification (Development Only)

```python
from fawlty.client import SensuClient
from fawlty.sensu_server import SensuServer

# Connect to a server with SSL but skip certificate validation
# WARNING: Only use this in development/testing environments
s = SensuServer(host="localhost", port=8080, use_ssl=True, ignore_cert=True)
client = SensuClient(server=s)
client.login("basil", "fawlty")
```
