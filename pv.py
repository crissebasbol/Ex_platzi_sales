import click
from clients import commands as clients_commands


CLIENTS_TABLE = ".clients.csv"

# definimos punto de entrada
# para definir punto de entrada
# dar un obejeto contecto
@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = {"clients_table": CLIENTS_TABLE}


cli.add_command(clients_commands.all)
