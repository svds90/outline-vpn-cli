import json
from typing import Optional


class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


class JSONHandler(Singleton):
    """
    Provides an interface for working with server data stored in the servers.json file.
    """

    def __init__(self):
        self.servers_dict = self.__load_json()

    def __load_json(self) -> dict:
        """
        Loads server data from the servers.json file and returns it as a dictionary.
        """
        try:
            with open('servers.json', 'r') as file:
                data = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            data = {}

        return data

    def __update_json(self, updates=None) -> None:
        """
        Updates server data in the servers.json file.
        """
        if updates:
            self.servers_dict.update(updates)

        with open('servers.json', 'w') as file:
            json.dump(self.servers_dict, file, indent=2)

    def get_servers(self) -> dict:
        """
        Returns all servers.
        """
        return self.servers_dict

    def get_server(self, id: str) -> Optional[dict]:
        """
        Returns server with the specified identifier.
        """
        if id in self.servers_dict:
            return self.servers_dict[id]
        else:
            return None

    def add_server(self, id: str, token: str) -> None:
        """
        Adds new server.
        """
        updates = {str(id): token}
        self.__update_json(updates)

    def rename_server(self, id: str, new_id: str) -> None:
        """
        Renames the server with th specified id.
        """
        if id in self.servers_dict:
            outline_api_url = self.servers_dict[id]
            del self.servers_dict[id]
            updates = {new_id: outline_api_url}
            self.__update_json(updates)

    def delete_server(self, id: str) -> None:
        """
        Deletes the server with th specified id.
        """
        if id in self.servers_dict:
            del self.servers_dict[id]
            self.__update_json()
