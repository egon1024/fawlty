# User

## Sensu documentation

  * [User](https://docs.sensu.io/sensu-go/latest/operations/control-access/rbac/#users)
  * [API](https://docs.sensu.io/sensu-go/latest/api/core/users/)

## Class: User

This class represents a Sensu user.  

The fields for a user are:

  * `username` (str)
  * `groups` (list)
  * `disabled` (bool)
  * `password` (str)
  * `metadata` (UserMetadata)

Example:

```python
from fawlty.resource.user import User

data = {
    "username": "polly",
    "groups": ["frontdesk", "kitchen", "waitstaff"],
    "password": "Sketchbook123",
    "disabled": False,
}

a = User(**data)
a.set_client(my_client)
a.create()
```

## Additional function

The `fawlty.resource.user` module has an additional helper function:

hash_password(password)
:    Takes a provided password and hashes it for use with Sensu.

## Additional Methods

The [User](#class_user) provides a few methods that are not common to other resources:

.change_password(old_password, new_password)
:    Will update the password for the user, presuming the provided old password is correct

.disable()
:    Causes the user to be disabled

.reinstate()
:    Change's a user's state from disabled to active

.reset_password(new_password)
:    Updates the password for the user object.

## Other Classes

These classes should not be used directly.

  * UserPasswordReset
  * UserChangePassword