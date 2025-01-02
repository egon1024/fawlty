"""
Test cases for the Asset resource.
"""

# Built in imports

# 3rd party imports
import pytest

# Our imports
from fawlty.resources.base import ResourceBase, MetadataWithNamespace
from fawlty.resources.asset import Asset, AssetMetadata
from fawlty.sensu_client import SensuClient

@pytest.fixture
def asset_metadata():
    return AssetMetadata(name="test_asset", namespace="default")

@pytest.fixture
def asset(asset_metadata):
    return Asset(
        url="http://example.com/asset.tar.gz",
        sha512="dummysha512",
        filters=["filter1", "filter2"],
        headers={"Authorization": "Bearer token"},
        metadata=asset_metadata
    )

class TestAssetMetadata:
    def test_asset_metadata(self, asset_metadata):
        assert asset_metadata.name == "test_asset"
        assert asset_metadata.namespace == "default"
        assert isinstance(asset_metadata, MetadataWithNamespace)

class TestAssetInitialization:
    def test_asset_initialization(self, asset):
        assert asset.url == "http://example.com/asset.tar.gz"
        assert asset.sha512 == "dummysha512"
        assert asset.filters == ["filter1", "filter2"]
        assert asset.headers == {"Authorization": "Bearer token"}
        assert asset.metadata.name == "test_asset"
        assert asset.metadata.namespace == "default"
        assert asset._sensu_client is None
        assert isinstance(asset, ResourceBase)

class TestAssetMethods:
    def test_asset_get_url(self):
        url = Asset.get_url(namespace="default")
        assert url == "/api/core/v2/namespaces/default/assets"

    def test_asset_urlify_create(self, asset):
        url = asset.urlify(purpose="create")
        assert url == "/api/core/v2/namespaces/default/assets"

    def test_asset_urlify_non_create(self, asset):
        url = asset.urlify()
        assert url == "/api/core/v2/namespaces/default/assets/test_asset"

class TestResourceBaseMethods:
    def test_set_client(self, asset):
        client = SensuClient()
        asset.set_client(client)
        assert asset._sensu_client == client