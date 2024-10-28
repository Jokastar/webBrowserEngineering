import tkinter

WIDTH, HEIGHT = 800, 600

class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window, 
            width=WIDTH,
            height=HEIGHT
        )
        self.canvas.pack()
        self.display_list = []
        self.scroll = 0
        self.SCROLL_STEP = 100
        self.HSTEP = 13
        self.VSTEP = 18

        self.window.bind("<Down>", self.scrolldown)

    def layout(self, body):
    
        cursor_x, cursor_y = self.HSTEP, self.VSTEP

        display_list = []

        for c in body:
            display_list.append((cursor_x, cursor_y, c))

            if(cursor_x >= WIDTH - self.HSTEP):
                cursor_x = self.HSTEP
                cursor_y += self.VSTEP
            else:
                cursor_x += self.HSTEP

        return display_list
    
    def draw(self):
        self.canvas.delete("all")

        for x, y, c in self.display_list:
            if y > self.scroll + HEIGHT: continue
            if y + self.VSTEP < self.scroll: continue
            self.canvas.create_text(x, y - self.scroll, text=c)

    def load(self, url):
        body = url.request()
        text = url.lex(body)
        self.display_list = self.layout(text)
        self.draw()

    def scrolldown(self, e):
        self.scroll += self.SCROLL_STEP
        self.draw()