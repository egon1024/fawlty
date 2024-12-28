# Filter

## Sensu documentation

  * [Filter](https://docs.sensu.io/sensu-go/latest/observability-pipeline/observe-filter/)
  * [API](https://docs.sensu.io/sensu-go/latest/api/core/filters/)

## Class: Filter

This class represents a Sensu filter.  

The fields for a filter are:

  * `action` (str)
  * `expressions`: (list)
  * `runtime_assets`: (list)
  * `metadata` (FilterMetadata)

Example:

```python
from fawlty.resource.filter import Filter

data = {
    "metadata": {
        "name": "test",
        "labels": {"donottalkabout": "thewar"},
        "annotations": {"hotel": "inspectors"},
        "namespace": "default",
    }, 
    "action": "allow",
    "expressions": [
        "event.check.occurrences == 1",
        "event.check.occurrences > 1",
    ]
    "runtime_assets": [],
}

a = Filter(**data)
a.set_client(my_client)
a.create()
```

## Other Classes

These classes should usually not need to be addressed directly, but can instead be referenced via data structure in the [Filter](#class_filter) class (see example above).

  * FilterMetadata
