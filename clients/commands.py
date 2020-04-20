import click

from clients.services import ClientService
from clients.models import Client


# Va a servir para definir al cual van a pertenecer las otras funciones
@click.group()
def clients():
    """Manages the clients lifecycle"""
    pass


@clients.command()
# "-n", "--name" --> patrón de abreviación, name ahora se representará como n
# type=str --> El tipo al que deseamos convertir la entrada del usuario
# prompt=True --> Le decimos a click que si no nos lo da vía al patrón abreviado dentro del comando,
#   queremos pedírselo al usuario
# help --> línea de ayuda
@click.option("-n", "--name",
              type=str,
              prompt=True,
              help="The client name")
@click.option("-c", "--company",
              type=str,
              prompt=True,
              help="The client company")
@click.option("-e", "--email",
              type=str,
              prompt=True,
              help="The client email")
@click.option("-p", "--position",
              type=str,
              prompt=True,
              help="The client position")
@click.pass_context
def create(ctx, name, company, email, position):
    """Creates a new client"""
    client = Client(name, company, email, position)
    client_service = ClientService(ctx.obj["clients_table"])

    client_service.create_client(client)


@clients.command()
@click.pass_context
def list(ctx):
    """List all clients"""
    client_service = ClientService(ctx.obj["clients_table"])
    # click.echo = print --> solo que se usa click.echo porque el comportamiento de print varia a lo largo de
    # diferentes sistemas operativos, entonces al usar click.echo garantizamos que la forma que imprimimos en
    # conola es igual en todos los sistemas operativos
    click.echo("  ID  |  NAME  |  COMPANY  |  EMAIL  |  POSITION")
    click.echo("*"*100)

    clients_list = client_service.list_clients()

    for client in clients_list:
        click.echo("{uid} | {name} | {company} | {email} | {position}".format(
            uid=client["uid"],
            name=client["name"],
            company=client["company"],
            email=client["email"],
            position=client["position"]
        ))


@clients.command()
@click.argument("client_uid",
                type=str)
@click.pass_context
def update(ctx, client_uid):
    """Updates a client"""
    client_service = ClientService(ctx.obj["clients_table"])
    client_list = client_service.list_clients()

    client = [client for client in client_list if client["uid"] == client_uid]

    if client:
        client = _update_client_flow(Client(**client[0]))
        client_service.update_clients(client)

        click.echo("Client updated")
    else:
        click.echo("Client not found")


def _update_client_flow(client):
    click.echo("Leave empty if you dont want to modify the value")

    client.name = click.prompt("New name", type=str, default=client.name)
    client.company = click.prompt("New company", type=str, default=client.company)
    client.email = click.prompt("New email", type=str, default=client.email)
    client.position = click.prompt("New position", type=str, default=client.position)

    return client


@clients.command()
@click.argument("client_uid",
                type=str)
@click.pass_context
def delete(ctx, client_uid):
    """Deletes a client"""
    client_service = ClientService(ctx.obj["clients_table"])
    client_list = client_service.list_clients()

    client = [client for client in client_list if client["uid"] == client_uid]

    if client:
        client_service.delete_client(client_uid)

        click.echo("Client deleted")
    else:
        click.echo("Client not found")


# Generamos un alias para que sea facil declarar todas estas funciones en un solo go
all = clients
