import click

from modules.server_json_manager import JSONManager
from outline.outline_api import OutlineVPN

manager = JSONManager()


def init_outline_api(outline_api_url):
    return OutlineVPN(outline_api_url)


@click.group()
def cli():
    pass


@cli.command(name='get')
@click.option('--server', '-s', 'server_id', required=True, help='Server ID')
@click.option('--key', '-k', 'key_id', required=False, help='Key ID')
@click.option('--keys', 'keys', is_flag=True, help='List all keys')
@click.option('--telemetry', '-t', 'telemetry', is_flag=True, help='Get telemetry status')
@click.option('--metrics', '-m', is_flag=True, help='Get metrics')
def get_command(server_id, key_id, keys, telemetry, metrics):

    outline = init_outline_api(manager.get_server(server_id))

    if server_id and key_id and metrics:
        click.echo(outline.client.get_all_metrics()['bytesTransferredByUserId'][str(key_id)])
    elif server_id and keys and metrics:
        click.echo(outline.client.get_all_metrics())
    elif server_id and keys:
        click.echo(outline.client.get_all_keys())
    elif server_id and key_id:
        outline.client.get_key(key_id)
        click.echo(outline.client.client_info())
    elif server_id and telemetry:
        click.echo(outline.server.get_telemetry_status())
    elif server_id:
        click.echo(outline.server.server_info())


@cli.command(name='set')
@click.option('--server', '-s', 'server_id', required=True, help='Server ID')
@click.option('--hostname', '-h', 'hostname', metavar='NEW HOSTNAME', help='Change hostname')
@click.option('--name', '-n', 'name', metavar='NEW NAME', help='Change name')
@click.option('--port', '-p', 'port', metavar='PORT', help='Change port for new keys')
@click.option('--rename-key', 'id_name', nargs=2, metavar='ID NAME', help='Rename key')
@click.option('--key-data-limit', 'key_limit', nargs=2, metavar='ID BYTES/"OFF"', help='Set limit per key')
@click.option('--global-limit', 'limit', metavar='BYTES/"OFF"', help='Set global data limit')
def set_command(server_id, hostname, name, port, id_name, key_limit, limit):

    outline = init_outline_api(manager.get_server(server_id))

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


@cli.command(name='json')
@click.option('--list', '-l', 'list', is_flag=True, help='Lists servers.json')
@click.option('--get-url', '-g', 'url', metavar='ID', help='Returns server url')
@click.option('--add', '-a', 'add', nargs=2, metavar='ID API_URL', help='Adds server')
@click.option('--name', '-n', 'name', nargs=2, metavar='ID NEW_ID', help='Renames server')
@click.option('--remove', '-r', 'remove', metavar='ID', help='Remove server')
def edit_json(list, url, add, name, remove):
    if list:
        click.echo(manager.get_servers())
    elif url:
        click.echo(manager.get_server(url))
    elif add:
        server_name, key = add
        manager.add_server(server_name, key)
    elif name:
        current_id, new_id = name
        manager.rename_server(current_id, new_id)
    elif remove:
        manager.delete_server(remove)


if __name__ == "__main__":
    cli()
