from common.file import File, save_file
from softp.client import Client
from softp.common import Address
import argparse

def get_arguments():
    # create parser object
    parser = argparse.ArgumentParser(description = "Manage the SOFTP Core Server")

    parser.add_argument("action", nargs="?")
    parser.add_argument("address", action = 'store',
                        help = "Core server address")
    parser.add_argument("-f", "--file", action = 'store',
                        help = "file path")
    parser.add_argument('-r', '--redundancy', action= 'store',
                        help = 'N of redundancies')
    args = parser.parse_args()
    return args

def send_to_server(server: dict, header: dict, data: bytes):
    c = Client()
    c.send(Address(server['address'], server['port']), header, data)
    return c.response

def upload_file(addr: dict, file_path: str, redund: int):
    file = File(file_path)
    send_to_server(addr, {'action': 'upload', 'content-length': file.content_length, 'hash': file.hash, 'name': file.name, 'redundancy': str(redund)}, file.content)

def download_file(addr: dict, file_name: str):
    r = send_to_server(addr, {'action': 'download', 'name': file_name}, b'')
    save_file('', r.header.attributes['name'], '', r.content)

def change_redundancy(addr: dict, file_name: str, redund: int):
    r = send_to_server(addr, {'action': 'change_redundancy', 'redundancy' : redund, 'name': file_name}, b'')


def get_address(ip: str):
    addr = ip.split(':',2)
    return {'address': addr[0], 'port': int(addr[1])}

def main():
    global directory
    args = get_arguments()
    p = 3042#CONFIG.PORT
    if not hasattr(args, 'action') or args.action is None:
        print("command should have action!")
        return
    if not hasattr(args, 'address') or args.address is None:
        print("command should have address!")
        return
    if not hasattr(args, 'file') or args.file is None:
        print("command should have file!")
        return
    
    if(args.action == "upload"):
        upload_file(get_address(args.address), args.file, args.redundancy)
    if(args.action == "download"):
        download_file(get_address(args.address), args.file)
    if(args.action == "redundancy"):
        change_redundancy(get_address(args.address), args.file, args.redundancy)

    

if __name__ == '__main__':
    main()