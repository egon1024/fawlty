"""
Test cases for the base resource class.
"""

# Built in imports
from typing import ClassVar

# 3rd party imports
import pytest
from pydantic import BaseModel

# Our imports
from fawlty.resources.base import ResourceBase, MetadataWithoutNamespace, MetadataWithNamespace
from fawlty.exceptions import SensuClientError
from fawlty.sensu_client import SensuClient

class MockSensuClient:
    def resource_get(self, cls, get_url):
        return [cls()]

    def resource_post(self, obj):
        return True

    def resource_put(self, obj):
        return True

    def resource_delete(self, obj):
        return True

@pytest.fixture
def mock_client():
    return MockSensuClient()

@pytest.fixture
def resource_base():
    return ResourceBase()


class MockResourceWithNamespace(ResourceBase):
    BASE_URL: ClassVar[str] = "http://example.com/{namespace}/resource"

    @classmethod
    def get_url(cls, namespace: str, name: str = None) -> str:
        """
        Use the namespaced version of the class method.
        """
        
        return cls.get_url_with_namespace(namespace=namespace, name=name)

    def urlify(self, purpose: str = None) -> str:
        """
        Return the URL for the resource.
        """

        url = self.BASE_URL.format(namespace=self.metadata.namespace)

        if purpose != "create":
            url += f"/{self.metadata.name}"


class MockResourceWithoutNamespace(ResourceBase):
    BASE_URL: ClassVar[str] = "http://example.com/resource"

    @classmethod
    def get_url(cls, name: str = None) -> str:
        """
        Use the non-namespaced version of the class method.
        """
        
        return cls.get_url_without_namespace(name=name)
    
    def urlify(self, purpose: str = None) -> str:
        """
        Return the URL for the resource.
        """

        url = self.BASE_URL

        if purpose != "create":
            url += f"/{self.metadata.name}"


class TestResourceBase:
    def test_set_client(self, resource_base, mock_client):
        resource_base.set_client(mock_client)
        assert resource_base._sensu_client == mock_client

    def test_create(self, resource_base, mock_client):
        resource_base.set_client(mock_client)
        assert resource_base.create() is True

    def test_create_without_client(self, resource_base):
        with pytest.raises(SensuClientError):
            resource_base.create()

    def test_update(self, resource_base, mock_client):
        resource_base.set_client(mock_client)
        assert resource_base.update() is True

    def test_update_without_client(self, resource_base):
        with pytest.raises(SensuClientError):
            resource_base.update()

    def test_delete(self, resource_base, mock_client):
        resource_base.set_client(mock_client)
        assert resource_base.delete() is True

    def test_delete_without_client(self, resource_base):
        with pytest.raises(SensuClientError):
            resource_base.delete()

class TestResourceWithNamespace:
    def test_get_url_with_namespace(self):
        url = MockResourceWithNamespace.get_url_with_namespace(namespace="default", name="test")
        assert url == "http://example.com/default/resource/test"

    def test_get_with_namespace(self, mock_client):
        resources = MockResourceWithNamespace.get(client=mock_client, namespace="default", name="test")
        assert len(resources) == 1
        assert isinstance(resources[0], MockResourceWithNamespace)

class TestResourceWithoutNamespace:
    def test_get_url_without_namespace(self):
        url = MockResourceWithoutNamespace.get_url_without_namespace(name="test")
        assert url == "http://example.com/resource/test"

    def test_get_without_namespace(self, mock_client):
        resources = MockResourceWithoutNamespace.get(client=mock_client, name="test")
        assert len(resources) == 1
        assert isinstance(resources[0], MockResourceWithoutNamespace)

class TestMetadataWithoutNamespace:
    def test_metadata_without_namespace(self):
        metadata = MetadataWithoutNamespace(name="test")
        assert metadata.name == "test"
        assert metadata.created_by is None
        assert metadata.labels == {}
        assert metadata.annotations == {}

#class TestMetadataWithNamespace:
#    def test_metadata_with_namespace(self):
#        metadata = MetadataWithNamespace(name="test", namespace="default")
#        assert metadata.name == "test"
#        assert metadata.namespace == "default"
#        assert metadata.created_by is None
#        assert metadata.labels == {}
#        assert metadata.annotations == {}
#