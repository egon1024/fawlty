# Entity

[^ro]: Read only attribute

## Sensu documentation

  * [Entity](https://docs.sensu.io/sensu-go/latest/observability-pipeline/observe-entities/)
  * [API](https://docs.sensu.io/sensu-go/latest/api/core/entities/)

## Class: Entity

This class represents a Sensu entity.  

The fields for an entity are:

  * `metadata` (EntityMetadata)
  * `deregister` (bool)
  * `deregistration` (dict)
  * `entity_class` (str)
  * `last_seen` (int)
  * `redact` (list)
  * `sensu_agent_version`[^ro] (str)
  * `subscriptions` (list)
  * `system`[^ro] (dict)
  * `user` (str)

Example:

```python
from fawlty.resource.clusterrole import ClusterRole

data = {
    "metadata": {
        "name": "test",
        "labels": {"donottalkabout": "thewar"},
        "annotations": {"hotel": "inspectors"},
        "namespace": "torquay",
    }, 
    'entity_class': 'agent',
    'subscriptions': ['DailyExpress'],
    'deregister': False,
    'redact': ['horse_race'],
}

a = Entity(**data)
a.set_client(my_client)
a.create()
```

## Other Classes

These classes should usually not need to be addressed directly, but can instead be referenced via data structure in the [Entity](#class_entity) class (see example above).

  * EntityMetadata
