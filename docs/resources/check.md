# Check

## Sensu documentation

  * [Checks](https://docs.sensu.io/sensu-go/latest/observability-pipeline/observe-schedule/checks/)
  * [API](https://docs.sensu.io/sensu-go/latest/api/core/checks/)

## Class: Check

This class represents a Sensu check.  

The fields for a check are:

  * `check_hooks` (list)
  * `command` (str)
  * `cron` (str)
  * `env_vars`: (list)
  * `handlers`: (list)
  * `high_flap_threshold` (int)
  * `low_flap_threshold` (int)
  * `output_metric_format` (int)
  * `output_metric_handlers` (list)
  * `output_metric_tags` (list)
  * `output_metric_thresholds` (list)
  * `pipelines` (list)
  * `proxy_entity_name` (str)
  * `publish` (bool)
  * `round_robin` (bool)
  * `runtime_assets` (list)
  * `scheduler` (str)
  * `secrets` (list)
  * `silenced` (list)
  * `stdin` (bool)
  * `subdues` (list)
  * `subscriptions` (list)
  * `timeout` (int)
  * `ttl` (int)

Example:

```python
from fawlty.resource.check import Check

data = {
    "command": "check-cpu-usage -w 75 -c 90",
    "handlers": [],
    "high_flap_threshold": 0,
    "interval": 60,
    "low_flap_threshold": 0,
    "public": True,
    "runtime_assets": [
        "check-cpu-usage"
    ],
    "subscriptions": [
        "system"
    ],
    "proxy_entity_name": "",
    "check_hooks": None,
    "stdin": False,
    "subdue": None,
    "ttl": 0,
    "timeout": 0,
    "round_robin": False,
    "output_metric_format": "",
    "output_metric_handlers": None,
    "env_vars": None,
    "metadata": {
        "name": "check_cpu",
        "namespace": "default",
        "labels": {},
        "annotations": {},
    },
    "secrets": None,
    "pipelines": None,
}

c = Check(**data)
c.set_client(my_client)
c.create()
```

## Other Classes

These classes should usually not need to be addressed directly, but can instead be referenced via data structure in the [Check](#class_check) class (see example above).

  * CheckMetadata
  * CheckMetricTag
  * CheckMetricThreshold
  * CheckOutputMetricThreshold
  * CheckPipeline
  * CheckProxyRequests

