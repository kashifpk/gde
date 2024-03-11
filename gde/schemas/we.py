"Workflow Executor related schemas"


from typing import Literal, Any
from enum import Enum
from uuid import UUID

from pydantic import BaseModel

from datetime import datetime


# TODO: See if graph_info and tasks can be a single model, if not, it's ok too.
# Perhaps having them separate would be fine? As for graph_info we can ask for input and config before
# executing the workflow
# May be rename these? GraphInfo = WorkflowInfo, etc.

class GraphInfo(BaseModel):
    name: str
    description: str = ""
    input: dict = {}
    output: dict = {}
    config: dict = {}


class Task(BaseModel):
    _schema_extra = {'executor': {'choices': ['python', 'os', 'subgraph']}}

    name: str
    executor: Literal['python', 'os', 'subgraph']
    call: str
    execute_async: bool = False
    plugins: dict = {}
    config: dict = {}
    input: dict = {}
    publish: dict = {}


class Transition(BaseModel):
    label: str | None = None
    condition: str | None = None


class UserTask(BaseModel):
    name: str
    label: str | None = None
    user_id: str | None = None
    task_graph_name: str
    config: dict = {}
    input: dict = {}

    # task_graph = relationship(GraphInfo, "task_graph_name", cache=False)


class ExecutionStart(BaseModel):
    id: UUID
    label: str | None = None
    graph_name: str
    start_execution_id: str | None = None  # in case of subgraphs
    user_task_id: str
    timestamp: datetime
    state: str | None = None
    finished_timestamp: datetime | None = None
    input: dict = {}
    result: dict = {}
    context: dict = {}
    config: dict = {}

    # task_graph = relationship(GraphInfo, "graph_name", cache=False)


class Execution(BaseModel):
    id: UUID
    label: str | None = None
    timestamp: datetime
    start_execution_id: str
    graph_step_name: str
    executor: str
    execute_async: bool
    plugins: dict = {}
    call: str
    input: dict = {}
    state: str | None = None
    status: str | None = None
    result: Any | None = None
    errors: str | None = None

    # start_node = relationship(ExecutionStart, "start_execution_id", cache=False)


class Next(BaseModel):
    condition: str | None = None
    label: str | None = None
