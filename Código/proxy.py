import socket
from cache import start_cache
from conection import ConexionCliente

params = {}

def setup(file):
    global params
    try:
        with open(file) as conf:
            for line in conf:
                if line.startswith("PUERTO"):
                    p = line[line.index("=") + 1 :]
                    params["puerto"] = int(p)
                elif line.startswith("HOST"):
                    p = line[line.index("=") + 1 : -1]
                    params["host"] = p
                elif line.startswith("SERVERS"):
                    p = line[line.index("=") + 1 : -1].replace(" ", "").split(",")
                    for i in range(0, len(p)):
                        p[i] = tuple(map(str, p[i].split(":")))
                    params["servers"] = p
                elif line.startswith("BUFF_SIZE"):
                    p = line[line.index("=") + 1 :]
                    params["buff_size"] = int(p)
                elif line.startswith("TTL"):
                    p = line[line.index("=") + 1 :]
                    params["ttl"] = float(p)
        return True, params
    except:
        return False, params

def start_server():
    check, params = setup("serv.config")
    start_cache("cache.txt", params)
    if check:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
            servidor.bind((params["host"], params["puerto"]))
            servidor.listen(5)
            print("Servidor listo y esperando")
            while True:
                socketcliente, dircliente = servidor.accept()
                thread_cliente = ConexionCliente(dircliente, socketcliente, params)
                thread_cliente.start()
    else:
        print("Por favor ingrese un archivo de configuracion")
