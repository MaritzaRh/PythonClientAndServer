import socket
import sys
from socketserver import TCPServer

from dictionary import Dictionary
import cgi

class HTTPServer:

    def __init__(self, host='127.0.0.1', port=5005):
        self.host = host
        self.port = port

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen(1)

        print("Listening at", s.getsockname())

        while True:
            conn, addr = s.accept()
            print("Connected by", addr)
            data = conn.recv(8000)

            response = self.handle_request(data)
            print(response.decode())
            conn.sendall(response)
            conn.close()

    # Revisa que tipo de petición es y manda los datos a la correspondiente para regresar el contenido de respuesta
    # convertido a bytes
    def handle_request(self, data):
        dictionary = Dictionary()

        req_dictionary = dictionary.parseInfo(data.decode())

        if req_dictionary['Method'] == 'GET':
            response = self.get(req_dictionary)
        elif req_dictionary['Method'] == 'POST':
            response = self.post(req_dictionary)
        else:
            return b"".join(self.error(req_dictionary['Version'], 501))
        print(req_dictionary)
        return b"".join(response)

    # Se encarga de la tupla de respuesta, viendo si los encabezados estan completos y si el contenido existe
    # para poder regresar una tupla ya sea con el contenido pedido o con un error indicado
    def get(self, req_dictionary):
        try:
            response = (
                self.str2b(req_dictionary['Version']) + b" 200 OK\r\n",  # response line
                #b"Cache-Control:" + self.str2b(req_dictionary['Cache-Control']) + b"\r\n",  # response line
                b"Content-Type: text/html; charset=utf-8\r\n",
                b"Connection:" + self.str2b(req_dictionary['Connection']) + b"\r\n",  # response line
            )
        except KeyError:
            return self.error(req_dictionary['Version'], 404)

        if len(req_dictionary['params']) > 0:
            if "message" in req_dictionary['params']:
                msg = req_dictionary['params']['message']
                response += (b"Content-Length: " + self.int2b(len(msg)) + b"\r\n",)  # response line
                response += (b'\r\n',)  # blank line)
                response += (self.str2b(msg),)  # response body)
        elif "." in req_dictionary['Url']:
            filextension = req_dictionary['Url'].split(".")
            file = './' + filextension[1] + req_dictionary['Url']

            try:
                f = open(file, "r").read()
                response += (b"Content-Length: " + self.int2b(len(f)) + b"\r\n",)  # response line
                response += (b'\r\n',)  # blank line)
                response += (self.str2b(f),)  # response body)
            except IOError:
                return self.error(req_dictionary['Version'], 404)
        else:
            return self.error(req_dictionary['Version'], 404)

        return response

    def post(self,req_dictionary):
        data = req_dictionary.split("\r\n")
        requestType = data[0].split(" ")

        newDictionary = {
            'Method': requestType[0],
            'Url': requestType[1],
            'Version': requestType[2]
        }

        for x in range(1, len(data)):
            separated = data[x].split(":")
            if len(separated) == 2:
                newDictionary.update({separated[0]: separated[1]})
            message = data[len(data) - 1].split("=")

        # Create instance of FieldStorage
        form = cgi.FieldStorage()

        # Get data from fields
        params = {
            'First name': form.getvalue('fname'),
            'Last name': form.getvalue('lname')
        }
        requestDictionary.update({'params': params})
        return (json.dumps(requestDictionary, indent=4))

    # Convierte str a byte
    def str2b(self, data):
        return bytes(data, 'utf-8')

    # Convierte int a byte
    def int2b(self, data):
        return self.str2b(str(data))

    def error(self, version, code):
        status_codes = {
            404: b'Not Found\r\n',
            501: b'Not Implemented\r\n',
        }
        return (
            bytes(version, 'utf-8') + self.int2b(code) + status_codes[code],  # response line
            b'\r\n'  # blank line
        )


if __name__ == '__main__':
    try:
        server = HTTPServer()
        server.start()
    except KeyboardInterrupt:
        print("Server Stopped")
