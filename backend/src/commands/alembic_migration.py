import click


@click.command()
@click.option("--version", help="Alembic version", type=str)
@click.option("--inifile", help="Alembic config file", type=str)
def alembic_migration(version: str, inifile: str):
    from src.commands.managers.alembic_migration import AlembicMigrationCommandManager

    click.echo("Migration command is started...")

    manager = AlembicMigrationCommandManager(version, inifile)
    manager.run()

    click.echo("Migration command is completed successfully!")


if __name__ == "__main__":
    alembic_migration()
