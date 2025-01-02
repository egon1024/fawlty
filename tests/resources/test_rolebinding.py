"""
Test cases for the RoleBinding resource.
"""

# Built in imports

# 3rd party imports
import pytest

# Our imports
from fawlty.resources.base import ResourceBase, MetadataWithNamespace
from fawlty.resources.rolebinding import RoleBinding, RoleBindingMetadata, RoleBindingRoleRef, RoleBindingSubject
from fawlty.sensu_client import SensuClient

@pytest.fixture
def rolebinding_metadata():
    return RoleBindingMetadata(name="test_rolebinding", namespace="default")

@pytest.fixture
def rolebindingsubject():
    return RoleBindingSubject(name="test_user", type="User")

@pytest.fixture
def rolebindingroleref():
    return RoleBindingRoleRef(name="test_role")

@pytest.fixture
def rolebinding(rolebinding_metadata):
    return RoleBinding(
        metadata=rolebinding_metadata,
        role_ref=RoleBindingRoleRef(name="test_role"),
        subjects=[RoleBindingSubject(name="test_user", type="User")]
    )

class TestRoleBindingMetadata:
    def test_rolebinding_metadata(self, rolebinding_metadata):
        assert rolebinding_metadata.name == "test_rolebinding"
        assert rolebinding_metadata.namespace == "default"
        assert isinstance(rolebinding_metadata, MetadataWithNamespace)

class TestRoleBindingSubject:
    def test_rolebinding_subject(self, rolebindingsubject):
        assert rolebindingsubject.name == "test_user"
        assert rolebindingsubject.type == "User"

class TestRoleBindingRoleRef:
    def test_rolebinding_roleref(self, rolebindingroleref):
        assert rolebindingroleref.name == "test_role"
        assert rolebindingroleref.type == "Role"

class TestRoleBindingInitialization:
    def test_rolebinding_initialization(self, rolebinding):
        assert rolebinding.metadata.name == "test_rolebinding"
        assert rolebinding.metadata.namespace == "default"
        assert rolebinding.role_ref.name == "test_role"
        assert rolebinding.role_ref.type == "Role"
        assert rolebinding.subjects[0].name == "test_user"
        assert rolebinding.subjects[0].type == "User"
        assert rolebinding._sensu_client is None
        assert isinstance(rolebinding, ResourceBase)

class TestRoleBindingMethods:
    def test_rolebinding_get_url(self):
        url = RoleBinding.get_url(namespace="default")
        assert url == "/api/core/v2/namespaces/default/rolebindings"

    def test_rolebinding_urlify_create(self, rolebinding):
        url = rolebinding.urlify(purpose="create")
        assert url == "/api/core/v2/namespaces/default/rolebindings"

    def test_rolebinding_urlify_non_create(self, rolebinding):
        url = rolebinding.urlify()
        assert url == "/api/core/v2/namespaces/default/rolebindings/test_rolebinding"

class TestResourceBaseMethods:
    def test_set_client(self, rolebinding):
        client = SensuClient()
        rolebinding.set_client(client)