"""
Test cases for the Entity resource.
"""

# Built in imports

# 3rd party imports
import pytest
from pydantic import ValidationError

# Our imports
from fawlty.resources.base import ResourceBase, MetadataWithNamespace
from fawlty.resources.entity import Entity, EntityMetadata
from fawlty.sensu_client import SensuClient

@pytest.fixture
def entity_metadata():
    return EntityMetadata(name="test_entity", namespace="default")

@pytest.fixture
def entity(entity_metadata):
    return Entity(
        metadata=entity_metadata,
        deregister=False,
        entity_class="agent",
        deregistration=None,
        last_seen=0,
        redact=[],
        sensu_agent_version="1.0.0",
        subscriptions=["test"],
        user="agent"
    )

class TestEntityMetadata:
    def test_entity_metadata(self, entity_metadata):
        assert entity_metadata.name == "test_entity"
        assert entity_metadata.namespace == "default"
        assert isinstance(entity_metadata, MetadataWithNamespace)

class TestEntityInitialization:
    def test_entity_initialization(self, entity):
        assert entity.metadata.name == "test_entity"
        assert entity.metadata.namespace == "default"
        assert entity.deregister is False
        assert entity.entity_class == "agent"
        assert entity.deregistration is None
        assert entity.last_seen == 0
        assert entity.redact == []
        assert entity.sensu_agent_version == "1.0.0"
        assert entity.subscriptions == ["test"]
        assert entity.user == "agent"
        assert entity._sensu_client is None
        assert isinstance(entity, ResourceBase)

    def test_entity_invalid_deregistration(self, entity):
        for bad_deregistration in [
            "invalid_string", 
            {"more": "than", "one": "key"},
            {"invalid": "key"}
        ]:

            with pytest.raises(ValidationError):
                _ = Entity(
                    metadata=entity.metadata,
                    deregister=False,
                    entity_class="agent",
                    deregistration=bad_deregistration,
                    last_seen=0,
                    redact=[],
                    sensu_agent_version="1.0.0",
                    subscriptions=["test"],
                    user="agent"
                )

    def test_valid_registrations(self, entity):
        for good_deregistration in [
            None,
            {},
            {"handler": "handler"}
        ]:
            _ = Entity(
                metadata=entity.metadata,
                deregister=False,
                entity_class="agent",
                deregistration=good_deregistration,
                last_seen=0,
                redact=[],
                sensu_agent_version="1.0.0",
                subscriptions=["test"],
                user="agent"
            )
            assert _.deregistration == good_deregistration


class TestEntityMethods:
    def test_entity_get_url(self):
        url = Entity.get_url(namespace="default")
        assert url == "/api/core/v2/namespaces/default/entities"

    def test_entity_urlify_create(self, entity):
        url = entity.urlify(purpose="create")
        assert url == "/api/core/v2/namespaces/default/entities"

    def test_entity_urlify_non_create(self, entity):
        url = entity.urlify()
        assert url == "/api/core/v2/namespaces/default/entities/test_entity"

class TestResourceBaseMethods:
    def test_set_client(self, entity):
        client = SensuClient()
        entity.set_client(client)
        assert entity._sensu_client == client