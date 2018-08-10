import pygame
from game_object import GameObject


class Apple(GameObject):
    def __init__(self, pos_x, pos_y, radius, apple_image_filename):
        self.image = pygame.image.load(apple_image_filename).convert_alpha()
        GameObject.__init__(self, pos_x, pos_y, radius, radius)

    def add_new(self, pos_x, pos_y):
        self.bounds = self.bounds.move(pos_x, pos_y)

    def draw(self, surface):
        surface.blit(self.image, (self.bounds.x, self.bounds.y))


