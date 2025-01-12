# Asset

## Sensu documentation

  * [Events](https://docs.sensu.io/sensu-go/latest/observability-pipeline/observe-events/events/)
  * [API](https://docs.sensu.io/sensu-go/latest/api/core/events/)

## Class: Event

This class represents a Sensu event.  

Example:

```python
from fawlty.resource.event import Event

a = Asset(**data)
a.set_client(my_client)
a.create()

events = my_client.resource_get(
    cls=fawlty.resources.event.Event,
    get_url=fawlty.resources.event.Event.get_url(namespace="default")
)

for event in events:
    if event.check.state != "passing":
       print("XX Event: "
        f"{event.entity.metadata.name}/{event.check.metadata.name}:  "
        f"{event.check.state}")
    else:
       print(" * Event: "
        f"{event.entity.metadata.name}/{event.check.metadata.name}:  "
        f"{event.check.state}")
```

## Other Classes

There are several auxilary classes that accompany events, many because they are very similar to the "normal" resource counterpart, but with addtional fields.

  * EventMetadata
  * EventCheckMetadata
  * EventCheckHistory
  * EventCheckMetricTag
  * EvenCheckSecret
  * EventCheckSubdue
  * EventCheck
  * EventEntityMetadata
  * EventEntity

