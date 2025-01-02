"""
Test cases for the Role resource.
"""

# Built in imports

# 3rd party imports
import pytest
from pydantic import ValidationError

# Our imports
from fawlty.resources.base import ResourceBase, MetadataWithNamespace
from fawlty.resources.role import Role, RoleMetadata, RoleRule
from fawlty.sensu_client import SensuClient

@pytest.fixture
def role_metadata():
    return RoleMetadata(name="test_role", namespace="default")

@pytest.fixture
def role_rule():
    return RoleRule(verbs=["get"], resources=["assets"])

@pytest.fixture
def role(role_metadata, role_rule):
    return Role(
        rules=[role_rule],
        metadata=role_metadata
    )

class TestRoleMetadata:
    def test_role_metadata(self, role_metadata):
        assert role_metadata.name == "test_role"
        assert role_metadata.namespace == "default"
        assert isinstance(role_metadata, MetadataWithNamespace)

class TestRoleRule:
    def test_role_rule(self, role_rule):
        assert role_rule.verbs == ["get"]
        assert role_rule.resources == ["assets"]
        assert role_rule.resource_names is None

    def test_role_rule_invalid_verb(self):
        with pytest.raises(ValidationError):
            RoleRule(verbs=["invalid"], resources=["assets"])

    def test_role_rule_invalid_resource(self):
        with pytest.raises(ValidationError):
            RoleRule(verbs=["get"], resources=["invalid"])

    def test_role_rule_with_star_verb_and_other(self):
        with pytest.raises(ValidationError):
            RoleRule(verbs=["*", "get"], resources=["assets"])

    def test_role_rule_with_star_resource_and_other(self):
        with pytest.raises(ValidationError):
            RoleRule(verbs=["get"], resources=["*", "assets"])
        
class TestRoleInitialization:
    def test_role_initialization(self, role):
        assert role.rules[0].verbs == ["get"]
        assert role.rules[0].resources == ["assets"]
        assert role.metadata.name == "test_role"
        assert role.metadata.namespace == "default"
        assert role._sensu_client is None
        assert isinstance(role, ResourceBase)

class TestRoleMethods:
    def test_role_get_url(self):
        url = Role.get_url(namespace="default")
        assert url == "/api/core/v2/namespaces/default/roles"

    def test_role_urlify_create(self, role):
        url = role.urlify(purpose="create")
        assert url == "/api/core/v2/namespaces/default/roles"

    def test_role_urlify_non_create(self, role):
        url = role.urlify()
        assert url == "/api/core/v2/namespaces/default/roles/test_role"

class TestResourceBaseMethods:
    def test_set_client(self, role):
        role.set_client(SensuClient())
        assert isinstance(role._sensu_client, SensuClient)