"""
Test cases for the Mutator resource
"""

# Built in imports

# 3rd party imports
import pytest

# Our imports
from fawlty.resources.base import ResourceBase, MetadataWithNamespace
from fawlty.resources.mutator import Mutator, MutatorMetadata
from fawlty.sensu_client import SensuClient

@pytest.fixture
def mutator_metadata():
    return MutatorMetadata(name="test_mutator", namespace="default")

@pytest.fixture
def mutator(mutator_metadata):
    return Mutator(
        command="echo 'Hello, World!'",
        env_vars=["ENV_VAR1=value1", "ENV_VAR2=value2"],
        eval=None,
        runtime_assets=["asset1", "asset2"],
        secrets=[{"name": "secret1", "secret": "value1"}, {"name": "secret2", "secret": "value2"}],
        timeout=30,
        type="pipe",
        metadata=mutator_metadata
    )

class TestMutatorMetadata:
    def test_mutator_metadata(self, mutator_metadata):
        assert mutator_metadata.name == "test_mutator"
        assert mutator_metadata.namespace == "default"
        assert isinstance(mutator_metadata, MetadataWithNamespace)

class TestMutatorInitialization:
    def test_mutator_pipe_initialization(self, mutator):
        assert mutator.command == "echo 'Hello, World!'"
        assert mutator.env_vars == ["ENV_VAR1=value1", "ENV_VAR2=value2"]
        assert mutator.eval is None
        assert mutator.runtime_assets == ["asset1", "asset2"]
        assert mutator.secrets == [{"name": "secret1", "secret": "value1"}, {"name": "secret2", "secret": "value2"}]
        assert mutator.timeout == 30
        assert mutator.type == "pipe"
        assert mutator.metadata.name == "test_mutator"
        assert mutator.metadata.namespace == "default"
        assert mutator._sensu_client is None
        assert isinstance(mutator, ResourceBase)

    def test_mutator_javascript_initialization(self, mutator_metadata):
        mutator = Mutator(
            command=None,
            env_vars=None,
            eval="return 'Hello, World!';",
            runtime_assets=None,
            secrets=None,
            timeout=30,
            type="javascript",
            metadata=mutator_metadata
        )

        assert mutator.command is None
        assert mutator.env_vars is None
        assert mutator.eval == "return 'Hello, World!';"
        assert mutator.runtime_assets is None
        assert mutator.secrets is None
        assert mutator.timeout == 30
        assert mutator.type == "javascript"
        assert mutator.metadata.name == "test_mutator"
        assert mutator.metadata.namespace == "default"
        assert mutator._sensu_client is None
        assert isinstance(mutator, ResourceBase)

    def test_mutator_initialization_pipe_no_command(self, mutator_metadata):
        with pytest.raises(ValueError) as e:
            Mutator(
                command=None,
                env_vars=None,
                eval=None,
                runtime_assets=None,
                secrets=None,
                timeout=30,
                type="pipe",
                metadata=mutator_metadata
            )

        assert "If type is 'pip', the 'command' attribute must be set." in str(e.value)

    def test_mutator_initialization_pipe_eval_set(self, mutator_metadata):
        with pytest.raises(ValueError) as e:
            Mutator(
                command="echo 'Hello, World!'",
                env_vars=None,
                eval="return 'Hello, World!';",
                runtime_assets=None,
                secrets=None,
                timeout=30,
                type="pipe",
                metadata=mutator_metadata
            )

        assert "If type is 'pipe', the 'eval' attribute must not be set." in str(e.value)

    def test_mutator_initialization_javascript_no_eval(self, mutator_metadata):
        with pytest.raises(ValueError) as e:
            Mutator(
                command=None,
                env_vars=None,
                eval=None,
                runtime_assets=None,
                secrets=None,
                timeout=30,
                type="javascript",
                metadata=mutator_metadata
            )

        assert "If type is 'javascript', the 'eval' attribute must be set." in str(e.value)

    def test_mutator_initialization_javascript_command_set(self, mutator_metadata):
        with pytest.raises(ValueError) as e:
            Mutator(
                command="echo 'Hello, World!'",
                env_vars=None,
                eval="return 'Hello, World!';",
                runtime_assets=None,
                secrets=None,
                timeout=30,
                type="javascript",
                metadata=mutator_metadata
            )

        assert "If type is 'javascript', the 'command' attribute must not be set." in str(e.value)

class TestMutatorMethods:
    def test_mutator_get_url(self):
        url = Mutator.get_url(namespace="default")
        assert url == "/api/core/v2/namespaces/default/mutators"

    def test_mutator_urlify_create(self, mutator):
        url = mutator.urlify(purpose="create")
        assert url == "/api/core/v2/namespaces/default/mutators"

    def test_mutator_urlify_non_create(self, mutator):
        url = mutator.urlify()
        assert url == "/api/core/v2/namespaces/default/mutators/test_mutator"

class TestResourceBaseMethods:
    def test_set_client(self, mutator):
        client = SensuClient()
        mutator.set_client(client)
        assert mutator._sensu_client == client