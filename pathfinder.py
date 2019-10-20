import math
from PIL import Image
import numpy as np
import random as r


class Map:
    def __init__(self, file):
        self.file = file
        self.elevations = []
        self.min_elevation = []
        self.max_elevation = []
        self.text_contents = []
        self.colors_big_list = []
        self.little_rows_of_colors = []
        self.paths = []
        self.img = ''

    def read_file(self):
        with open(self.file) as text_file:
            self.text_contents = text_file.read()

    def find_elevations(self):
        self.elevations = [[int(each) for each in line.split()]
                           for line in self.text_contents.split("\n")]

    def find_min_and_max(self):
        self.min_elevation = self.elevations[0][0]
        self.max_elevation = self.elevations[0][0]

        for each in self.elevations:
            for integer in each:
                if integer < self.min_elevation:
                    self.min_elevation = integer
                if integer > self.max_elevation:
                    self.max_elevation = integer

    def get_colors_from_elevations(self):
        for rows in self.elevations:
            for number in rows:
                color_int = round(
                    ((number - self.min_elevation) / (self.max_elevation-self.min_elevation)) * 255)
                self.little_rows_of_colors.append(color_int)
            self.colors_big_list.append(self.little_rows_of_colors)
            self.little_rows_of_colors = []

    def create_map_image(self):
        self.img = Image.fromarray(np.uint8(self.colors_big_list))
        # self.img.save("test.png")
        # saves a test image


class Path:
    def __init__(self, elevations, map):
        self.position = 0
        self.elevations = elevations
        self.all_paths = []
        self.map_pixels = ''
        self.path = []
        self.map = map
        self.poop = ()
        # poop is a tuple of (x,y) coordinates
        self.starting_position_y = 0
        self.list_of_path_elevation_changes = []
        self.hiking_trail = []

    def determine_map_pixels(self):
        self.map.img = self.map.img.convert('RGB')
        self.map_pixels = self.map.img.load()

    def draw_path(self, point):
        self.map_pixels[self.poop] = (255, 255, 102)

    def find_path(self):
        total_elevation_change = 0
        x = 0
        y = self.starting_position_y
        while x < (len(self.elevations)-1):
            point = []
            NE = abs((self.elevations[y-1][x+1]) - self.position)
            E = abs((self.elevations[y][x+1]) - self.position)
            if y >= (len(self.elevations)-1):
                SE = abs((self.elevations[y][x+1]) - self.position)
            else:
                SE = abs((self.elevations[y+1][x+1]) - self.position)
            smallest_delta = min(NE, E, SE)
            if smallest_delta == NE:
                if y <= 0:
                    y = y
                    x += 1
                else:
                    y -= 1
                    x += 1
                self.poop = (x, y)
                point.append(self.poop)
                self.draw_path(point)
                self.position = self.elevations[x][y]
                total_elevation_change += smallest_delta
            elif smallest_delta == E:
                x += 1
                self.poop = (x, y)
                point.append(self.poop)
                self.draw_path(point)
                self.position = self.elevations[x][y]
                total_elevation_change += smallest_delta
            else:
                y += 1
                x += 1
                self.poop = (x, y)
                point.append(self.poop)
                self.draw_path(point)
                self.position = self.elevations[x][y]
                total_elevation_change += smallest_delta
            self.path.append(self.poop)
        self.list_of_path_elevation_changes.append(total_elevation_change)

    def get_all_paths(self):
        while self.starting_position_y < len(self.elevations):
            self.find_path()
            self.starting_position_y += 1
            self.all_paths.append(self.path)
            self.path = []

    def identify_path_of_least_change(self):
        self.hiking_trail = self.all_paths[self.list_of_path_elevation_changes.index(min(
            self.list_of_path_elevation_changes))]

    def draw_hiking_trail(self):
        for pixel in self.hiking_trail:
            self.map_pixels[pixel] = (0, 0, 255)


if __name__ == "__main__":
    map = Map("elevation_large.txt")
    map.read_file()
    map.find_elevations()
    map.find_min_and_max()
    map.get_colors_from_elevations()
    map.create_map_image()
    path = Path(map.elevations, map)
    path.determine_map_pixels()
    path.get_all_paths()
    path.identify_path_of_least_change()
    path.draw_hiking_trail()
    map.img.save("pathfinder.png")