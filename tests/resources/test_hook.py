"""
Test cases for the Hook resource.
"""

# Built in imports

# 3rd party imports
import pytest

# Our imports
from fawlty.resources.base import ResourceBase, MetadataWithNamespace
from fawlty.resources.hook import Hook, HookMetadata
from fawlty.sensu_client import SensuClient

@pytest.fixture
def hook_metadata():
    return HookMetadata(name="test_hook", namespace="default")

@pytest.fixture
def hook(hook_metadata):
    return Hook(
        command="echo 'Hello, world!'",
        runtime_assets=["asset1", "asset2"],
        stdin=True,
        timeout=30,
        metadata=hook_metadata
    )

class TestHookMetadata:
    def test_hook_metadata(self, hook_metadata):
        assert hook_metadata.name == "test_hook"
        assert hook_metadata.namespace == "default"
        assert isinstance(hook_metadata, MetadataWithNamespace)

class TestHookInitialization:
    def test_hook_initialization(self, hook):
        assert hook.command == "echo 'Hello, world!'"
        assert hook.runtime_assets == ["asset1", "asset2"]
        assert hook.stdin is True
        assert hook.timeout == 30
        assert hook.metadata.name == "test_hook"
        assert hook.metadata.namespace == "default"
        assert hook._sensu_client is None
        assert isinstance(hook, ResourceBase)

class TestHookMethods:
    def test_hook_get_url(self):
        url = Hook.get_url(namespace="default")
        assert url == "/api/core/v2/namespaces/default/hooks"

    def test_hook_urlify_create(self, hook):
        url = hook.urlify(purpose="create")
        assert url == "/api/core/v2/namespaces/default/hooks"

    def test_hook_urlify_non_create(self, hook):
        url = hook.urlify()
        assert url == "/api/core/v2/namespaces/default/hooks/test_hook"

class TestResourceBaseMethods:
    def test_set_client(self, hook):
        assert hook._sensu_client is None
        hook.set_client(SensuClient())
        assert isinstance(hook._sensu_client, SensuClient)