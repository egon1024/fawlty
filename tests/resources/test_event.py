"""
Test cases for the Event resource.
"""

# Built in imports

# 3rd party imports
import pytest

# Our imports
from fawlty.resources.base import ResourceBase, MetadataWithNamespace
from fawlty.resources.event import (
    Event, EventMetadata, EventCheckMetadata, EventCheckHistory, 
    EventCheckMetricTag, EventCheckSecret, EventCheckSubdue, 
    EventCheck, EventEntityMetadata, EventEntity
)
from fawlty.sensu_client import SensuClient


@pytest.fixture
def event_metadata():
    return EventMetadata(namespace="default")

@pytest.fixture
def event_check_metadata():
    return EventCheckMetadata(namespace="default", name="test")

@pytest.fixture
def event_check_history():
    return EventCheckHistory(status=0, executed=0)

@pytest.fixture
def event_check_metric_tag():
    return EventCheckMetricTag(name="test", value="tag")

@pytest.fixture
def event_check_secret():
    return EventCheckSecret(name="test", secret="secret")

@pytest.fixture
def event_check_subdue():
    return EventCheckSubdue(begin="00:00:00", end="23:59:59")

@pytest.fixture
def event_check(event_check_metadata, event_check_history, event_check_metric_tag, event_check_secret, event_check_subdue):
    return EventCheck(
        metadata=event_check_metadata,
        executed=0,
        history=[event_check_history],
        is_silenced=False,
        issued=0,
        last_ok=0,
        occurrences=0,
        occurrences_watermark=0,
        metric_tags=[event_check_metric_tag],
        secrets=[event_check_secret],
        subdue=event_check_subdue,
        state="passing",
        status=0,
        total_state_change=0,
    )

@pytest.fixture
def event_entity_metadata():
    return EventEntityMetadata(namespace="default", name="test")

@pytest.fixture
def event_entity(event_entity_metadata):
    return EventEntity(
        metadata=event_entity_metadata,
        deregister=False,
        entity_class="agent",
        last_seen=0,
        sensu_agent_version="6.12.0",
    )

@pytest.fixture
def event(event_metadata, event_check, event_entity):
    return Event(
        metadata=event_metadata,
        check=event_check,
        entity=event_entity,
        id="abc1234",
    )

class TestEventMetadata:
    def test_event_metadata(self, event_metadata):
        assert event_metadata.namespace == "default"
        assert isinstance(event_metadata, EventMetadata)
        # Event metadata does not contain a name or any other typical metadata fields
        assert not hasattr(event_metadata, "name")
        assert not hasattr(event_metadata, "labels")
        assert not hasattr(event_metadata, "annotations")
        assert not hasattr(event_metadata, "created_by")
                            
class TestEventCheckMetadata:
    def test_event_check_metadata(self, event_check_metadata):
        assert event_check_metadata.namespace == "default"
        assert isinstance(event_check_metadata, MetadataWithNamespace)

class TestEventCheckHistory:
    def test_event_check_history(self, event_check_history):
        assert event_check_history.status == 0
        assert event_check_history.executed == 0
        assert isinstance(event_check_history, ResourceBase)

class TestEventCheckMetricTag:
    def test_event_check_metric_tag(self, event_check_metric_tag):
        assert event_check_metric_tag.name == "test"
        assert event_check_metric_tag.value == "tag"
        assert isinstance(event_check_metric_tag, ResourceBase)

class TestEventCheckSecret:
    def test_event_check_secret(self, event_check_secret):
        assert event_check_secret.name == "test"
        assert event_check_secret.secret == "secret"
        assert isinstance(event_check_secret, ResourceBase)

class TestEventCheckSubdue:
    def test_event_check_subdue(self, event_check_subdue):
        assert event_check_subdue.begin == "00:00:00"
        assert event_check_subdue.end == "23:59:59"
        assert event_check_subdue.repeat is None
        assert isinstance(event_check_subdue, ResourceBase)

class TestEventCheck:
    def test_event_check(self, event_check):
        assert event_check.metadata.namespace == "default"
        assert event_check.metadata.name == "test"
        assert event_check.history[0].status == 0
        assert event_check.history[0].executed == 0
        assert event_check.secrets[0].name == "test"
        assert event_check.secrets[0].secret == "secret"
        assert event_check.subdue.begin == "00:00:00"
        assert event_check.subdue.end == "23:59:59"
        assert event_check.subdue.repeat is None
        assert isinstance(event_check, ResourceBase)

class TestEventEntityMetadata:
    def test_event_entity_metadata(self, event_entity_metadata):
        assert event_entity_metadata.namespace == "default"
        assert event_entity_metadata.name == "test"
        assert isinstance(event_entity_metadata, MetadataWithNamespace)


class TestEventEntity:
    def test_event_entity(self, event_entity):
        assert event_entity.metadata.namespace == "default"
        assert event_entity.metadata.name == "test"
        assert isinstance(event_entity, ResourceBase)
        assert event_entity.entity_class == "agent"
        assert event_entity.metadata.namespace == "default"
        assert event_entity.metadata.name == "test"
        assert event_entity.metadata.labels == {}

class TestEventInitialization:
    def test_event_initialization(self, event):
        assert event.check.metadata.namespace == "default"
        assert event.check.metadata.name == "test"
        assert event.check.history[0].status == 0
        assert event.check.history[0].executed == 0
        assert event.check.secrets[0].name == "test"
        assert event.check.secrets[0].secret == "secret"
        assert event.check.subdue.begin == "00:00:00"
        assert event.check.subdue.end == "23:59:59"
        assert event.check.subdue.repeat is None
        assert isinstance(event, ResourceBase)

class TestEventMethods:
    def test_event_get_url(self):
        url = Event.get_url(namespace="default")
        assert url == "/api/core/v2/namespaces/default/events"

    def test_event_urlify_create(self, event):
        url = event.urlify(purpose="create")
        assert url == "/api/core/v2/namespaces/default/events"
