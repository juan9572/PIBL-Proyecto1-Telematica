import socket
import threading
import cache

round_counter = -1

def round_robin(size):
    global round_counter
    round_counter = (
        0 if round_counter == size - 1 
        else round_counter + 1
    )
    return round_counter

class ConexionCliente(threading.Thread):

    def log(self, line):
        with open("log.txt", "a") as f:
            f.write(line + "\n")
        return print(line)

    def __init__(self, ip_cliente, socket_cliente, params):
        threading.Thread.__init__(self, name=f"CL-{ip_cliente}")
        self.socket_cliente = socket_cliente
        self.ip_cliente = ip_cliente
        self.params = params
        self.log(f"-------------------NUEVA CONEXION------------------- {ip_cliente}")

    def app_connection(self, request, ip, puerto):
        response = ""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as aplicacion:
            aplicacion.connect((ip, puerto))
            aplicacion.send(request)
            data = aplicacion.recv(self.params["buff_size"])
            response = data
            aplicacion.close()
        return response

    def run(self):
        request = ""
        while True:
            data = self.socket_cliente.recv(self.params["buff_size"])
            request = data
            if request.decode("utf-8") == "QUIT":
                break
            parseRequest = request.decode("utf-8")
            if parseRequest:
                cache.check_registers_cache("cache.txt", self.params)
                request_line = parseRequest[:parseRequest.index('\n') - 1]    
                if request_line in cache.cache.keys():
                    response = cache.cache[request_line][1]
                else:
                    index = round_robin(len(self.params["servers"]))
                    ip, puerto = self.params["servers"][index]
                    self.log(f"REQUEST FORWARDED TO SERVER {index + 1}: {ip}:{puerto}")
                    response = self.app_connection(request, ip, int(puerto))
                    cache.add_cache(request_line, response, self.params)
                self.socket_cliente.sendall(response)
                self.log(f"* RESPONSE {self.ip_cliente}* {response}")
                f"-------------------FINALIZO CONEXION------------------- {self.ip_cliente}"
        self.socket_cliente.close()
        return
