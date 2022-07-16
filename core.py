from softp.client import Client
from softp.common import Address
from softp.server import Request, Response, Server
import argparse

def get_arguments():
    # create parser object
    parser = argparse.ArgumentParser(description = "Manage the SOFTP Core Server")
    parser.add_argument("-p", "--port", action = 'store',
                    help = "Starts server with the selected port.") 
    args = parser.parse_args()
    return args

server: Server= None
file_servers: list= [{'address': '127.0.0.1', 'port': 4444},{'address': '127.0.0.1', 'port': 3030}, {'address': '127.0.0.1', 'port': 3031}]
files: dict = {}
def setup_server(ip: str, port: int):
    global server
    try:
        server = Server(Address(ip, port))
        setup_server_actions()
    except BaseException as e:
        #do something later, not just throw the same error pls
        raise e

def get_best_servers(amount: int):
    if(amount > len(file_servers)):
        raise Exception("Not enough file servers!")
    return file_servers[:amount]

def add_server_to_file(hash: str, server = str):
    if hash not in files:
        files[hash] = []
    files[hash].append(server)
    print("file added to list")
    print(files)

def send_to_server(server: dict, header: dict, data: bytes):
    c = Client()
    c.send(Address(server['address'], int(server['port'])), header, data)
    return c.response

def get_server_that_has_file(name):
    if (name not in files) or len(files[name]) == 0:
        return None
    return files[name][0]







def on_upload(req: Request, res: Response):
    redundancy= int(req.header.attributes['redundancy'])
    servers = get_best_servers(redundancy)
    res.respond({'action': 'ok'}, b'')
    for fs in servers:
        awnser = send_to_server(fs, req.header.attributes, req.data)
        if(awnser.header.attributes['action'] == 'ok'):
            add_server_to_file(req.header.attributes['name'], fs)

    return

def download_file(name: str):
    server = get_server_that_has_file(name)
    if (server == None):
        return None
    print(server)
    awnser = send_to_server(server, {'action': 'download', 'name': name}, b'')
    return awnser

def on_download(req: Request, res: Response):
    awnser = download_file(req.header.attributes['name'])
    header = awnser.header.attributes.copy()
    header['action']= 'ok'
    res.respond(header_parameters=header, data= awnser.content)
    pass

def change_redundancy(req: Request, res: Response):
    new_redundancy = int(req.header.attributes["redundancy"])
    name = req.header.attributes['name']
    redundancy_diff = len(files[name]) - new_redundancy
    print('redund: ', redundancy_diff)
    if redundancy_diff > 0:
        for i in range(redundancy_diff):
            server = files[name].pop()
            header = req.header.attributes.copy()
            header['action']= 'delete'
            awnser = send_to_server(server, header, req.data)
    elif redundancy_diff == 0:
        pass
    else:
        if redundancy_diff > len(file_servers):
            res.respond({'action': 'bad'})
            return
        
        filePacket = download_file(req.header.attributes['name'])
        servers_that_doesnt_have_file = []
        for fs in file_servers:
            if fs not in files[name]:
                servers_that_doesnt_have_file.append(fs)
            if len(servers_that_doesnt_have_file) >= redundancy_diff:
                continue
        for fs in servers_that_doesnt_have_file:
            header = req.header.attributes.copy()
            header['action'] = 'upload'
            header['content-length'] = filePacket.header.attributes['content-length']
            awnser = send_to_server(fs, header, filePacket.content)
            if(awnser.header.attributes['action'] == 'ok'):
                add_server_to_file(name, fs)

    res.respond({'action': 'ok'}, b'')

def delete(req: Request, res: Response):
   for s_id in files['name']:
        header = req.header.attributes.copy()
        header['name'] = 'delete'
        awnser = send_to_server(file_servers[s_id], header, req.data) 
        files[hash].pop()

def setup_server_actions():
    server.setOnAction('upload', on_upload)
    server.setOnAction('download', on_download)
    server.setOnAction('change_redundancy', change_redundancy)
    server.setOnAction('delete', delete)
    # server.setOnAction('ls', lambda e : e)

def main():
    args = get_arguments()
    p = 3042#CONFIG.PORT
    if hasattr(args, 'port') and args.port is not None:
        p = int(args.port)

    setup_server(ip='', port=p)
    server.run()

if __name__ == '__main__':
    main()



