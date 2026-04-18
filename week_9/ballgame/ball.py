import pygame

class Ball:
    def __init__(self, x, y, radius, color, screen_width, screen_height):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.step = 5

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

    def move_up(self):
        if self.y - self.step >= self.radius:
            self.y -= self.step

    def move_down(self):
        if self.y + self.step <= self.screen_height - self.radius:
            self.y += self.step

    def move_left(self):
        if self.x - self.step >= self.radius:
            self.x -= self.step

    def move_right(self):
        if self.x + self.step <= self.screen_width - self.radius:
            self.x += self.step