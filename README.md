# Graph Data Explorer

- Create and explore data graphs.
- Execute workflows (from workflow-executor) to populate graph data


## Node Types

There are two types of node-types.

1. For creating graph data items, e.g, Person. These are defined as JSON in arango (or later through GDE interface) and allow to add fields according to node type when creating node/edge objects.
2. Second type of NodeType objects are used inside the code too (like in Workflow-Explorer) and their database entry contains a reference to the node schema so the UI can display proper fields and code can work with pydantic/Arango models.

