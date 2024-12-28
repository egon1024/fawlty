# Asset

## Sensu documentation

  * [Assets](https://docs.sensu.io/sensu-go/latest/plugins/assets/)
  * [API](https://docs.sensu.io/sensu-go/latest/api/core/assets/)

## Class: Asset

This class represents a Sensu asset.  

The fields for an asset are:

  * `url` (str)
  * `sha512` (str)
  * `filters` (list)
  * `headers` (dict)
  * `metadata` AssetMetadata

Example:

```python
from fawlty.resource.asset import Asset

data = {
    "url": "https://github.com/sensu/sensu-slack-handler/releases/download/1.0.3/sensu-slack-handler_1.0.3_linux_amd64.tar.gz",
    "sha512": "68720865127fbc7c2fe16ca4d7bbf2a187a2df703f4b4acae1c93e8a66556e9079e1270521999b5871473e6c851f51b34097c54fdb8d18eedb7064df9019adc8"
    "headers": {
        "X-Forwarded-For": "The Germans",
    }
    "metadata": {
        "name": "sensu-slack-handler",
        "namespace": "default",
        "labels": {"somelabel": "somevalue"},
        "annotations": {"manuel": "barcelona"}
    }
}

a = Asset(**data)
a.set_client(my_client)
a.create()
```

## Other Classes

These classes should usually not need to be addressed directly, but can instead be referenced via data structure in the [Asset](#class_asset) class (see example above).

  * AssetMetadata
