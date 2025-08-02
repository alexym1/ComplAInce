"""Schema module."""

from pydantic import BaseModel


class Root(BaseModel):
    """Schema model to the root "/" endpoint."""

    version: str
    message: str
    description: str
    usage: str
