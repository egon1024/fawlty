# Hook

## Sensu documentation

  * [Hook](https://docs.sensu.io/sensu-go/latest/observability-pipeline/observe-schedule/hooks/)
  * [API](https://docs.sensu.io/sensu-go/latest/api/core/hooks/)

## Class: Hook

This class represents a Sensu hook.  

The fields for a hook are:

  * `command` (str)
  * `runtime_assets` (list)
  * `stdin` (bool)
  * `timeout` (int)
  * `metadata` (HookMetadata)

Example:

```python
from fawlty.resource.hook import Hook

data = {
    "metadata": {
        "name": "upgradable_packages",
        "labels": {"donottalkabout": "thewar"},
        "annotations": {"hotel": "inspectors"},
        "namespace": "default",
    }, 
    "command": "apt list --upgradable",
    "runtime_assets": None,
    "stdin": False,
    "timeout": 60
}

a = Hook(**data)
a.set_client(my_client)
a.create()
```

## Other Classes

These classes should usually not need to be addressed directly, but can instead be referenced via data structure in the [Hook](#class_hook) class (see example above).

  * HookMetadata

