SELF_CLOSING_TAGS = [
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
]

class Text:
    def __init__(self, text, parent):
        self.text = text
        self.parent = parent
        self.children = []

    def __str__(self):
        return self.text

    def __repr__(self):
        return f'Text("{self.text}")'

class Element:
    def __init__(self, tag, parent, attributes):
        self.tag = tag
        self.parent = parent
        self.children = []
        self.attributes = attributes

    def __str__(self):
        return "<" + self.tag + ">"

    def __repr__(self):
        return f'Tag("{self.tag}")'
    
class HtmlParser:
    def __init__(self, body):
        self.body = body
        self.unfinished = []
    
    def addText(self, text):
        if text.isspace(): return
        self.implicit_tags(None)

        parent = self.unfinished[-1]
        element = Text(text, parent)
        parent.children.append(element)

    def addTag(self, tag):
    
        parseTag, attributes = self.getAttributes(tag)
    # Skip any comment or special tags
        if parseTag.startswith("!"): 
            return
        self.implicit_tags(parseTag)
        
        
        # Check for a self-closing tag
        if parseTag in SELF_CLOSING_TAGS:
            parent = self.unfinished[-1] if self.unfinished else None
            node = Element(parseTag, parent, attributes)
            if parent:
                parent.children.append(node)
            return

        # If it's an opening parseTag
        if not parseTag.startswith("/"):
            parent = self.unfinished[-1] if self.unfinished else None
            node = Element(parseTag, parent, attributes)
            self.unfinished.append(node)
        else:
            # It's a closing tag match it with the most recent tag
            if len(self.unfinished) > 1:
                node = self.unfinished.pop()
                parent = self.unfinished[-1]
                parent.children.append(node)

    def getAttributes(self, text):
         attributes = {}
         elements = text.split(" ")
         tag = elements[0].casefold()

         for pair in elements[1:]:
             
             if "=" in pair:
                key, value = pair.split("=", 1)

                #strip quote sign from the value 
                if len(value) > 2 and value[0] in ["'", "\""]:
                    value = value[1:-1]

                attributes[key.casefold()] = value
             else:
                attributes[pair.casefold()] = ""
             
         return tag , attributes 
             
    def finish(self):
        if not self.unfinished:
            self.implicit_tags(None)
            return
        
        while len(self.unfinished) > 1:
            node = self.unfinished.pop()
            parent = self.unfinished[-1]
            parent.children.append(node)
        return self.unfinished.pop()
    
    def parse(self):
        inTag = False
        text=""
        for char in self.body:
            if char == "<":
                inTag = True
                if(text):self.addText(text)
                text=""
            elif char == ">":
                inTag = False
                if(text):self.addTag(text)
                text=""
            else:
                text+=char
        return self.finish()

    def implicit_tags(self, tag):
        while True:
            open_tags = [node.tag for node in self.unfinished]
            if open_tags == [] and tag != "html":
                self.add_tag("html")
            elif open_tags == ["html"] \
                 and tag not in ["head", "body", "/html"]:
                if tag in self.HEAD_TAGS:
                    self.add_tag("head")
                else:
                    self.add_tag("body")
            elif open_tags == ["html", "head"] and \
                 tag not in ["/head"] + self.HEAD_TAGS:
                self.add_tag("/head")
            else:
                break
def print_tree(node, indent=0):
    print(" " * indent, node)

    for child in node.children:
        print_tree(child, indent + 2)

""" body = "<div><p>This is a <b>bold</b><small>move</small> for real</p><p>Donald J Trump</p></div>"
parser = HtmlParser(body)
root = parser.parse()
print_tree(root) """




