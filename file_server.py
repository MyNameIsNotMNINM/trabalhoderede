from urllib import response
from common.arguments import get_arguments
from common.file import delete_file, get_file, save_file
from softp.common import Address
from softp.server import Request, Response, Server


server: Server= None
directory: str = './core'

def setup_server(ip: str, port: int):
    global server
    try:
        server = Server(Address(ip, port))
        setup_server_actions()
    except BaseException as e:
        #do something later, not just throw the same error pls
        raise e


def on_upload(req: Request, res: Response):
    attr = req.header.attributes
    print(attr['name'])
    res.respond({'action': 'ok'}, b'')
    save_file(directory, attr['name'],  '', req.data)
    # pass

def on_download(req: Request, res: Response):
    file = get_file(directory, req.header.attributes['name'])
    res.respond({'action': 'upload', 'content-length': file.content_length, 'hash': file.hash, 'name': file.name}, file.content )

def on_delete(req: Request, res: Response):
    delete_file(directory, req.header.attributes['name'])
    res.respond({'action': 'ok'}, b'')
def setup_server_actions():
    server.setOnAction('upload', on_upload)
    server.setOnAction('download', on_download)
    server.setOnAction('delete', on_delete)

def main():
    global directory
    args = get_arguments()
    p = 4444#CONFIG.PORT
    if hasattr(args, 'port') and args.port is not None:
        p = int(args.port)
    if hasattr(args, 'directory') and args.directory is not None:
        directory = args.directory
    setup_server(ip='', port=p)
    server.run()

if __name__ == '__main__':
    main()


