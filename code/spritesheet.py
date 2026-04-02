import pygame

class Spritesheet:
    def __init__(self, filename):
        #
        self.filename = filename
        self.sprite_sheet = pygame.image.load(self.filename).convert_alpha()
        #
        self.picture_w = self.sprite_sheet.get_width()
        self.picture_h = self.sprite_sheet.get_height()
        
    def load_image(self, column , row):
        x = column * (self.picture_w // 4) # // damit ich nur int bekomme und keine float
        y = row * (self.picture_h // 4)
        frame_w = self.picture_w // 4
        frame_h = self.picture_h // 4
        cutted_image = self.sprite_sheet.subsurface((x, y, frame_w, frame_h))
        return cutted_image

    def load_animation(sprite_sheet):
        pass