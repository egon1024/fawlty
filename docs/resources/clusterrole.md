# ClusterRole

## Sensu documentation

  * [ClusterRoles](https://docs.sensu.io/sensu-go/latest/operations/control-access/rbac/#cluster-roles)
  * [API](https://docs.sensu.io/sensu-go/latest/api/core/cluster-roles/)

## Class: ClusterRole

This class represents a Sensu clusterrole.  

The fields for an clusterrole are:

  * `rules` (list of ClusterRoleRule)
  * `metadata` (ClusterRoleMetadata)

Example:

```python
from fawlty.resource.clusterrole import ClusterRole

data = {
    "metadata": {
        "name": "test",
        "labels": {"donottalkabout": "thewar"},
        "annotations": {"hotel": "inspectors"},
    }, 
    "rules": [
        {"verbs": ["get"], "resources": ["*"]},
    ],
}

a = ClusterRole(**data)
a.set_client(my_client)
a.create()
```

## Other Classes

These classes should usually not need to be addressed directly, but can instead be referenced via data structure in the [ClusterRole](#class_clusterrole) class (see example above).

  * ClusterRoleMetadata
  * ClusterRoleRule
