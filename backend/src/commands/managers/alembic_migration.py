import click
from alembic import command
from alembic.config import Config


class AlembicMigrationCommandManager:
    def __init__(self, version: str, inifile: str):
        self.version = version
        self.inifile = inifile

    def run(self):
        alembic_cfg = Config(self.inifile)
        command.stamp(alembic_cfg, self.version, purge=True)
        click.echo(f"Migration version {self.version} has been set")
