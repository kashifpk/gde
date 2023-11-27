import typer

from .commands import (
    db as cmd_db
)

app = typer.Typer()
app.add_typer(cmd_db.app, name="db", help="Manage the database")


def main():
    app()
