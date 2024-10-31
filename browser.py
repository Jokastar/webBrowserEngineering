from DocumentLayout import DocumentLayout
from HtmlParser import HtmlParser
from globals_variables import  HEIGHT, VSTEP, SCROLL_STEP, WIDTH
from HtmlParser import print_tree
import tkinter

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
        self.nodes = None

        #bind down key to scrolldown function
        self.window.bind("<Down>", self.scrolldown)

        #bind up key to scrolldown function
        self.window.bind("<Up>", self.scrollup)
        
    def load(self, url):
        body = url.request()
        self.nodes = HtmlParser(body).parse()
        self.document = DocumentLayout(self.nodes)
        self.document.layout()
        self.display_list = []
        paint_tree(self.document, self.display_list)
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        for cmd in self.display_list:
            if cmd.top > self.scroll + HEIGHT: continue
            if cmd.bottom < self.scroll: continue
            cmd.execute(self.scroll, self.canvas)

    def scrolldown(self, e):
        max_y = max(self.document.height + 2*VSTEP - HEIGHT, 0)
        self.scroll = min(self.scroll + SCROLL_STEP, max_y)
        self.draw()
    
    def scrollup(self, e):
        self.scroll = max(self.scroll - SCROLL_STEP, 0)
        self.draw()

def paint_tree(layout_object, display_list):
    display_list.extend(layout_object.paint())

    for child in layout_object.children:
        paint_tree(child, display_list)