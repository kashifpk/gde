from pathlib import Path
from typing import Any

from pydantic import Field, ConfigDict, BaseModel
from arango_orm import Collection, Relation, Graph, GraphConnection, Database

from . import get_db
from ..schema import NodeMetaInformation


class Setting(Collection):
    __collection__ = "settings"

    key_: str = Field(..., alias="_key")
    value: Any

    @classmethod
    def get(cls, key, default=None, db=None):
        if db is None:
            db = get_db()

        r = db.query(cls).filter_by(_key=key).first()
        if r is None:
            return default

        return r.value


class FieldSpecification(BaseModel):

    name: str
    label: str | None
    data_type: str
    content_type: str | None  # mime type style
    required: bool | None


class NodeType(Collection):
    """
    Node types configuration.

    - label: Display label, if not present then key_ is used
    - display: Node/edge display style. Format is 'type:value'.
      Type can be color, icon or image. Example 'color:#ff00ff', 'icon:fas fa-circle'
    - is_edge: Whether this data is for a node or an edge.

    """
    __collection__ = "node_types"

    model_config = ConfigDict(extra="allow")

    key_: str = Field(..., alias="_key")   # Node type name/key

    label_field: str | None = None
    default_display: str = 'color:#ff0000'
    display_fields_priority: list[str] = ['photo', 'icon', 'color']
    is_edge: bool = False
    fields: list[FieldSpecification]


class UserGraph(Collection):
    "Information about graphs created by user"

    __collection__ = "user_graphs"

    model_config = ConfigDict(extra="allow")

    key_: str = Field(..., alias="_key")  # graph name
    name: str | None = None  # Graph's dispaly title, uses key if None
    start_node: str | None = None
    layouts: dict | None = None


class NodeMeta:

    _meta: NodeMetaInformation | None = None
    user_graph: str


class Node(Collection, NodeMeta):
    "Nodes for general purpose graph data storage"

    __collection__ = "nodes"

    model_config = ConfigDict(extra="allow")

    key_: str = Field(..., alias="_key")  # user supplied key prefixed by user graph name


class Link(Relation, NodeMeta):
    "Linkages to nodes for generaal purpose graphs"

    __collection__ = "links"

    model_config = ConfigDict(extra="allow")



class GeneralGraph(Graph):
    __graph__ = "general_graph"

    graph_connections = [
        GraphConnection(Node, Link, Node)
    ]
