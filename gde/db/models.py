from pathlib import Path
from typing import Any

from pydantic import Field, ConfigDict
from arango_orm import Collection, Relation, Graph, GraphConnection, Database

from . import get_db


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


class UserGraph(Collection):
    "Information about graphs created by user"

    __collection__ = "user_graphs"

    model_config = ConfigDict(extra="allow")

    key_: str = Field(..., alias="_key")  # graph name
    name: str | None = None  # Graph's dispaly title, uses key if None
    start_node: str | None = None
    layouts: dict | None = None


class Node(Collection):
    "Nodes for general purpose graph data storage"

    __collection__ = "nodes"

    model_config = ConfigDict(extra="allow")

    key_: str = Field(..., alias="_key")  # user supplied key prefixed by user graph name
    user_graph: str
    label: str | None = None  # Node's dispaly title, uses key if None


class Link(Relation):
    "Linkages to nodes for generaal purpose graphs"

    __collection__ = "links"

    model_config = ConfigDict(extra="allow")

    key_: str = Field(..., alias="_key")  # user supplied key prefixed by user graph name
    user_graph: str
    label: str | None = None  # Link's dispaly title, uses key if None


class GeneralGraph(Graph):
    __graph__ = "general_graph"

    graph_connections = [
        GraphConnection(Node, Link, Node)
    ]
