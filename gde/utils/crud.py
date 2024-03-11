"""CRUD API base class for arango models."""

import logging

from fastapi import Depends, Request, HTTPException, status
from fastapi_views.views.api import APIView
from fastapi_views.views.functools import get, post, patch, put, delete

from arango_orm import Database, Collection
from arango_orm.exceptions import DocumentNotFoundError


from ..db import get_db


log = logging.getLogger(__name__)

# router = InferringRouter()


# @cbv(router)
class CRUDAPIBase(APIView):
    """Class based API for managing user graphs."""

    log: logging.Logger | None = None
    MODEL: Collection | None = None

    @get("")
    def list(self, db: Database = Depends(get_db)) -> list[dict]:
        "List records"
        ret = []
        q = db.query(self.MODEL)
        recs = q.all()

        for r in recs:
            ret.append(r.model_dump(mode='json', by_alias=True))

        return ret

    @post("", status_code=status.HTTP_201_CREATED)
    def add(self, item: dict, db: Database = Depends(get_db)):
        rec = self.MODEL(**item)
        db.add(rec)

    @get("<item_id>")
    def get_item(self, item_id, db: Database = Depends(get_db)) -> dict:
        rec = db.query(self.MODEL).by_key(item_id)
        return rec

    @delete("<item_id>")
    def delete_item(self, item_id, db: Database = Depends(get_db)):
        rec = db.query(self.MODEL).by_key(item_id)
        db.delete(rec)


    # @router.get(API_BASE_PATH + "/{graph_key}")
    # def get_user_graph(self, graph_key: str) -> GraphSchema:
    #     ug: UserGraph = self.db.query(UserGraph).by_key(graph_key)
    #     node_manager = NodeManager(self.db)

    #     node_recs: list[Node] = self.db.query(Node).filter_by(user_graph=ug._key).all()
    #     nodes = {}

    #     for n_rec in node_recs:
    #         nodes[n_rec._key] = node_manager.post_process(n_rec)

    #     link_recs: list[Link] = self.db.query(Link).filter_by(user_graph=ug._key).all()
    #     edges = {}
    #     for l_rec in link_recs:
    #         edges[l_rec._key] = node_manager.post_process(l_rec)

    #     ret = GraphSchema(graph_name=ug.name, layouts=ug.layouts, nodes=nodes, edges=edges)

    #     return ret

    # @router.post(API_PATH)
    # def save_graph(self, item: GraphSchema) -> str:

    #     log.debug(item)
    #     ug = self.db.query(UserGraph).filter_by(_key=item.graph_key).first()
    #     # if ug is not None:
    #     #     raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Already exists")

    #     if ug:
    #         ug.layouts = item.layouts
    #         self.db.update(ug)
    #         self.db.query(Node).filter_by(user_graph=ug._key).delete()
    #         self.db.query(Link).filter_by(user_graph=ug._key).delete()
    #         ret_msg = f"Graph '{ug._key}' updated"
    #     else:
    #         ug = UserGraph(_key=item.graph_key, name=item.graph_name, layouts=item.layouts)
    #         self.db.add(ug)
    #         ret_msg = f"Graph '{ug._key}' created"

    #     for n_key, node in item.nodes.items():
    #         node['_key'] = n_key
    #         new_node = Node(user_graph=ug._key, **node)
    #         self.db.add(new_node)
    #         log.debug(f"New node: {new_node}")

    #     for e_key, edge in item.edges.items():
    #         e_from = Node.__collection__ + '/' + edge['source']
    #         e_to = Node.__collection__ + '/' + edge['target']

    #         del edge['source']
    #         del edge['target']

    #         if '_key' in edge:
    #             del edge['_key']

    #         new_link = Link(_key=e_key, _from=e_from, _to=e_to, user_graph=ug._key, **edge)
    #         self.db.add(new_link)
    #         log.debug(f"New link: {new_link}")

    #     return ret_msg
