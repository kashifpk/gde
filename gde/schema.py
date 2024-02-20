from typing import Literal

from pydantic import BaseModel, field_validator, computed_field, ConfigDict, Field
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


class NodeResponseSchema(BaseModel):
    model_config = ConfigDict(extra="allow")

    key_: str = Field(..., alias="_key")
    meta_: NodeMetaInformation = Field(..., alias="_meta")
    extra_info: dict = {}
    links_: list | None = Field([], alias="_links")


class LinkSchema(BaseModel):
    key_: str = Field(..., alias="_key")
    from_: str = Field(..., alias="_from")
    to_: str = Field(..., alias="_to")
    meta_: NodeMetaInformation = Field(..., alias="_meta")
    linked_node: NodeResponseSchema