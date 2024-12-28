# RoleBinding

## Sensu documentation

  * [RoleBinding](https://docs.sensu.io/sensu-go/latest/operations/control-access/rbac/#role-bindings)
  * [API](https://docs.sensu.io/sensu-go/latest/api/core/role-bindings/)

## Class: RoleBinding

This class represents a Sensu rolebinding.  

The fields for a rolebinding are:

  * `role_ref` (RoleBindingRoleRef)
  * `subjects` (list)
  * `metadata` (RoleBindingMetadata)

Example:

```python
from fawlty.resource.rolebinding import RoleBinding

data = {
    "metadata": {
        "name": "kitchenstaff",
        "labels": {"donottalkabout": "thewar"},
        "annotations": {"hotel": "inspectors"},
        "namespace": "default",
    }, 
    "role_ref": {"type": "role", "name": "basic-read"}
    "subjects: [
        {"type": "User", "name": "Manuel"},
        {"type": "Group", "name": "chefs"}
    ]
}

a = RoleBinding(**data)
a.set_client(my_client)
a.create()
```

## Other Classes

These classes should usually not need to be addressed directly, but can instead be referenced via data structure in the [RoleBinding](#class_rolebinding) class (see example above).

  * RoleBindingMetadata
  * RoleBindingRoleRef
  * RoleBindingSubject