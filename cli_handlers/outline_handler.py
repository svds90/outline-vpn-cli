import click
from pprint import pprint
from outline.outline_api import OutlineVPN


@click.command()
@click.option('--list', is_flag=False, flag_value='list_all', default='Default')
def get_info(list):
    print(list)
    pprint(vpn.server.server_info())
