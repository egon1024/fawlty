"""
Test cases for the User resource.
"""

# Built in imports
from unittest.mock import MagicMock, patch

# 3rd party imports
import bcrypt
import pytest

# Our imports
from fawlty.resources.base import ResourceBase
from fawlty.resources.user import UserPasswordReset, hash_password, UserChangePassword, User
from fawlty.sensu_client import SensuClient

@pytest.fixture
def user():
    return User(
        username="test_user",
        groups=["group1", "group2"],
    )


class TestHashPassword:
    def test_hash_password(self):
        hashed_pw = hash_password("password")
        assert bcrypt.checkpw("password".encode('utf-8'), hashed_pw.encode('utf-8'))

    def test_hash_password_different(self):
        hashed_pw = hash_password("password")
        assert not bcrypt.checkpw("different".encode('utf-8'), hashed_pw.encode('utf-8'))

class TestUserInitialization:
    def test_user_initialization(self, user):
        assert user.username == "test_user"
        assert user.groups == ["group1", "group2"]
        assert user._sensu_client is None
        assert isinstance(user, ResourceBase)
                          
    def test_initialize_user_with_good_password(self):
        _ = User(
            username="test_user",
            groups=["group1", "group2"],
            password="password"
        )

    def test_initialize_user_with_bad_password(self):
        with pytest.raises(ValueError):
            _ = User(
                username="test_user",
                groups=["group1", "group2"],
                password="short"
            )

class TestUserMethods:
    def test_user_get_url(self):
        url = User.get_url()
        assert url == "/api/core/v2/users"

    def test_user_urlify_create(self, user):
        url = user.urlify(purpose="create")
        assert url == "/api/core/v2/users"

    def test_user_urlify_non_create(self, user):
        url = user.urlify()
        assert url == "/api/core/v2/users/test_user"

    def test_disable_user(self, user):
        magic_delete = MagicMock()
        with patch.object(User, 'delete', magic_delete):
            user.disable()

        assert user.disabled is True
        magic_delete.assert_called_once()

    def test_reset_password(self, user):
        user._sensu_client = MagicMock()
        magic_update = MagicMock()
        with patch.object(UserPasswordReset, 'update', magic_update):
            user.reset_password("new_password")

        magic_update.assert_called_once()

    def test_change_password(self, user):
        user._sensu_client = MagicMock()
        magic_update = MagicMock()
        with patch.object(UserChangePassword, 'update', magic_update):
            user.change_password("old_password", "new_password")

        magic_update.assert_called_once()

    def test_change_password_no_client(self, user):
        with pytest.raises(Exception):
            user.change_password("old_password", "new_password")

    def test_reset_password_no_client(self, user):
        with pytest.raises(Exception):
            user.reset_password("new_password")

    def test_disable_user_no_client(self, user):
        with pytest.raises(Exception):
            user.disable()
    
    def test_user_reinstate(self, user):
        # Mock the resource_put method
        user._sensu_client = MagicMock()
        user.disabled = True
        user.reinstate()
        assert user.disabled is False
        user._sensu_client.resource_put.assert_called_once()

    def test_user_reinstate_no_client(self, user):
        with pytest.raises(Exception):
            user.reinstate()

class TestUserPasswordReset:
    def test_user_password_reset(self):
        reset_obj = UserPasswordReset(username="test_user", password_hash="dummyhash")
        assert reset_obj.username == "test_user"
        assert reset_obj.password_hash == "dummyhash"
        assert reset_obj._sensu_client is None
        assert isinstance(reset_obj, ResourceBase)

    def test_user_password_reset_get_url(self):
        url = UserPasswordReset.get_url()
        assert url == "/api/core/v2/users"

    def test_user_password_reset_urlify(self):
        reset_obj = UserPasswordReset(username="test_user", password_hash="dummyhash")
        url = reset_obj.urlify()
        assert url == "/api/core/v2/users/test_user/reset_password"

class TestUserChangePassword:
    def test_user_change_password(self):
        reset_obj = UserChangePassword(username="test_user", password="old_password", password_hash="dummyhash")
        assert reset_obj.username == "test_user"
        assert reset_obj.password == "old_password"
        assert reset_obj.password_hash == "dummyhash"
        assert reset_obj._sensu_client is None
        assert isinstance(reset_obj, ResourceBase)

    def test_user_change_password_get_url(self):
        url = UserChangePassword.get_url()
        assert url == "/api/core/v2/users"

    def test_user_change_password_urlify(self):
        reset_obj = UserChangePassword(username="test_user", password="old_password", password_hash="dummyhash")
        url = reset_obj.urlify()
        assert url == "/api/core/v2/users/test_user/password"