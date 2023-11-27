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
