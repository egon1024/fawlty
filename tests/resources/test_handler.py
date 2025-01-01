"""
Test cases for the Handler resource.
"""

# Built in imports

# 3rd party imports
import pytest
from pydantic import ValidationError

# Our imports
from fawlty.resources.base import ResourceBase, MetadataWithNamespace
from fawlty.resources.handler import Handler, HandlerMetadata, HandlerSocket
from fawlty.sensu_client import SensuClient

@pytest.fixture
def handler_metadata():
    return HandlerMetadata(name="test_handler", namespace="default")

@pytest.fixture
def handler_socket():
    return HandlerSocket(host="localhost", port=80)

@pytest.fixture
def handler(handler_metadata, handler_socket):
    return Handler(
        type="pipe",
        command="/bin/true",
        env_vars=["VAR1=VALUE1", "VAR2=VALUE2"],
        filters=["filter1", "filter2"],
        mutator="mutator1",
        runtime_assets=["asset1", "asset2"],
        secrets=[{"name": "secret1", "secret": "value1"}, {"name": "secret2", "secret": "value2"}],
        timeout=30,
        metadata=handler_metadata
    )

class TestHandlerMetadata:
    def test_handler_metadata(self, handler_metadata):
        assert handler_metadata.name == "test_handler"
        assert handler_metadata.namespace == "default"
        assert isinstance(handler_metadata, MetadataWithNamespace)

class TestHandlerSocket:
    def test_handler_socket(self, handler_socket):
        assert handler_socket.host == "localhost"
        assert handler_socket.port == 80

class TestHandlerInitialization:
    def test_handler_initialization(self, handler):
        assert handler.type == "pipe"
        assert handler.command == "/bin/true"
        assert handler.env_vars == ["VAR1=VALUE1", "VAR2=VALUE2"]
        assert handler.filters == ["filter1", "filter2"]
        assert handler.handlers is None
        assert handler.mutator == "mutator1"
        assert handler.runtime_assets == ["asset1", "asset2"]
        assert handler.secrets == [{"name": "secret1", "secret": "value1"}, {"name": "secret2", "secret": "value2"}]
        assert handler.socket is None
        assert handler.timeout == 30
        assert handler.metadata.name == "test_handler"
        assert handler.metadata.namespace == "default"
        assert handler._sensu_client is None
        assert isinstance(handler, ResourceBase)

    def test_initialize_without_set_with_handlers(self, handler_metadata):
        with pytest.raises(ValidationError):
            _ = Handler(
                type="pipe",
                handlers=["handler1", "handler2"],
                metadata=handler_metadata
            )

    def test_initialize_with_set_without_handlers(self, handler_metadata):
        with pytest.raises(ValidationError):
            _ = Handler(
                type="set",
                metadata=handler_metadata
            )

    def test_initialize_without_type_with_socket(self, handler_metadata):
        with pytest.raises(ValidationError):
            _ = Handler(
                type="pipe",
                socket=HandlerSocket(host="localhost", port=80),
                metadata=handler_metadata
            )
        
    def test_initialize_with_type_without_socket(self, handler_metadata):
        with pytest.raises(ValidationError):
            _ = Handler(
                type="udp",
                metadata=handler_metadata
            )

    def test_initialize_without_pipe_with_command(self, handler_metadata):
        with pytest.raises(ValidationError):
            _ = Handler(
                type="tcp",
                command="/bin/true",
                metadata=handler_metadata,
                socket=HandlerSocket(host="localhost", port=80)
            )

    def test_initialize_without_pipe_with_env_vars(self, handler_metadata):
        with pytest.raises(ValidationError):
            _ = Handler(
                type="tcp",
                env_vars=["VAR1=VALUE1", "VAR2=VALUE2"],
                metadata=handler_metadata,
                socket=HandlerSocket(host="localhost", port=80)
            )

    def test_initialize_with_bad_secrets_dict(self, handler_metadata):
        with pytest.raises(ValidationError):
            _ = Handler(
                type="pipe",
                metadata=handler_metadata,
                command="/bin/true",
                secrets=[{"name": "something", "badkey": "value"}],
            )

class TestHandlerMethods:
    def test_handler_get_url(self):
        url = Handler.get_url(namespace="default")
        assert url == "/api/core/v2/namespaces/default/handlers"

    def test_handler_urlify_create(self, handler):
        url = handler.urlify(purpose="create")
        assert url == "/api/core/v2/namespaces/default/handlers"

    def test_handler_urlify_non_create(self, handler):
        url = handler.urlify()
        assert url == "/api/core/v2/namespaces/default/handlers/test_handler"

class TestResourceBaseMethods:
    def test_set_client(self, handler):
        client = SensuClient()
        handler.set_client(client)