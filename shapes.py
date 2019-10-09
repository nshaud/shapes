import matplotlib.pyplot as plt
import numpy as np

from skimage import draw

""" Simple elements

    Elements are defined by a center, a scale (on x and y) and an angle.

    Since the 2D coordinates in numpy are line-column, this means that x is actually the height
    and y is the width. We invert (x,y) to be less confusing when drawing figures.
    However y increases when going "down" in the image.
"""
class Rectangle():
    def __init__(self, center, width, height=None, rotation=0):
        self.y, self.x = center
        self.width = width
        self.height = height if height is not None else width
        self.rotation = rotation
    
    def coords(self):
        top_left = self.x - (self.height // 2), self.y - (self.width // 2)
        bottom_right = self.x + (self.height // 2), self.y + (self.width // 2)
        coords = draw.rectangle_perimeter(top_left, extent=(self.height, self.width))
        return coords

class Ellipse():
    def __init__(self, center, major, minor=None, rotation=0):
        self.y, self.x = center
        self.major = major
        self.minor = minor if minor is not None else major
        self.rotation = rotation
    
    def coords(self):
        coords = draw.ellipse_perimeter(self.x, self.y, self.major, self.minor)
        return coords

class Triangle():
    def __init__(self, top, left_offset, right_offset, rotation=0):
        self.y, self.x = top
        self.left_y, self.left_x = left_offset
        self.right_y, self.right_x = right_offset
        self.rotation = rotation
    
    def coords(self):
        rows = [self.x, self.x + self.left_x, self.x + self.right_x]
        columns = [self.y, self.y + self.left_y, self.y + self.right_y]
        coords = draw.polygon_perimeter(rows, columns)
        return coords


""" Complex figures

    Complex figures are comprised of a set of simple Elements.
"""
class House():
    def __init__(self, center, scale, rotation=0):
        self.x, self.y = center
        self.scale = scale
        self.rotation = rotation
    
    def coords(self):
        # A house is defined as a square and a triangle on top.
        walls = Rectangle((self.x, self.y), self.scale)
        # The rooftop (highest point) is in the horizontal middle of the house and at height max height + half the scale
        rooftop = (self.x, self.y - self.scale)
        roof = Triangle(rooftop, (-self.scale // 2, self.scale // 2), (self.scale // 2, self.scale // 2))
        # We concatenate the row and column coordinates for the walls and the roof
        rr, cc = map(np.concatenate, zip(*(walls.coords(), roof.coords())))
        return rr, cc

rect = Rectangle((64, 64), 10, 30)
img = np.zeros((128, 128), dtype=np.uint8)
img[rect.coords()] = 1

ellipse = Ellipse((80, 30), 10, 40)
img[ellipse.coords()] = 1

triangle = Triangle((5, 5), (0, 30), (30, 30))
img[triangle.coords()] = 1

plt.imshow(img) and plt.show()

# Draw a house
img = np.zeros((128, 128), dtype=np.uint8)
house = House((80, 64), 30)
img[house.coords()] = 1
plt.imshow(img) and plt.show()