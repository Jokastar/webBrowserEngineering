import tkinter
from tkinter import font  # Import `font` directly for easier access


from HtmlParser import Text
from globals_variables import HSTEP, VSTEP, WIDTH

FONTS = {}

class Layout:
    def __init__(self, nodes):
        """
        Initializes the layout for text and tags by setting up initial parameters such as font style, weight, size, 
        and cursor position for rendering. It processes each token by calling `token(tok)` and finalizes the layout 
        of the current line using `flush()`.
        """
        self.nodes = nodes  # List of tokens to be processed (Text or Tag)
        self.display_list = []  # List that will store the final display details
        self.cursor_x = HSTEP  # Horizontal cursor position, starting at a step from the left margin
        self.cursor_y = VSTEP  # Vertical cursor position, starting at a step from the top margin
        self.weight = "normal"  # Initial font weight
        self.style = "roman"  # Initial font style
        self.size = 12  # Initial font size

        self.line = []  # Temporary storage for words in the current line

        # Process each nodes in the input
        self.recurse(self.nodes)
        self.flush()  # Ensure any remaining text is added to the display list

   
    def open_tag(self, tag):
        if tag == "i":
            self.style = "italic"
        elif tag == "b":
            self.weight = "bold"
        elif tag == "small":
            self.size -= 2  # Decrease font size for <small> tags
        elif tag == "big":
            self.size += 4  # Increase font size for <big> tags
        elif tag == "br":
            self.flush()  # New line (flush current line content)
            self.cursor_y += VSTEP  # Additional spacing after paragraphs
            
    def close_tag(self, tag):
        if tag == "i":
            self.style = "roman"
        elif tag == "b":
            self.weight = "normal"
        elif tag == "small":
            self.size += 2
        elif tag == "big":
            self.size -= 4

    def word(self, word):
        """
        Adds a word to the current line with its x-position, font, and style. If the line width exceeds the screen 
        width, it calls `flush()` to move to the next line. It then updates `cursor_x` based on the word width.
        """
        font = get_font(self.size, self.weight, self.style)  # Get font based on size, weight, and style
        w = font.measure(word)  # Measure word width
        
        # Check if adding the word would exceed the line width, and flush if needed
        if self.cursor_x + w > WIDTH - HSTEP:
            self.flush()
        
        # Append the word and its current x-position to the line
        self.line.append((self.cursor_x, word, font))
        
        # Update x-position for the next word
        self.cursor_x += w + font.measure(" ")

    def flush(self):
        """
        Renders the current line of words to `display_list` by calculating the baseline for alignment, updating 
        `cursor_y` for the next line, and resetting `cursor_x` and `line` for new content.
        """
        if not self.line:
            return  # Skip if there are no words to process in the line
        
        # Get the font metrics for each word in the line
        metrics = [font.metrics() for x, word, font in self.line]
        
        # Calculate the maximum ascent for baseline alignment of the current line
        max_ascent = max([metric["ascent"] for metric in metrics])
        baseline = self.cursor_y + 1.25 * max_ascent
        
        # Align each word to the baseline and add it to the display list
        for x, word, font in self.line:
            y = baseline - font.metrics("ascent")
            self.display_list.append((x, y, word, font))
        
        # Update `cursor_y` for the next line by adding the maximum descent
        max_descent = max([metric["descent"] for metric in metrics])
        self.cursor_y = baseline + 1.25 * max_descent
        self.cursor_x = HSTEP  # Reset x-position to left margin
        self.line = []  # Clear current line content

    def recurse(self, tree):
        if isinstance(tree, Text):
            for word in tree.text.split():
                self.word(word)
        else:
            self.open_tag(tree.tag)
            for child in tree.children:
                self.recurse(child)
            self.close_tag(tree.tag)

def get_font(size, weight, style):
    """
    Returns a font object based on the specified `size`, `weight`, and `style`. This function caches font objects 
    to avoid creating duplicate fonts.
    """
    key = (size, weight, style)
    if key not in FONTS:
        font = tkinter.font.Font(size=size, weight=weight, slant=style)
        label = tkinter.Label(font=font)  # Dummy label to hold the font reference
        FONTS[key] = (font, label)
    return FONTS[key][0]  # Return only the font, discarding the label

        