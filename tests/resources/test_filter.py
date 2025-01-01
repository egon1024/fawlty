"""
Test cases for the Filter resource.
"""

# Built in imports

# 3rd party imports
import pytest

# Our imports
from fawlty.resources.base import ResourceBase, MetadataWithNamespace
from fawlty.resources.filter import Filter, FilterMetadata
from fawlty.sensu_client import SensuClient

@pytest.fixture
def filter_metadata():
    return FilterMetadata(name="test_filter", namespace="default")

@pytest.fixture
def filter(filter_metadata):
    return Filter(
        action="allow",
        expressions=["event.check.occurrences > 2"],
        metadata=filter_metadata
    )

class TestFilterMetadata:
    def test_filter_metadata(self, filter_metadata):
        assert filter_metadata.name == "test_filter"
        assert filter_metadata.namespace == "default"
        assert isinstance(filter_metadata, MetadataWithNamespace)

class TestFilterInitialization:
    def test_filter_initialization(self, filter):
        assert filter.action == "allow"
        assert filter.expressions == ["event.check.occurrences > 2"]
        assert filter.metadata.name == "test_filter"
        assert filter.metadata.namespace == "default"
        assert filter._sensu_client is None
        assert isinstance(filter, ResourceBase)

class TestFilterMethods:
    def test_filter_get_url(self):
        url = Filter.get_url(namespace="default")
        assert url == "/api/core/v2/namespaces/default/filters"

    def test_filter_urlify_create(self, filter):
        url = filter.urlify(purpose="create")
        assert url == "/api/core/v2/namespaces/default/filters"

    def test_filter_urlify_non_create(self, filter):
        url = filter.urlify()
        assert url == "/api/core/v2/namespaces/default/filters/test_filter"

class TestResourceBaseMethods:
    def test_set_client(self, filter):
        assert filter._sensu_client is None
        filter.set_client(SensuClient())
        assert isinstance(filter._sensu_client, SensuClient)