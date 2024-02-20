import logging

from fastapi import Depends, Request, HTTPException, status
from fastapi_views import ViewRouter
from arango_orm import Database
from arango_orm.exceptions import DocumentNotFoundError

from . import API_BASE
from .settings import get_settings

from .utils.cbv import cbv
from .utils.inferring_router import InferringRouter
from .utils.crud import CRUDAPIBase
from .utils.node_manager import NodeManager
from .db import get_db
from .db.models import GeneralGraph, UserGraph, Node, Link, NodeType

from .schema import GraphSchema, NodeResponseSchema

log = logging.getLogger(__name__)

router = InferringRouter()
# API_PATH = API_BASE + "user-graphs"


@cbv(router)
class UserGraphAPI:
    """Class based API for managing user graphs."""

    request: Request

    db: Database = Depends(get_db)
    USER_GRAPH_API_PATH = API_BASE + "user-graphs"

    @router.get(USER_GRAPH_API_PATH)
    def list_user_graphs(self) -> list[dict]:
        "List available user graphs"

        return []

    @router.get(USER_GRAPH_API_PATH + "/{graph_key}")
    def get_user_graph(self, graph_key: str) -> GraphSchema:
        ug: UserGraph = self.db.query(UserGraph).by_key(graph_key)
        node_manager = NodeManager(self.db)

        node_recs: list[Node] = self.db.query(Node).filter_by(user_graph=ug._key).all()
        nodes = {}

        for n_rec in node_recs:
            nodes[n_rec._key] = node_manager.post_process(n_rec)

        link_recs: list[Link] = self.db.query(Link).filter_by(user_graph=ug._key).all()
        edges = {}
        for l_rec in link_recs:
            edges[l_rec._key] = node_manager.post_process(l_rec)

        ret = GraphSchema(graph_name=ug.name, layouts=ug.layouts, nodes=nodes, edges=edges)

        return ret

    @router.post(USER_GRAPH_API_PATH)
    def save_graph(self, item: GraphSchema) -> str:
        log.debug(item)
        ug = self.db.query(UserGraph).filter_by(_key=item.graph_key).first()
        # if ug is not None:
        #     raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Already exists")

        if ug:
            ug.layouts = item.layouts
            self.db.update(ug)
            self.db.query(Node).filter_by(user_graph=ug._key).delete()
            self.db.query(Link).filter_by(user_graph=ug._key).delete()
            ret_msg = f"Graph '{ug._key}' updated"
        else:
            ug = UserGraph(_key=item.graph_key, name=item.graph_name, layouts=item.layouts)
            self.db.add(ug)
            ret_msg = f"Graph '{ug._key}' created"

        for n_key, node in item.nodes.items():
            node["_key"] = n_key
            new_node = Node(user_graph=ug._key, **node)
            self.db.add(new_node)
            log.debug(f"New node: {new_node}")

        for e_key, edge in item.edges.items():
            e_from = Node.__collection__ + "/" + edge["source"]
            e_to = Node.__collection__ + "/" + edge["target"]

            del edge["source"]
            del edge["target"]

            if "_key" in edge:
                del edge["_key"]

            new_link = Link(_key=e_key, _from=e_from, _to=e_to, user_graph=ug._key, **edge)
            self.db.add(new_link)
            log.debug(f"New link: {new_link}")

        return ret_msg


@cbv(router)
class ItemsAPI:
    """Class based API for managing and querying items (nodes/edges)."""

    request: Request

    db: Database = Depends(get_db)

    ITEMS_API_PATH = API_BASE + "items"

    @router.get(ITEMS_API_PATH + "/{item_key}")
    def get_item(self, item_key: str) -> NodeResponseSchema:

        item: Node = self.db.query(Node).by_key(item_key)
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


        general_graph = GeneralGraph(connection=self.db)
        general_graph.expand(item)
        node_manager = NodeManager(self.db)
        n_dict = node_manager.post_process(item)


        # link_recs: list[Link] = self.db.query(Link).filter_by(user_graph=ug._key).all()
        # edges = {}
        # for l_rec in link_recs:
        #     edges[l_rec._key] = node_manager.post_process(l_rec)

        # ret = GraphSchema(graph_name=ug.name, layouts=ug.layouts, nodes=nodes, edges=edges)

        return NodeResponseSchema(**n_dict)


class NodeTypesAPI(CRUDAPIBase):
    response_schema = NodeType
    MODEL = NodeType
    log = logging.getLogger("NodeTypesAPI")


node_type_api_router = ViewRouter(prefix="/api/node-types")
node_type_api_router.register_view(NodeTypesAPI)
