import matplotlib.pyplot as plt
import numpy as np

from skimage import draw

class Rectangle():
    def __init__(self, center, width, height=None, rotation=0):
        self.y, self.x = center
        self.width = width
        self.height = height if height is not None else width
        self.rotation = rotation
    
    def get_coords(self):
        top_left = self.x - (self.width // 2), self.y - (self.height // 2)
        bottom_right = self.x + (self.width // 2), self.y + (self.height // 2)
        coords = draw.rectangle_perimeter(top_left, extent=(self.width, self.height))
        return coords

class Ellipse():
    def __init__(self, center, major, minor=None, rotation=0):
        self.y, self.x = center
        self.major = major
        self.minor = minor if minor is not None else major
        self.rotation = rotation
    
    def get_coords(self):
        coords = draw.ellipse_perimeter(self.x, self.y, self.major, self.minor)
        return coords

class Triangle():
    def __init__(self, top, left_offset, right_offset, rotation=0):
        self.y, self.x = top
        self.left_y, self.left_x = left_offset
        self.right_y, self.right_x = right_offset
        self.rotation = rotation
    
    def get_coords(self):
        rows = [self.x, self.x + self.left_x, self.x + self.right_x]
        columns = [self.y, self.y + self.left_y, self.y + self.right_y]
        coords = draw.polygon_perimeter(rows, columns)
        return coords


class House():
    def __init__(self, center, scale, rotation=0):
        self.x, self.y = center
        self.scale = scale
        self.rotation = rotation
    
    def get_coords(self):
        walls = Rectangle((self.x, self.y), self.scale)
        rooftop = (self.x, self.y - self.scale)
        roof = Triangle(rooftop, (-self.scale // 2, self.scale // 2), (self.scale // 2, self.scale // 2))
        rr, cc = map(np.concatenate, zip(*(walls.get_coords(), roof.get_coords())))
        return rr, cc

rect = Rectangle((64, 64), 10, 30)
img = np.zeros((128, 128), dtype=np.uint8)
img[rect.get_coords()] = 1

ellipse = Ellipse((80, 30), 10, 40)
img[ellipse.get_coords()] = 1

triangle = Triangle((5, 5), (0, 30), (30, 30))
img[triangle.get_coords()] = 1

plt.imshow(img) and plt.show()

img = np.zeros((128, 128), dtype=np.uint8)
house = House((80, 64), 30)
img[house.get_coords()] = 1
plt.imshow(img) and plt.show()