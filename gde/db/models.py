from typing import Any, Literal

from pydantic import Field, ConfigDict, BaseModel, validator
from arango_orm import Collection, Relation, Graph, GraphConnection

from . import get_db
from ..schemas import NodeMetaInformation
from ..utils.import_utils import import_module


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
    label: str | None = None
    data_type: str
    content_type: str | None = None  # mime type style
    required: bool | None = None
    choices: list | None = None  # Possible acceptable values for the field


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

    key_: str = Field(..., alias="_key")  # Node type name/key

    label_field: str | None = None
    default_display_type: str | None = None
    default_display_value: str | None = None
    display_fields_priority: list[str] = ["photo", "icon", "color"]
    is_edge: bool = False
    fields: list[FieldSpecification] | None = None
    fields_schema: str | None = None  # example we.GraphInfo (would import gde.schemas.we.GraphInfo)

    @validator("fields_schema")
    def fields_or_schema_must_be_present(cls, v, values):
        if v is None and values.get("fields") is None:
            raise ValueError("Either fields_schema or fields must be present")
        return v

    def model_dump(
        self,
        *,
        mode: str = "python",
        include: set[int] | set[str] | dict[int, Any] | dict[str, Any] | None = None,
        exclude: set[int] | set[str] | dict[int, Any] | dict[str, Any] | None = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        round_trip: bool = False,
        warnings: bool = True,
    ) -> dict[str, Any]:
        if self.fields_schema:
            schema = import_module(f"gde.schemas.{self.fields_schema}")
            json_schema = schema.model_json_schema(by_alias=True)
            self.fields = []

            for fname, finfo in json_schema["properties"].items():
                is_field_required = fname in json_schema.get("required", [])
                ftype = None
                if "type" in finfo:
                    ftype = finfo["type"]
                elif "oneOf" in finfo:
                    ftype = finfo["oneOf"][0]["type"]
                elif "anyOf" in finfo:
                    ftype = finfo["anyOf"][0]["type"]

                choices = None
                if hasattr(schema, "_schema_extra"):
                    choices = schema._schema_extra.default.get(fname, {}).get("choices")

                self.fields.append(
                    FieldSpecification(
                        name=fname, data_type=ftype, required=is_field_required, choices=choices
                    )
                )

        return super().model_dump(
            mode=mode,
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            warnings=warnings,
        )


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

    graph_connections = [GraphConnection(Node, Link, Node)]
