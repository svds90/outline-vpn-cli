import click
from modules.server_json_manager import JSONManager

server_manager = JSONManager()


@click.command()
@click.argument('list')
def get_srv(list):
    print(server_manager.get_servers())
