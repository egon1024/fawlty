"""
Test the clusterrole resource
"""
import pytest
from pydantic import ValidationError

from fawlty.resources.base import MetadataWithoutNamespace
from fawlty.resources.clusterrole import ClusterRoleRule, ClusterRoleMetadata, ClusterRole
from fawlty.sensu_client import SensuClient

@pytest.fixture
def clusterrole_metadata():
    return ClusterRoleMetadata(
        name="test",
        labels={"app": "test"}
    )

@pytest.fixture
def clusterrole_rule():
    return ClusterRoleRule(
        resources=["*"],
        verbs=["get", "list"]
    )

@pytest.fixture
def clusterrole(clusterrole_metadata, clusterrole_rule):
    return ClusterRole(
        metadata=clusterrole_metadata,
        rules=[clusterrole_rule]
    )

class TestClusterRoleMetadata:
    def test_clusterrole_metadata(self, clusterrole_metadata):
        assert clusterrole_metadata.name == "test"
        assert clusterrole_metadata.labels == {"app": "test"}
        assert isinstance(clusterrole_metadata, MetadataWithoutNamespace)

class TestClusterRoleRule:
    def test_clusterrole_rule(self, clusterrole_rule):
        assert clusterrole_rule.resources == ["*"]
        assert clusterrole_rule.verbs == ["get", "list"]

    def test_invalid_verb(self):
        with pytest.raises(ValidationError):
            ClusterRoleRule(resources=["*"], verbs=["get", "list", "invalid"])

    def test_verbs_with_star(self):
        with pytest.raises(ValidationError):
            ClusterRoleRule(resources=["*"], verbs=["*", "get"])

    def test_invalid_resource(self):
        with pytest.raises(ValidationError):
            ClusterRoleRule(resources=["*invalid"], verbs=["get"])

    def test_resources_with_star(self):
        with pytest.raises(ValidationError):
            ClusterRoleRule(resources=["*", "assets"], verbs=["get"])

class TestClusterRoleInitialization:
    def test_clusterrole_initialization(self, clusterrole):
        assert clusterrole.metadata.name == "test"
        assert clusterrole.metadata.labels == {"app": "test"}
        assert clusterrole.rules[0].resources == ["*"]
        assert clusterrole.rules[0].verbs == ["get", "list"]
        assert clusterrole._sensu_client is None

    def test_clusterrole_invalid_rule(self, clusterrole_metadata):
        with pytest.raises(ValidationError):
            ClusterRole(metadata=clusterrole_metadata, rules=["a string", "another string"])

class TestClusterRoleMethods:
    def test_clusterrole_get_url(self):
        url = ClusterRole.get_url()
        assert url == "/api/core/v2/clusterroles"

    def test_clusterrole_urlify_create(self, clusterrole):
        url = clusterrole.urlify(purpose="create")
        assert url == "/api/core/v2/clusterroles"

    def test_clusterrole_urlify_non_create(self, clusterrole):
        url = clusterrole.urlify()
        assert url == "/api/core/v2/clusterroles/test"

class TestResourceBaseMethods:
    def test_set_client(self, clusterrole):
        client = SensuClient()
        clusterrole.set_client(client)
        assert clusterrole._sensu_client == client