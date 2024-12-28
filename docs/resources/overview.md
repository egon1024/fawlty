# Overview

This doc is a general overview of interacting with the resources classes.  As much as possible, the interfacing to each object is kept consistent.  There are two primary "types" of resources - those that require a namespace to be specified and those that do not.

Each module contains a class (CamelCase version of the module name) that is the main interface to resources of that type.  

## Common Interfaces

These interfaces are common to all resource objects:

### get

Before making a request to get resources, you must have a logged in [SensuClient](/client/#sensuclient) object.

Every resource class has a `.get` class method that can be called to retrive a list of resources.  The first argument is a mandatory reference to a [SensuClient](/client/#sensuclient) object.  If the specific resource resides within a namespace, that namespace should be the second argument.

Example:

```python
from fawlty.resources.entity import Entity

entities = Entity.get(
    client=my_sensu_client, # Must be instantiated and logged in
    namespace="default",    # Entity resources require this arg
)
```

This will provide a list of zero or more entities.  Any resource objects returned will have been seeded with the client instance used to retrieve them.

Most resource objects will also allow the retrieval of a specific resource by including the `name` argument, indicating the specific name of the resource to be retrieved.

### set_client

Call this method to add a client to a resource instance.  Necessary if you wish to write the values from the instance to the sensu server.

### create

To create a new resource, the `.create` method may be called on an object.  Requires the [set_client](#set_client) method to have been called first.

On success, returns a `True`.  Raises an exception otherwise.

### update

To update the values for a resource that already exists in the Sensu server, use the `.update` method.  Requires the [set_client](#set_client) method to have been called first.

On success, returns a `True`.  Raises an exception otherwise.

### delete

To delete a resource from the Sensu server, use the `.delete` method on an instance.  Requires the [set_client](#set_client) method to have been called first.

On success, returns a `True`.  Raises an exception otherwise.
