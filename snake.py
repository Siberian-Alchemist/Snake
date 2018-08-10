import pygame
from game_object import GameObject
import math


class SnakeHead(GameObject):
    def __init__(self, x, y, w, h, speed, image):
        GameObject.__init__(self, x, y, w, h, speed)
        self.image = image

    def draw(self, surface):
        angle = 0
        if self.speed[0] == 0:
            angle = math.asin(-self.speed[1]/abs(self.speed[1]))/3.14*180
        else:
            angle = math.acos(self.speed[0]/abs(self.speed[0]))/3.14*180
        new_image = pygame.transform.rotate(self.image, angle)
        surface.blit(new_image, self.bounds)


class Tail(GameObject):
    def __init__(self, w, pred, image1, image2):
        GameObject.__init__(self, pred.left, pred.bottom, w, w, pred.speed.copy())
        self.image1 = image1
        self.image2 = image2
        self.pred = pred

    def draw(self, surface, last):
        if not last:
            surface.blit(self.image1, (self.bounds.x, self.bounds.y))
        else:
            angle = 0
            if self.speed[0] == 0:
                angle = math.asin(self.speed[1] / abs(self.speed[1])) / 3.14 * 180
            else:
                angle = math.acos(-self.speed[0] / abs(self.speed[0])) / 3.14 * 180
            new_image = pygame.transform.rotate(self.image2, angle)
            surface.blit(new_image, (self.bounds.x, self.bounds.y))

    def update(self):
        self.old_pos = self.bounds.copy()
        self.old_speed = self.speed
        self.speed = self.pred.old_speed.copy()
        self.bounds = self.pred.old_pos.copy()


class Snake:
    def __init__(self, start_pos_x, start_pos_y, head_w, head_h, tail_w, tail_length, speed,
                 head_image_filename, tail_image1_filename,
                 tail_image2_filename):
        self.image = pygame.image.load(head_image_filename).convert_alpha()
        self.image1 = pygame.image.load(tail_image1_filename).convert_alpha()
        self.image2 = pygame.image.load(tail_image2_filename).convert_alpha()
        self.head = SnakeHead(start_pos_x, start_pos_y, head_w, head_h, speed, self.image)
        self.tail = [Tail(tail_w, self.head, self.image1, self.image2), ]
        self.last = None
        for i in range(1, tail_length):
            self.increase()

    def increase(self):
        self.tail.append(Tail(self.tail[0].width, self.tail[self.tail.__len__() - 1],
                         self.image1, self.image2))
        self.last = self.tail[self.tail.__len__() - 1]


    def draw(self, surface):
        self.head.draw(surface)
        for part in self.tail:
            part.draw(surface, part == self.last)

    def update(self):
        self.head.update()
        for part in self.tail:
            part.update()

    def handle(self, key):
        speed_abs = self.tail[0].width
        if key == pygame.K_LEFT:
            if self.head.speed[0] <= 0:
                self.head.speed = [-speed_abs, 0]
        elif key == pygame.K_RIGHT:
            if self.head.speed[0] >= 0:
                self.head.speed = [speed_abs, 0]
        elif key == pygame.K_DOWN:
            if self.head.speed[1] >= 0:
                self.head.speed = [0, speed_abs]
        elif key == pygame.K_UP:
            if self.head.speed[1] <= 0:
                self.head.speed = [0, -speed_abs]

