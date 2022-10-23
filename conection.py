import socket
import threading

class ConexionCliente(threading.Thread):

    round_counter = -1

    def round_robin(self):
        self.round_counter = (
            0 if self.round_counter == len(self.params["servers"]) - 1 
            else self.round_counter + 1
        )
        return self.round_counter

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
        index = self.round_robin()
        while True:
            data = self.socket_cliente.recv(self.params["buff_size"])
            request = data
            ip, puerto = self.params["servers"][index]
            self.log(f"REQUEST FORWARDED TO SERVER {index+1}: {ip}:{puerto}")
            response = self.app_connection(request, ip, int(puerto))
            self.socket_cliente.sendall(response)
            self.log(f"* RESPONSE {self.ip_cliente}* {response}")
            if request == "QUIT": #Esto esta mas malo que un hpta
                break
        self.log(
            f"-------------------FINALIZO CONEXION------------------- {self.ip_cliente}"
        )
        self.socket_cliente.close()
        return
