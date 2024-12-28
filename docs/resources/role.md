# Role

## Sensu documentation

  * [Role](https://docs.sensu.io/sensu-go/latest/operations/control-access/rbac/#roles)
  * [API](https://docs.sensu.io/sensu-go/latest/api/core/roles/)

## Class: Role

This class represents a Sensu role.  

The fields for a role are:

  * `rules` (list)
  * `metadata` (RoleMetadata)

Example:

```python
from fawlty.resource.role import Role

data = {
    "metadata": {
        "name": "basic-read",
        "labels": {"donottalkabout": "thewar"},
        "annotations": {"hotel": "inspectors"},
        "namespace": "default",
    }, 
    "rules": [
        {
            "resource_names": None,
            "resources": ["entities", "checks", "events"],
            "verbs": ["get", "list"],
        },
        {
            "resource_names": None,
            "resources": ["namespaces"],
            "verbs": ["list"]
        },
    ]
}

a = Role(**data)
a.set_client(my_client)
a.create()
```

## Other Classes

These classes should usually not need to be addressed directly, but can instead be referenced via data structure in the [Role](#class_role) class (see example above).

  * RoleMetadata
  * RoleRule

