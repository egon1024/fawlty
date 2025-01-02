"""
A module for Sensu check resources.
"""

# Built in imports
import re
from typing import Optional, List, Dict, Literal, ClassVar

# 3rd party imports
from pydantic import BaseModel, model_validator, field_validator

# Our imports
from fawlty.resources.base import ResourceBase, MetadataWithNamespace
from fawlty.sensu_client import SensuClient

# Constants
PROXY_NAME_RE = re.compile(r'^[\w\.\-]+$')


class CheckMetadata(MetadataWithNamespace):
    """
    A class to represent the data structure of a check metadata
    """


class CheckMetricTag(BaseModel):
    """
    A class to represent the data structure of a metric tag
    """
    name: str
    value: str


class CheckMetricThreshold(BaseModel):
    """
    A class to represent the data structure of a metric threshold
    """
    max: Optional[str] = None
    min: Optional[str] = None
    status: int

    @model_validator(mode='after')
    def check_fields(self):
        """
        Verify the provided fields have acceptable values
        """
        if self.max is None and self.min is None:
            raise ValueError("Threshold must define at least one of 'max' or 'min'")

        return self


class CheckOutputMetricThreshold(BaseModel):
    """
    A class to represent the data structure of an output metric threshold
    """
    name: str
    tags: Optional[List[CheckMetricTag]] = None
    null_status: Optional[int] = 0
    thresholds: List[CheckMetricThreshold]


class CheckPipeline(BaseModel):
    """
    A class to represent the data structure of a check pipeline
    """
    api_version: str = 'core/v2'
    name: str
    type: str = 'Pipeline'


class CheckProxyRequests(BaseModel):
    """
    A class to represent the data structure of a check proxy requests
    """
    entity_attributes: Optional[List[str]] = None
    splay: Optional[bool] = False
    splay_coverage: Optional[int] = None

    @model_validator(mode='after')
    def check_fields(self):
        """
        Validate the fields for the instance
        """
        if self.splay and self.splay_coverage is None:
            raise ValueError("'splay_coverage' must be set when 'splay' is True")

        return self


class CheckSecret(BaseModel):
    """
    A class to represent the data structure of a check secret
    """
    name: str
    secret: str


class CheckSubdue(BaseModel):
    """
    A class to represent the data structure of a check subdue
    """
    begin: str
    end: str
    repeat: Optional[List[Literal[
        "mondays", "tuesdays", "wednesdays", "thursdays", "fridays", "saturdays", "sundays"
        "weekdays", "weekends", "daily", "weekly", "monthly", "annually"
    ]]] = None

    # TODO: validate begin/end


class Check(ResourceBase):
    """
    A class to represent a Sensu check resource.
    """
    check_hooks: Optional[List[Dict[str, List[str]]]] = None
    command: str
    cron: Optional[str] = None
    env_vars: Optional[List[str]] = None
    handlers: Optional[List[str]] = None
    high_flap_threshold: Optional[int] = None
    interval: Optional[int] = None
    low_flap_threshold: Optional[int] = None
    output_metric_format: Optional[Literal[
        "nagios_perfdata", "graphite_plaintext", "influxdb_line",
        "opentsdb_line", "prometheus_text", ""
    ]] = None
    output_metric_handlers: Optional[List[str]] = None
    output_metric_tags: Optional[List[CheckMetricTag]] = None
    output_metric_thresholds: Optional[List[CheckOutputMetricThreshold]] = None
    pipelines: Optional[List[CheckPipeline]] = None
    proxy_entity_name: Optional[str] = None
    proxy_requests: Optional[CheckProxyRequests] = None
    publish: Optional[bool] = False
    round_robin: Optional[bool] = False
    runtime_assets: Optional[List[str]] = None
    scheduler: Optional[str] = None
    secrets: Optional[List[CheckSecret]] = None
    silenced: Optional[List[str]] = None
    stdin: Optional[bool] = False
    subdues: Optional[List[CheckSubdue]] = None
    subscriptions: List[str]
    timeout: Optional[int] = None
    ttl: Optional[int] = None
    metadata: CheckMetadata
    _sensu_client: Optional[SensuClient] = None

    BASE_URL: ClassVar[str] = "/api/core/v2/namespaces/{namespace}/checks"

    @classmethod
    def get_url(cls, *args, **kwargs) -> str:
        """
        Use the namespaced version of the class method.
        """
        return cls.get_url_with_namespace(*args, **kwargs)

    @field_validator("proxy_entity_name")
    def validate_proxy_entity_name(cls, value):
        """
        Validate the that name given for a proxy entity is acceptable.
        """
        # Special case, we'll switch empty string to None
        if value == '':
            return None

        if not PROXY_NAME_RE.search(value):
            raise ValueError(f"proxy_entity_name ({value}) is invalid")

        return value

    @field_validator("subscriptions")
    def validate_subscriptions(cls, value):
        """
        Validate that the subscription list is acceptable.
        """
        if len(value) < 1:
            raise ValueError("Subscription list must have at least one subscription name in it.")

        return value

    def urlify(self, purpose: str = None) -> str:
        """
        Return the URL for the check resource(s).

        :return: The URL for the check resource.
        """

        url = self.BASE_URL.format(namespace=self.metadata.namespace)

        if purpose != "create":
            url += f"/{self.metadata.name}"

        return url
