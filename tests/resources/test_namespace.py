"""
Test cases for the Namespace resource.
"""

# Built in imports

# 3rd party imports
import pytest
from pydantic import ValidationError

# Our imports
from fawlty.resources.base import ResourceBase
from fawlty.resources.namespace import Namespace
from fawlty.sensu_client import SensuClient

@pytest.fixture
def namespace():
    return Namespace(name="test_namespace")

class TestNamespaceInitialization:
    def test_namespace_initialization(self, namespace):
        assert namespace.name == "test_namespace"
        assert namespace._sensu_client is None
        assert isinstance(namespace, ResourceBase)

    def test_namespace_initialization_without_name(self):
        with pytest.raises(ValidationError):
            Namespace()

class TestNamespaceMethods:
    def test_namespace_get_url(self):
        url = Namespace.get_url()
        assert url == "/api/core/v2/namespaces"

    def test_namespace_urlify_create(self, namespace):
        url = namespace.urlify(purpose="create")
        assert url == "/api/core/v2/namespaces"

    def test_namespace_urlify_non_create(self, namespace):
        url = namespace.urlify()
        assert url == "/api/core/v2/namespaces/test_namespace"

class TestResourceBaseMethods:
    def test_set_client(self, namespace):
        client = SensuClient()
        namespace.set_client(client)
        assert namespace._sensu_client == client