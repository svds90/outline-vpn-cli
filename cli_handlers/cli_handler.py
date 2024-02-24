from modules.server_json_manager import JSONHandler
import click

handler = JSONHandler()


@click.command()
@click.option('--list', help='List JSON file')
def get_srv():
    data = handler.get_servers()
    print(data)


get_srv()
