from arango_orm import Database

from ..utils.dict_list_tools import dict_set_if_none_or_missing
from ..db.models import NodeType, Node, Link
from ..schemas import NodeMetaInformation, NodeResponseSchema, LinkSchema


class NodeManager:
    "Manage operations on node like post-processing after db-fetch etc"

    IGNORE_FIELDS = {"rev_", "_id", "label", "node_type", "user_graph"}

    def __init__(self, db: Database) -> None:
        self.db = db
        self._node_types = {}

    @property
    def node_types(self):
        q = self.db.query(NodeType)
        for r in q.all():
            self._node_types[r._key] = r

        return self._node_types

    def post_process(self, node: Node | Link) -> dict:
        n_dict = node.model_dump(mode="json", by_alias=True, exclude=self.IGNORE_FIELDS)

        node._meta = node._meta or NodeMetaInformation(**n_dict.get("_meta", {}))
        n_dict["_meta"] = node._meta.model_dump(mode="json")

        if isinstance(node, Link):
            n_dict["source"] = n_dict["_from"].removeprefix(Node.__collection__ + "/")
            n_dict["target"] = n_dict["_to"].removeprefix(Node.__collection__ + "/")
            del n_dict["_from"]
            del n_dict["_to"]

        if node._meta.node_type:
            # lookup node type
            node_type: NodeType = self.node_types.get(node._meta.node_type, None)
            if node_type:
                if node_type.label_field in n_dict:
                    # Set labe if label field exists in data
                    dict_set_if_none_or_missing(
                        n_dict, ["_meta", "label"], n_dict[node_type.label_field]
                    )

                dict_set_if_none_or_missing(
                    n_dict, ["_meta", "display_type"], node_type.default_display_type
                )
                dict_set_if_none_or_missing(
                    n_dict, ["_meta", "display_value"], node_type.default_display_value
                )
        else:
            dict_set_if_none_or_missing(n_dict, ["_meta", "label"], node._key)

        if hasattr(node, "_relations"):
            # class LinkSchema(BaseModel):
            #     key_: str = Field(..., alias="_key")
            #     from_: str = Field(..., alias="_from")
            #     to_: str = Field(..., alias="_to")
            #     meta_: NodeMetaInformation = Field(..., alias="_meta")
            #     linked_node: NodeResponseSchema
            n_dict["_links"] = []
            for k, links in node._relations.items():
                for link in links:

                    ls_d = dict(
                        _key=link._key,
                        source=link._from.split('/')[-1],
                        target=link._to.split('/')[-1],
                        _meta=link.model_dump()['_meta'],
                        linked_node=NodeResponseSchema(
                            **link._next.model_dump(
                                mode="json", by_alias=True, exclude=self.IGNORE_FIELDS
                            )
                        )
                    )
                    link_obj = LinkSchema(**ls_d)
                    n_dict["_links"].append(link_obj.model_dump(mode="json", by_alias=True))

        return n_dict
