from http.server import HTTPServer, BaseHTTPRequestHandler

def parseInfo(head, httpReq, content, msn):
    #separar los elementos solicitados para enviar respuesta
    data = httpReq.split("\n")
    msn = msn.split("%9D")
    cont = 0
    try:
        msn = msn[1]
        aux = ""
        for i in range(len(msn)):
            if msn[i] == "%" and msn[i+1] == "2" and msn[i+2] == "0":
                cont -= 1
                aux += " "
            elif msn[i] == "%" and msn[i+1] == "E" and msn [i+2] == "2":
                break
            else:
                if msn[i-1] != "%" and msn[i-2] != "%":
                    aux += msn[i]
                    cont += 1

        response = " " + head +  r"200 OK\r\n " + "\n " + str(data[2]) + r"\r\n" \
                   + "\n Content-Length: " + str(cont) + r"\r\n" \
                   + "\n Content-Type: " + content + r"\r\n " + "\n " \
                   + str(data[1]) + r"\r\n " + "\n " + r"\r\n "  + "\n " + aux
        print (response)
    except:
        pass

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello World!!!!')

        content = self.error_content_type
        headers = str(self.headers)
        message = str(self.path)
        version = str(self.request_version)
        parseInfo(version, headers, content, message)

httpd = HTTPServer(('localhost', 5005), SimpleHTTPRequestHandler)
httpd.serve_forever()
