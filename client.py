from common.arguments import get_arguments
from common.file import File, save_file
from softp.client import Client
from softp.common import Address

def send_to_server(server: dict, header: dict, data: bytes):
    c = Client()
    c.send(Address(server['address'], server['port']), header, data)
    return c.response

def upload_file(file_path: str):
    file = File(file_path)
    send_to_server({'address': '127.0.0.1', 'port': 3042}, {'action': 'upload', 'content-length': file.content_length, 'hash': file.hash, 'name': file.name, 'redundancy': '2'}, file.content)

def download_file():
    r= send_to_server({'address': '127.0.0.1', 'port': 3042}, {'action': 'download', 'name': 'gato.webp'}, b'')
    save_file('', r.header.attributes['name'], '', r.content)

def change_redundancy():
    r= send_to_server({'address': '127.0.0.1', 'port': 3042}, {'action': 'change_redundancy', 'redundancy' : '3', 'name': 'gato.webp'}, b'')
    

upload_file('gato.webp')
change_redundancy()

# download_file()