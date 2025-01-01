"""
Test the ClusterRoleBinding resource.
"""

# Built in imports

# 3rd party imports
import pytest

# Our imports
from fawlty.resources.clusterrolebinding import (
    ClusterRoleBinding, ClusterRoleBindingMetadata,
    ClusterRoleBindingRoleRef, ClusterRoleBindingSubject
)
from fawlty.resources.base import ResourceBase, MetadataWithoutNamespace
from fawlty.sensu_client import SensuClient

@pytest.fixture
def clusterrolebinding_metadata():
    return ClusterRoleBindingMetadata(name="test_clusterrolebinding")

@pytest.fixture
def clusterrolebindingsubject():
    return ClusterRoleBindingSubject(name="test_subject", type="User")

@pytest.fixture
def clusterrolebindingrole_ref():
    return ClusterRoleBindingRoleRef(name="test_role_ref")

@pytest.fixture
def clusterrolebinding(clusterrolebinding_metadata, clusterrolebindingsubject, clusterrolebindingrole_ref):
    return ClusterRoleBinding(
        metadata=clusterrolebinding_metadata,
        role_ref=clusterrolebindingrole_ref,
        subjects=[clusterrolebindingsubject]
    )

class TestClusterRoleBindingMetadata:
    def test_clusterrolebinding_metadata(self, clusterrolebinding_metadata):
        assert clusterrolebinding_metadata.name == "test_clusterrolebinding"
        assert isinstance(clusterrolebinding_metadata, MetadataWithoutNamespace)

class TestClusterRoleBindingSubject:
    def test_clusterrolebinding_subject(self, clusterrolebindingsubject):
        assert clusterrolebindingsubject.name == "test_subject"
        assert clusterrolebindingsubject.type == "User"

class TestClusterRoleBindingRoleRef:
    def test_clusterrolebinding_role_ref(self, clusterrolebindingrole_ref):
        assert clusterrolebindingrole_ref.name == "test_role_ref"
        assert clusterrolebindingrole_ref.type == "ClusterRole"

class TestClusterRoleBindingInitialization:
    def test_clusterrolebinding_initialization(self, clusterrolebinding):
        assert clusterrolebinding.metadata.name == "test_clusterrolebinding"
        assert clusterrolebinding.role_ref.name == "test_role_ref"
        assert clusterrolebinding.role_ref.type == "ClusterRole"
        assert clusterrolebinding.subjects[0].name == "test_subject"
        assert clusterrolebinding.subjects[0].type == "User"
        assert clusterrolebinding._sensu_client is None
        assert isinstance(clusterrolebinding, ResourceBase)

class TestClusterRoleBindingMethods:
    def test_clusterrolebinding_get_url(self):
        url = ClusterRoleBinding.get_url()
        assert url == "/api/core/v2/clusterrolebindings"

    def test_clusterrolebinding_urlify_create(self, clusterrolebinding):
        url = clusterrolebinding.urlify(purpose="create")
        assert url == "/api/core/v2/clusterrolebindings"

    def test_clusterrolebinding_urlify_non_create(self, clusterrolebinding):
        url = clusterrolebinding.urlify()
        assert url == "/api/core/v2/clusterrolebindings/test_clusterrolebinding"

class TestResourceBaseMethods:
    def test_set_client(self, clusterrolebinding):
        client = SensuClient()
        clusterrolebinding.set_client(client)
        assert clusterrolebinding._sensu_client == client