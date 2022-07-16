# trabalhoderede

Componentes da equipe: Rafael Pereira, Caroline Morais, Jeisiane Macedo, Bruno Junqueira

para rodar o programa primeiro inicie um servidor core:

`python3 core.py --port <porta do core>`

e pelo menos um servidor fs:

`python3 file_server.py --directory <diretorio> --port <porta do fs>`

# após ambos rodando, você pode fazer as requests de client como:

fazer upload determinando o numero de redundancias: 


`python3 client.py upload <ip do core>:<porta do core> --file <nome do arquivo> --redundancy <numero de redundancia>`

Alterar o número de redundancias:

`python3 client.py redundancy <ip do core>:<porta do core> --file <nome do arquivo> --redundancy <numero de redundancia>`

Fazer Download do arquivo:


`python3 client.py download  <ip do core>:<porta do core>  --file <nome do arquivo>`

