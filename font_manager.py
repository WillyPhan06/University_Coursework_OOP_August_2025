# font_manager.py
import tkinter.font as tkfont

class FontManager:
    def __init__(self, family="Helvetica", default_size=15, text_size=12, fixed_size=12):
        self.family = family
        self.default_size = default_size
        self.text_size = text_size
        self.fixed_size = fixed_size

    def configure(self):
        default_font = tkfont.nametofont("TkDefaultFont")
        default_font.configure(size=self.default_size, family=self.family)

        text_font = tkfont.nametofont("TkTextFont")
        text_font.configure(size=self.text_size, family=self.family)

        fixed_font = tkfont.nametofont("TkFixedFont")
        fixed_font.configure(size=self.fixed_size, family=self.family)
