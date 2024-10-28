from URL import URL

url = URL("http://example.org/index.html")

body = url.request()

print("body: " + body)

url.show(body)



