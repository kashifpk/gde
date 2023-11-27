"Database management commands."

import typer
from rich import print

from ..db import get_db
from ..db.models import GeneralGraph, Setting, UserGraph
app = typer.Typer()


@app.command()
def init():
    "Initialize database (create tables etc)"
    db = get_db()
    db.create_all([Setting, UserGraph, GeneralGraph])
    print("[green]Database initialization done.[/green]")
