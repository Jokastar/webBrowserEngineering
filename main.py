from URL import URL
from Browser import Browser

url = URL("https://browser.engineering/examples/xiyouji.html")
browser = Browser()
browser.load(url)
browser.window.mainloop()



