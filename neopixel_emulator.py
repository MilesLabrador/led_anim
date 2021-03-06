from tkinter import *
import time
import numpy as np
class NeoPixel():
    """
    Class to mimic neopixel.NeoPixel object that controls leds from neopixel library
    We don't need board or auto_write, but keep for consistency sake
    """
    #def __init__(self, board, num_leds, pixel_order, auto_write):
    """Borrowing init parameters from Adafruit_CircuitPython_NeoPixel library"""
    def __init__(
        self, pin, n, *, bpp=3, brightness=1.0, auto_write=True, pixel_order=None, ring=False, pixel_size=10
    ):
        self.tk = Tk()
        self.width = 800
        self.height=500
        self.canvas = Canvas(self.tk, width=self.width, height=self.height)
        self.tk.title("led animations!")
        # make all led elements stack on same canvas
        self.canvas.pack()

        # initialize array that will keep track of our led objects to manipulate
        self.led_arr = []
        # set number of leds to n
        self.num_leds = n
        # initialize all led objects that are part of our led array
            
        # If ring=True (LEDS are on ring-shaped PCB), set leds equidistant from each other in circle
        if ring:
            # set radius of pcb ring and add buffer of 1 pixel to keep it in view
            r = (min(self.width, self.height)/2)-pixel_size
            # Make equidistant circles (leds) around a center of a canvas!
            origin_x = self.width/2
            origin_y = self.height/2
            for i in range(self.num_leds):
                x = origin_x + r * np.cos(2 * np.pi * i / self.num_leds) 
                y = origin_y + r * np.sin(2 * np.pi * i / self.num_leds)
                self.led_arr.append(led(color="black", size=pixel_size, xpos= x, ypos=y, canvas=self.canvas))
        else:
            # default make leds in a line
            for i in range(self.num_leds):
                self.led_arr.append(led(color="black", size=pixel_size, xpos= ((pixel_size/2))+(pixel_size*(i+1)), ypos=250, canvas=self.canvas))
        
        # IMPORTANT, we need the canvas to remain open
        #self.canvas.mainloop()
    def __getitem__(self, item_index):
        """Return led object at led_arr[item_index] when requested, though I don't think this is
        a feature that is used in neopixel library
        """
        return self.led_arr[item_index].color
    
    def __setitem__(self, item_index, rbg_tuple):
        """Assign color (from (R,B,G) format) to led object at led_arr[item_index]"""
        # Convert (R,B,G) tuple to RGB tuple then hex color code
        rgb_tuple = (rbg_tuple[0], rbg_tuple[2], rbg_tuple[1])
        hex_color = self.rgb_to_hex(rgb_tuple)
        
        self.led_arr[item_index].update_color(hex_color)
    def __len__(self):
        """Find number of leds that the led_arr was initialized with and return"""
        return self.num_leds
    
    def rgb_to_hex(self, rgb_tuple):
        """Convert RGB values to hex that tkinter can utilize"""
        hex_color =  '#%02x%02x%02x' % rgb_tuple  # convert RGB to hex
        return hex_color
        
    def fill(self, rbg_tuple):
        """Change colors of all led objects in one command"""
        # Convert (R,B,G) tuple to RGB tuple then hex color code
        rgb_tuple = (rbg_tuple[0], rbg_tuple[2], rbg_tuple[1])
        hex_color = self.rgb_to_hex(rgb_tuple)
        for pixel in self.led_arr:
            pixel.update_color(hex_color)
    
    def show(self):
        """Emulate pixel updates by updating tkinter"""
        self.tk.update() # show updated changes
        #self.tk.mainloop()

class led:
    def __init__(self, color, size, xpos, ypos, canvas):
        # Make circle centered at xpos ypos by defining x0,y0,x1,y1 around the center in accordance with size
        x0, y0, x1, y1 = xpos-(size/2), ypos-(size/2), xpos+(size/2), ypos+(size/2)
        self.color = color
        self.canvas = canvas
        self.shape = self.canvas.create_oval(x0, y0, x1, y1, fill=self.color)

    def update_color(self, hex_color):
        self.color = hex_color
        self.canvas.itemconfig(self.shape, fill=self.color)