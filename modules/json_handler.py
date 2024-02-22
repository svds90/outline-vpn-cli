import json


class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


class JSONHandler(Singleton):
    def __init__(self):
        self.servers_dict = self.load_json()

    def load_json(self) -> dict:

        try:
            with open('servers.json', 'r') as file:
                data = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            data = {}

        return data

    def __update_json(self, updates=None) -> None:

        if updates:
            self.servers_dict.update(updates)

        with open('servers.json', 'w') as file:
            json.dump(self.servers_dict, file, indent=2)

    def add_server(self, id: str, token: str) -> None:

        updates = {str(id): token}
        self.__update_json(updates)

    def rename_server(self, id: str, new_id: str) -> None:

        if id in self.servers_dict:
            outline_api_url = self.servers_dict[id]
            del self.servers_dict[id]
            updates = {new_id: outline_api_url}
            self.__update_json(updates)

    def delete_server(self, id: str):

        if id in self.servers_dict:
            del self.servers_dict[id]
            self.__update_json()
