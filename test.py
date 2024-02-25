import click

from modules.server_json_manager import JSONManager

sm = JSONManager()


@click.group()
def cli():
    pass


@click.command()
@click.option('--list', '-l', 'server_id', help='Lists servers from servers.json')
def get_info(server_id):
    if server_id != 'all':
        click.echo(sm.get_server(server_id))
    else:
        click.echo(sm.get_servers())


@click.command()
@click.option('--add', '-a', 'new_server', nargs=2, help='Adds new server to servers.json')
def add_json(new_server):
    if new_server:
        idn, token = [str(i) for i in new_server]
        sm.add_server(idn, token)



def main():



if __name__ == "__main__":
    main()
