# ClusterRoleBinding

## Sensu documentation

  * [ClusterRoles](https://docs.sensu.io/sensu-go/latest/operations/control-access/rbac/#cluster-role-bindings)
  * [API](https://docs.sensu.io/sensu-go/latest/api/core/cluster-role-bindings/)

## Class: ClusterRoleBinding

This class represents a Sensu clusterrolebinding.  

The fields for an clusterrolebinding are:

  * `role_ref` (ClusterRoleBindingRoleRef)
  * `subjects` (list)
  * `metadata` (ClusterRoleBindingMetadata)

Example:

```python
from fawlty.resource.clusterrole import ClusterRole

data = {
    "metadata": {
        "name": "test",
        "labels": {"donottalkabout": "thewar"},
        "annotations": {"hotel": "inspectors"},
    }, 
    "role_ref": {
        "name": "cluster role name",
    },
    "subjects": [
        {"type": "Group", "name": "customers"},
        {"type": "User", "name": "major_gowen"}
    ],
}

a = ClusterRoleBinding(**data)
a.set_client(my_client)
a.create()
```

## Other Classes

These classes should usually not need to be addressed directly, but can instead be referenced via data structure in the [ClusterRoleBinding](#class_clusterrolebinding) class (see example above).

  * ClusterRoleBindingMetadata
  * ClusterRoleBindingSubject
  * ClusterRoleBindingRoleRef

