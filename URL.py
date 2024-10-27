import socket

class URL:
    def __init__(self, url):
        self.scheme, self.url = url.split("://", 1)
        assert self.scheme == "http"
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
        s.connect((self.host, 80))
        
        # write the request
        request = "GET {} HTTP/1.0\r\n".format(self.path)
        request += "Host: {}\r\n".format(self.host)
        request += "\r\n"
        print("request " + request)

        # send the request 
        s.send(request.encode("utf8"))

        #read the response
        response = s.makefile("r", encoding="utf8", newline="\r\n")
        statusline = response.readline()

        #read the response status
        version, status, explanation = statusline.split(" ", 2)

        #get the reponse header value
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