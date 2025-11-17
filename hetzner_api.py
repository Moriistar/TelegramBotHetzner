import requests
import json

class HetznerAPI:
    def __init__(self, token):
        self.token = token
        self.url = "https://api.hetzner.cloud/v1/"
        self.headers = {
            "Authorization": f"Bearer {self.token}"
        }

    def create_server(self, name, server_type="cx11", image="ubuntu-22.04", location="hel1"):
        data = {
            "name": name,
            "server_type": server_type,
            "image": image,
            "location": location
        }
        response = requests.post(self.url + "servers", headers=self.headers, json=data)
        return response.json()

    def delete_server(self, server_id):
        response = requests.delete(self.url + f"servers/{server_id}", headers=self.headers)
        return response.json()

    def reboot_server(self, server_id):
        data = {"type": "reboot"}
        response = requests.post(self.url + f"servers/{server_id}/actions", headers=self.headers, json=data)
        return response.json()

    def rebuild_server(self, server_id, image="ubuntu-22.04"):
        data = {"type": "rebuild", "image": image}
        response = requests.post(self.url + f"servers/{server_id}/actions", headers=self.headers, json=data)
        return response.json()

    def list_servers(self):
        response = requests.get(self.url + "servers", headers=self.headers)
        return response.json()
