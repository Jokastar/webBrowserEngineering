import socket
import ssl

class URL:
    def __init__(self, url):
        self.scheme, self.url = url.split("://", 1)
        
        #check scheme type
        assert self.scheme in ["http", "https"]
        
        if self.scheme == "http":
            self.port = 80
        elif self.scheme == "https":
            self.port = 443

        self.port = int(self.port)

        if "/" not in self.url:
            self.url+= "/"
        
        self.host, self.url = self.url.split("/", 1)
        self.path = "/" + self.url
        print(self.scheme, self.host, self.path)

    def request(self):
        # create a socket
        s = socket.socket(
            family = socket.AF_INET, 
            type = socket.SOCK_STREAM, 
            proto = socket.IPPROTO_TCP
            )
        s.connect((self.host, self.port))

        if self.scheme == "https":
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname=self.host)
        
        # write the request
        request = "GET {} HTTP/1.0\r\n".format(self.path)
        request += "Host: {}\r\n".format(self.host)
        request += "\r\n"

        # send the request 
        s.send(request.encode("utf8"))

        #read the response
        response = s.makefile("r", encoding="utf8", newline="\r\n")
        
        #read the first line
        statusline = response.readline()

        #read the response status
        version, status, explanation = statusline.split(" ", 2)

        #get the reponse headers value
        response_headers = {}
        while True:
            line = response.readline()
            if line == "\r\n": break
            header, value = line.split(":", 1)
            response_headers[header.casefold()] = value.strip()

        #check if this headers are in the response
        assert "transfer-encoding" not in response_headers
        assert "content-encoding" not in response_headers

        #get the response body
        body = response.read()
        s.close()

        return body
    
    def show(self, body):

        in_tag = False
        for c in body:
            if c == "<":
                in_tag = True
            elif c == ">":
                in_tag = False
            elif not in_tag:
                print(c, end="")
    
    def load(self):
        body = self.request()
        self.show(body)