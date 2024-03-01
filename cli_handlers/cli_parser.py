import click
from datetime import datetime
from tabulate import tabulate

from modules.server_json_manager import JSONManager
from outline.outline_api import OutlineVPN

metrics_columns = ['ID', 'Transferred data']


def init_outline_api(outline_api_url):
    return OutlineVPN(outline_api_url)


@click.group()
def cli_parser():
    """
    Main group for all click commands
    """
    pass


@cli_parser.command(name='add')
@click.option('--server', '-s', 'server_id', required=True, help='Server ID')
@click.option('--new-key', 'key', is_flag=True, help='Create new key')
def add_command(server_id, key):

    json_handler = JSONManager()
    outline = init_outline_api(json_handler.get_server(server_id))

    if server_id and key:
        outline.client.create_key()


@cli_parser.command(name='del')
@click.option('--server', '-s', 'server_id', required=True, help='Server ID')
@click.option('--remove-key', '-r', 'key_id', metavar='ID', help='Remove key')
def del_command(server_id, key_id):

    json_handler = JSONManager()
    outline = init_outline_api(json_handler.get_server(server_id))

    if server_id and key_id:
        outline.client.delete_key(str(key_id))


@cli_parser.command(name='get')
@click.option('--server', '-s', 'server_id', required=True, help='Server ID')
@click.option('--key', '-k', 'key_id', required=False, help='Key ID')
@click.option('--keys', 'keys', is_flag=True, help='List all keys')
@click.option('--telemetry', '-t', 'telemetry', is_flag=True, help='Get telemetry status')
@click.option('--metrics', '-m', is_flag=True, help='Get metrics')
def get_command(server_id, key_id, keys, telemetry, metrics):

    json_handler = JSONManager()
    outline = init_outline_api(json_handler.get_server(server_id))

    if server_id and key_id and metrics:
        res = outline.client.get_all_metrics()['bytesTransferredByUserId'][str(key_id)]
        _dict = {f"{key_id}": f"{round(res / (1000 ** 3), 2)}"}
        click.echo(tabulate(_dict.items(), headers=metrics_columns, tablefmt='rst'))

    elif server_id and keys and metrics:
        click.echo(tabulate(bytes_to_gb(outline.client.get_all_metrics()[
                   'bytesTransferredByUserId'].items()).items(), headers=metrics_columns, tablefmt='rst'))

    elif server_id and keys:
        res = outline.client.get_all_keys()['accessKeys']

        for item in res:
            click.echo(f"\n{tabulate(item.items(), tablefmt='plain')}")

    elif server_id and key_id:
        outline.client.get_key(key_id)
        click.echo(f"\n{tabulate(outline.client.client_info().items(), tablefmt='plain')}")

    elif server_id and telemetry:
        status = outline.server.get_telemetry_status()

        if status:
            click.echo(tabulate(dict(Telemetry='ENABLED').items(), tablefmt='rst'))
        elif not status:
            click.echo(tabulate(dict(Telemetry='DISABLED').items(), tablefmt='rst'))

    elif server_id:
        click.echo(tabulate(timestamp_to_date(outline.server.server_info()).items(), tablefmt='rst'))


@cli_parser.command(name='set')
@click.option('--server', '-s', 'server_id', required=True, help='Server ID')
@click.option('--hostname', '-h', 'hostname', metavar='NEW HOSTNAME', help='Change hostname')
@click.option('--name', '-n', 'name', metavar='NEW NAME', help='Change name')
@click.option('--port', '-p', 'port', metavar='PORT', help='Change port for new keys')
@click.option('--rename-key', 'id_name', nargs=2, metavar='ID NAME', help='Rename key')
@click.option('--key-data-limit', 'key_limit', nargs=2, metavar='ID BYTES/"OFF"', help='Set limit per key')
@click.option('--global-limit', 'limit', metavar='BYTES/"OFF"', help='Set global data limit')
def set_command(server_id, hostname, name, port, id_name, key_limit, limit):

    json_handler = JSONManager()
    outline = init_outline_api(json_handler.get_server(server_id))

    if server_id and name:
        outline.server.rename_server(name)
    elif server_id and port:
        outline.server.change_default_port(int(port))
    elif server_id and hostname:
        outline.server.change_hostname(hostname)
    elif server_id and id_name:
        str_id, new_name = [str(i) for i in id_name]
        outline.client.rename_key(str_id, new_name)
    elif server_id and key_limit:
        key_id, data_limit = key_limit

        if data_limit == 'off':
            outline.client.disable_data_limit(key_id)
        else:
            outline.client.set_data_limit(key_id, int(data_limit))

    elif server_id and limit:

        if limit == 'off':
            outline.server.disable_global_data_limit()
        else:
            outline.server.set_global_data_limit(int(limit))


@cli_parser.command(name='json')
@click.option('--list', '-l', 'list', is_flag=True, help='Lists servers.json')
@click.option('--get-url', '-g', 'url', metavar='ID', help='Returns server url')
@click.option('--add', '-a', 'add', nargs=2, metavar='ID API_URL', help='Adds server')
@click.option('--name', '-n', 'name', nargs=2, metavar='ID NEW_ID', help='Renames server')
@click.option('--remove', '-r', 'remove', metavar='ID', help='Remove server')
def edit_json(list, url, add, name, remove):
    json_handler = JSONManager()

    if list:
        click.echo(tabulate(json_handler.get_servers().items(), tablefmt='rst'))
    elif url:
        click.echo(json_handler.get_server(url))
    elif add:
        server_name, key = add
        json_handler.add_server(server_name, key)
    elif name:
        current_id, new_id = name
        json_handler.rename_server(current_id, new_id)
    elif remove:
        json_handler.delete_server(remove)


def bytes_to_gb(data_dict):

    data_in_gb = {}
    for key, value in data_dict:
        value = str(round(value / (1000 ** 3), 2))
        data_in_gb[key] = value
    return data_in_gb


def timestamp_to_date(server_info: dict) -> dict:
    updates = server_info

    updates['created_time'] = f"{datetime.fromtimestamp(
        updates['created_time'] / 1000).strftime("%d %B %Y, %I:%M:%S %p")}"

    return updates
