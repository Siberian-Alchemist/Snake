import pygame
import random
from time import sleep

import colors
import config as c
from snake import Snake
from apple import Apple
from game import Game
from text_object import TextObject


class SnakeGame(Game):
    def __init__(self):
        Game.__init__(self, 'Snake', c.window_width, c.window_height, c.background_image, c.frame_rate)
        self.sound_effects = {name: pygame.mixer.Sound(sound) for name, sound in c.sounds_effects.items()}
        self.snake = None
        self.apple = None
        self.score_label = None
        self.score = 0

        self.create_snake()
        self.create_apple()
        self.create_score_label()

        self.game_over = False

    def create_score_label(self):
        self.score_label = TextObject(c.score_offset,
                                      c.status_offset_y,
                                      lambda: f'СЧЕТ: {self.score}',
                                      c.text_color,
                                      c.font_name,
                                      c.font_size)
        self.objects.append(self.score_label)

    def create_snake(self):
        self.snake = Snake(c.start_pos_x, c.start_pos_y, c.head_w, c.head_h, c.tail_w, c.start_length, c.speed,
                           c.snake_head_image, c.snake_tail1_image, c.snake_tail2_image)
        self.objects.append(self.snake)
        self.keydown_handlers[pygame.K_RIGHT].append(self.snake.handle)
        self.keydown_handlers[pygame.K_LEFT].append(self.snake.handle)
        self.keydown_handlers[pygame.K_UP].append(self.snake.handle)
        self.keydown_handlers[pygame.K_DOWN].append(self.snake.handle)

    def create_apple(self):
        self.apple = Apple(random.randrange(10, c.window_width - 10), random.randrange(30, c.window_height - 20), c.apple_radius,
                           c.apple_image)
        self.objects.append(self.apple)

    def put_apple(self):
        flag = True
        while flag:
            new_place = pygame.Rect(random.randrange(10, c.window_width - 10),
                                    random.randrange(30, c.window_height-20),
                                    self.apple.width, self.apple.width)
            flag = False
            if self.snake.head.bounds.colliderect(new_place):
                flag = True
            for part in self.snake.tail:
                if part.bounds.colliderect(new_place):
                    flag = True
        self.apple.bounds = new_place

    def handle_collision(self):
        for part in self.snake.tail:
            if self.snake.head.bounds.colliderect(part.bounds):
                self.game_over = True
        if (self.snake.head.left < 0) or (self.snake.head.right > c.window_width) \
                or (self.snake.head.bottom > c.window_height) or (self.snake.head.top < 0):
            self.game_over = True

        if self.snake.head.bounds.colliderect(self.apple.bounds):
            self.sound_effects['eaten'].play()
            self.score += 1
            self.snake.increase()
            self.put_apple()

    def update(self):
        self.handle_collision()
        super().update()
        if self.game_over:
            self.sound_effects['game_over'].play()
            self.show_message('ДОИГРАЛСЯ', centralized=True, color=colors.BLACK, font_size=80)

    def show_message(self, text, color=colors.BLACK, font_name='Arial', font_size=20, centralized=False):
        message = TextObject(c.window_width // 2, c.window_height // 2, lambda: text, color, font_name, font_size)
        self.draw()
        message.draw(self.surface, centralized)
        pygame.display.update()
        sleep(c.message_duration)


def main():
    SnakeGame().run()


if __name__ == '__main__':
    main()
