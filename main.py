import sys
import csv
import os

# El punto al principio es para que el archivo permanezca oculto (esto solo funciona en mac o linux)
CLIENT_TABLE = ".clients.csv"
CLIENT_SCHEMA = ["name", "company", "email", "position"]
clients = []


def _initialize_clients_from_storage():
    with open(CLIENT_TABLE, mode="r") as file:
        # Fieldnames --> es una lista de las llaves que va a utilizar DictReader para poder construir
        # cada uno de los dicionarios
        reader = csv.DictReader(file, fieldnames=CLIENT_SCHEMA)

        for row in reader:
            clients.append(row)


def _save_clients_to_storage():
    # Tener en cuenta que una vez se abre el archivo, este ya no puede reescribirse, por este motivo se trabaja
    # con una tabla temporal, luego se elimina la original y a la temporal se le cambia el nombre por la original
    tmp_table_name = "{}.tmp".format(CLIENT_TABLE)
    with open(tmp_table_name, mode="w", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=CLIENT_SCHEMA)
        writer.writerows(clients)

    os.remove(CLIENT_TABLE)
    os.rename(tmp_table_name, CLIENT_TABLE)


def create_client(client):
    # para poder usar la variable clients que se encuentra global
    global clients

    if client not in clients:
        clients.append(client)
    else:
        print("Client already is in the client's list")


def update_client(client_id, updated_client):
    global clients

    if _valid_client_id(client_id):
        clients[client_id] = updated_client


def delete_client(client_id):
    global clients

    if _valid_client_id(client_id):
        clients.pop(client_id)


def list_clients():
    print("uid | name | company | email | position")
    for idx, client in enumerate(clients):
        print("{uid} | {name} | {company} | {email} | {position}".format(
            uid=idx,
            name=client["name"],
            company=client["company"],
            email=client["email"],
            position=client["position"]
        ))


def search_client(client_name):
    for client in clients:
        if client["name"] == client_name:
            return True

    return False


def _print_welcome():
    print("WELCOME TO PLATZI SALES")
    print("*" * 50)
    print("What would you like to do today")
    print("[C] Create client")
    print("[L] List clients")
    print("[U] Update client")
    print("[D] Delete client")
    print("[S] Search client")


def _get_client_field(field_name):
    field = None
    while not field:
        field = input("What is the client {}? ".format(field_name))

    return field


def _get_client_name():
    client_name = None

    while not client_name:
        client_name = input("What is the client name? ")
        if client_name.lower() == "exit":
            client_name = None
            break

    if not client_name:
        sys.exit()

    return client_name


def _get_client_from_user():
    return {
        "name": _get_client_field("name"),
        "company": _get_client_field("company"),
        "email": _get_client_field("email"),
        "position": _get_client_field("position")
    }


def _valid_client_id(client_id):
    if (client_id >= len(clients)) or (client_id < 0):
        print("Invalid id for a client")

        return False

    return True


def _client_not_found():
    print("Client is not in clients list")


def run():
    _initialize_clients_from_storage()

    _print_welcome()
    command = input().upper()
    if command == "C":
        client = _get_client_from_user()
        create_client(client)
    elif command == "L":
        list_clients()
    elif command == "U":
        client_id = int(_get_client_field("id"))
        updated_client = _get_client_from_user()
        update_client(client_id, updated_client)
    elif command.upper() == "D":
        client_id = int(_get_client_field("id"))
        delete_client(client_id)
    elif command == "S":
        client_name = _get_client_name()
        found = search_client(client_name)
        if found:
            print("The client is in the client's list")
        else:
            print("The client: {} is not int our client's list".format(client_name))
    else:
        print("Invalid command")

    _save_clients_to_storage()


if __name__ == "__main__":
    run()
