from typing import Literal

from pydantic import BaseModel, field_validator, computed_field
from slugify import slugify


class GraphSchema(BaseModel):

    graph_name: str

    # @field_validator('graph_name')
    # @classmethod
    # def graph_name_slugified(cls, v: str) -> str:
    #     return slugify(v)

    @computed_field
    @property
    def graph_key(self) -> str:
        return slugify(self.graph_name)

    nodes: dict = {}
    edges: dict = {}
    layouts: dict = {}


class NodeMetaInformation(BaseModel):

    node_type: str | None = None
    label: str | None = None
    display_type: Literal['color', 'icon', 'image'] | None = None
    display_value: str | None = None