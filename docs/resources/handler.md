# Handler

## Sensu documentation

  * [Handler](https://docs.sensu.io/sensu-go/latest/observability-pipeline/observe-process/handlers/)
  * [API](https://docs.sensu.io/sensu-go/latest/api/core/handlers/)

## Class: Handler

This class represents a Sensu handler.  

The fields for a handler are:

  * `type` (str)
  * `command` (str)
  * `env_vars` (list)
  * `filters` (list)
  * `handlers` (list)
  * `mutator` (str)
  * `runtime_assets` (list)
  * `secrets` (list)
  * `socket` (HandlerSocket)
  * `timeout` (int)
  * `metadata` (HandlerMetadata)

Example:

```python
from fawlty.resource.handler import Handler

data = {
    "metadata": {
        "name": "slack",
        "labels": {"donottalkabout": "thewar"},
        "annotations": {"hotel": "inspectors"},
        "namespace": "default",
    }, 
    "command": 'sensu-slack-handler -c "${SLACK_CHANNEL}" -w "${SLACK_WEBHOOK}"',
    "env_vars": [
        "SLACK_WEBHOOK=https://hooks.slack.com/services/redacted",
        "SLACK_CHANNEL=#sensu",
    ],
    "filters": ["filter_interval_60_bihourly"],
    "handlers": None,
    "runtime_assets": "sensu-slack-handler",
    "timeout: "0",
    "type": "pipe",
}

a = Handler(**data)
a.set_client(my_client)
a.create()
```

## Other Classes

These classes should usually not need to be addressed directly, but can instead be referenced via data structure in the [Handler](#class_handler) class (see example above).

  * HandlerMetadata
  * HandlerSocket

