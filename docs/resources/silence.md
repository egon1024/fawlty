# Silence

## Sensu documentation

  * [Silence](https://docs.sensu.io/sensu-go/latest/observability-pipeline/observe-process/silencing/)
  * [API](https://docs.sensu.io/sensu-go/latest/api/core/silenced/)

## Class: Silence

This class represents a Sensu silence.  

The fields for a silence are:

  * `check` (str)
  * `subscription` (str)
  * `begin` (int)
  * `expire` (int)
  * `expire_at` (int)
  * `expire_on_resolve` (bool)
  * `creator` (str)
  * `reason` (str)
  * `metadata` (SilenceMetadata)

Example:

```python
from fawlty.resource.silence import Silence

data = {
    "metadata": {
        "name": "test",
        "labels": {"donottalkabout": "thewar"},
        "annotations": {"hotel": "inspectors"},
        "namespace": "default",
    }, 
    "begin": 1735424740,
    "check": "*",
    "creator": "mr_fawlty",
    "expire": 0,
    "expire_at": None,
    "expire_on_resolve": True,
    "reason": "I think he is hiding a woman visitor in his room",
    "subscription": "entity:room12",
}

a = Silence(**data)
a.set_client(my_client)
a.create()
```

## Other Classes

These classes should usually not need to be addressed directly, but can instead be referenced via data structure in the [Silence](#class_silence) class (see example above).

  * SilenceMetadata

