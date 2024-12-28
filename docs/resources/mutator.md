# Mutator

## Sensu documentation

  * [Mutator](https://docs.sensu.io/sensu-go/latest/observability-pipeline/observe-transform/mutators/)
  * [API](https://docs.sensu.io/sensu-go/latest/api/core/mutators/)

## Class: Mutator

This class represents a Sensu mutator.  

The fields for a mutator are:

  * `command` (str)
  * `env_vars` (list)
  * `eval` (str)
  * `runtime_assets` (list)
  * `secrets` (list)
  * `timeout` (int)
  * `type` (str)
  * `metadata` (MutatorMetadata)

Example:

```python
from fawlty.resource.mutator import Mutator

data = {
    "metadata": {
        "name": "test",
        "labels": {"donottalkabout": "thewar"},
        "annotations": {"hotel": "inspectors"},
        "namespace": "default",
    }, 
    "command": "/path/to/mutator_script",
    "timeout": 3,
    "type": "pipe"
}

a = Mutator(**data)
a.set_client(my_client)
a.create()
```

## Other Classes

These classes should usually not need to be addressed directly, but can instead be referenced via data structure in the [Mutator](#class_mutator) class (see example above).

  * MutatorMetadata

