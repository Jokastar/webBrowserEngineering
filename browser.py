import tkinter
import tkinter.font
from URL import Text
from Layout import Layout
from HtmlParser import HtmlParser
from global_variables import WIDTH, HEIGHT
from HtmlParser import print_tree

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
        self.nodes = None

        #bind down key to scrolldown function
        self.window.bind("<Down>", self.scrolldown)

        #bind up key to scrolldown function
        self.window.bind("<Up>", self.scrollup)

    def draw(self):
        self.canvas.delete("all")

        for x, y, word, font in self.display_list:
            if y > self.scroll + HEIGHT: continue
            if y + font.metrics("linespace") < self.scroll: continue
            self.canvas.create_text(x, y - self.scroll, text=word, font=font, anchor="nw")


    def load(self, url):
        body = url.request()
        nodes = HtmlParser(body).parse()
        layout = Layout(nodes)
        self.display_list = layout.display_list
        self.draw()

    def scrolldown(self, e):
        self.scroll += self.SCROLL_STEP
        self.draw()

    def scrollup(self, e):
        self.scroll = max(self.scroll - self.SCROLL_STEP, 0)
        self.draw()