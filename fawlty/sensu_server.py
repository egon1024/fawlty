"""
A module to represent the connection information to a Sensu server API
"""

from pydantic import BaseModel, computed_field


class SensuServer(BaseModel):
    """
    A class to represent the connection information to a Sensu server API
    """

    host: str
    port: int = 8080
    use_ssl: bool = False
    ignore_cert: bool = False

    @computed_field
    @property
    def api_url(self) -> str:
        """
        Return the API URL.

        :return: The API URL.
        """
        return f"http{'s' if self.use_ssl else ''}://{self.host}:{self.port}"
