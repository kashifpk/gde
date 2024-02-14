# TODO

- [x] vite build setup (currently we're just running vite dev server for serving js)
- [x] Update or replace vite-fastapi. It probably doesn't even need to be linked with fastapi. Just some jinja2 template tags etc and reading manifest.json might be fine.

- [x] Node color should be fetched from _meta
- [x] Node editor should use the updated node format with nested _meta
- [x] Node meta/display information to use node type as default
- [x] Fix edit/update mode with node editor
- [x] Generic CRUD API for arango models
  - [x] Node types api and use it
- [x] Fields addition to add node/edge when selecting a node type
- [ ] Icon support for nodes
- [ ] Line color support for edges
- [ ] When updating nodes/edges don't set derived/calculated fields. Like label if it's not present and is fetched from node_type etc then on update it should not be set as a value on the node unless the user actually sets it.
- [ ] Bug: Newly created edges are not editable (error says missing _meta field) until they are saved and loaded back from DB.
- [ ] Node details page (separate window) should show more node details and configurable "n" linkages
- [ ] Bug: Node meta doesn't take affect for newly created/edited nodes. Only works when loaded from DB.
- [ ] Node types management interface