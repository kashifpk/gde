from arango_orm import Database

from ..db.models import NodeType, Node, Link
from ..schema import NodeMetaInformation


class NodeManager:
    "Manage operations on node like post-processing after db-fetch etc"

    IGNORE_FIELDS = {'key_', 'rev_', '_id', 'label', 'node_type', 'user_graph'}

    def __init__(self, db: Database) -> None:
        self.db = db
        self._node_types = {}

    @property
    def node_types(self):
        q = self.db.query(NodeType)
        for r in q:
            self._node_types[r._key] = r

        return self._node_types

    def post_process(self, node: Node|Link) -> dict:
        n_dict = node.model_dump(mode='json', by_alias=True, exclude=self.IGNORE_FIELDS)

        node._meta = node._meta or NodeMetaInformation(**n_dict.get('_meta', {}))
        node._meta.label = node._meta.label or node._key
        n_dict['_meta'] = node._meta.model_dump(mode='json')

        if isinstance(node, Link):

            n_dict['source'] = n_dict['_from'].removeprefix(Node.__collection__ + '/')
            n_dict['target'] = n_dict['_to'].removeprefix(Node.__collection__ + '/')
            del n_dict['_from']
            del n_dict['_to']

        if node._meta.node_type:
            # lookup node type
            node_type: NodeType = self._node_types.get(node._meta.node_type, None)

        return n_dict