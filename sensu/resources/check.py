"""
A module for Sensu check resources.
"""

# Built in imports
import re
from typing import Optional, List, Dict, Literal

# Our imports
from sensu.resources.base import ResourceBase
from sensu.client import SensuClient

# 3rd party imports
from pydantic import BaseModel, model_validator, validator

# Constants
BASE_URL = "/api/core/v2/namespaces/{namespace}/checks"
PROXY_NAME_RE = re.compile('^[\w\.\-]+$')

def get_url(namespace: str, name: str = None) -> str:
    """
    Get a url to retrieve a list of matching check resources.
    """

    url = BASE_URL.format(namespace=namespace)
    if name is not None:
        url += f"/{name}"
    
    return url


class CheckMetadata(BaseModel):
    """
    A class to represent the data structure of a check metadata
    """
    name: str
    namespace: str
    created_by: Optional[str] = None
    labels: Optional[dict[str, str]] = {}
    annotations: Optional[dict[str, str]] = {}


class MetricTag(BaseModel):
    """
    A class to represent the data structure of a metric tag
    """
    name: str
    value: str


class MetricThreshold(BaseModel):
    max: Optional[str] = None
    min: Optional[str] = None
    status: int

    @model_validator(mode='after')
    def check_fields(self):
        if self.max is None and self.min is None:
            raise ValueError("Threshold must define at least one of 'max' or 'min'")

        return self


class OutputMetricThreshold(BaseModel):
    name: str
    tags: Optional[List[MetricTag]] = None
    null_status: Optional[int] = 0
    thresholds: List[MetricThreshold]


class CheckPipeline(BaseModel):
    api_version: str = 'core/v2'
    name: str
    type: str = 'Pipeline'


class CheckProxyRequests(BaseModel):
    entity_attributes: Optional[List[str]] = None
    splay: Optional[bool] = False
    splay_coverage: Optional[int] = None

    @model_validator(mode='after')
    def check_fields(self):
        if self.splay and self.splay_coverage is None:
            raise ValueError("'splay_coverage' must be set when 'splay' is True")

        return self


class CheckSecret(BaseModel):
    name: str
    secret: str


class CheckSubdue(BaseModel):
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
    output_metric_tags: Optional[List[MetricTag]] = None
    output_metric_thresholds: Optional[List[OutputMetricThreshold]] = None
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

    @validator("proxy_entity_name")
    def validate_proxy_entity_name(cls, value):
        # Special case, we'll switch empty string to None
        if value == '':
            return None

        if not PROXY_NAME_RE.search(value):
            raise ValueError(f"proxy_entity_name ({value}) is invalid")

        return value

    @validator("subscriptions")
    def validate_subscriptions(cls, value):
        if len(value) < 1:
            raise ValueError("Subscription list must have at least one subscription name in it.")

        return value

    def urlify(self, purpose: str=None) -> str:
        """
        Return the URL for the check resource(s).

        :return: The URL for the check resource.
        """

        url = BASE_URL.format(namespace=self.metadata.namespace)

        if purpose != "create":
            url += f"/{self.metadata.name}"

        return url
