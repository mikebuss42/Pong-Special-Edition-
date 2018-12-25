
import pygame
from pygame import Surface


class OverlayBoard:

    def __init__(self, settings, screen, pong):

        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.pong = pong

        self.font_huge = pygame.font.SysFont(None, 60)
        self.font_large = pygame.font.SysFont(None, 40)
        self.font_small = pygame.font.SysFont(None, 25)

        self.__activated = True
        self.__activated_time = 0
        self.__is_dirty = True
        self.image = None
        self.rect = None
        self.opacity = 255

    def dirty(self):

        self.__is_dirty = True

    def set_opacity(self, alpha):

        self.opacity = alpha

    def get_opacity(self):

        return self.opacity

    def update(self, elapsed_me):

        self.__activated_time += elapsed_me

    def draw(self):

        if not self.image:
            self.image = Surface(
                (self.screen_rect.width, self.screen_rect.height),
                pygame.SRCALPHA, self.screen
            )
            self.rect = self.image.get_rect()

        self.image.fill((255, 0, 0, 0), self.image.get_rect())

        self.__is_dirty = False

    def draw_adjust_opacity(self):

        #
        if not self.image or self.opacity == 255:
            return

        #
        for y in range(0, self.rect.height):
            for x in range(0, self.rect.width):
                color = self.image.get_at((x, y))
                alpha = color.a
                alpha -= (255 - self.opacity)
                try:
                    color.a = alpha
                except ValueError:
                    color.a = 0
                self.image.set_at((x, y), color)

    def activate(self):

        self.__activated = True
        self.__activated_time = 0

        self.dirty()

    def deactivate(self):

        self.__activated = False

    def is_activated(self):

        return self.__activated

    def get_activated_time(self):

        return self.__activated_time

    def blitme(self):

        if not self.__activated:
            return

        if not self.image or self.__is_dirty:
            self.draw()

        self.screen.blit(self.image, (self.rect.left, self.rect.top))