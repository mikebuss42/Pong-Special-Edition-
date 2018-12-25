
import pygame


class Background:

    def __init__(self, settings, screen):

        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.image = None
        self.image_rect = None

        self.draw()

    def update(self, elapsed_ms):
        pass

    def draw(self):

        #----------------------------------------#
        if not self.image:
            self.image = self.screen.copy()
            self.image_rect = self.image.get_rect()

        x_midpoint = int(self.image_rect.width / 2)

        #----------------------------------------#
        self.image.fill(self.settings.background_color, self.screen_rect)

        r = g = 0
        b = 0
        b_velocity = 0.005
        b_acceleration = 0.002
        for x in range(0, x_midpoint):
            pygame.draw.line(
                self.image,
                (r, g, int(b)),
                (x, 0),
                (x, self.image_rect.height),
                1
            )
            pygame.draw.line(
                self.image,
                (r, g, int(b)),
                (self.image_rect.width - x, 0),
                (self.image_rect.width - x, self.image_rect.height),
                1
            )
            b += b_velocity
            b_velocity += b_acceleration
            if b > 100:
                b = 100

        x = int(self.image_rect.width / 2)
        y = 0
        while y < self.image_rect.height:

            pygame.draw.line(
                self.image,
                self.settings.background_net_line_color,
                (x, y),
                (x, y + self.settings.background_net_line_spacing),
                self.settings.background_net_line_width
            )
            y += (self.settings.background_net_line_spacing * 2)

    def blitme(self):

        self.screen.blit(self.image, (0, 0))