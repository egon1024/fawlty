# Namespace

## Sensu documentation

  * [Namespace](https://docs.sensu.io/sensu-go/latest/operations/control-access/namespaces/)
  * [API](https://docs.sensu.io/sensu-go/latest/api/core/namespaces/)

## Class: Namespace

This class represents a Sensu namespace.  

The fields for a namespace are:

  * `name` (str)

Example:

```python
from fawlty.resource.namespace import Namespace

data = {
    "name": "default",
} 

a = Namespace(**data)
a.set_client(my_client)
a.create()
```

## Other Classes

N/A