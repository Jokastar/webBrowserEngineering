from URL import URL
from Browser import Browser

url = URL("https://browser.engineering/html.html")
browser = Browser()
browser.load(url)
browser.window.mainloop()



