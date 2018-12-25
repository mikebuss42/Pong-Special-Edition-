
import pygame
from pygame import Surface
from pygame.sprite import Sprite
from pygame import Rect


class Paddle(Sprite):

    def __init__(self, player, settings, screen):

        super().__init__()

        self.player = player
        self.settings = settings
        self.screen = screen

        self.screen_rect = screen.get_rect()

        self.speed = self.settings.paddle_speed_factor_human
        self.__color_base = self.settings.paddle_color_base_human
        self.__color_border = self.settings.paddle_color_border_human

        self.width = None
        self.height = None
        self.rect_basis = None
        self.rect = None
        self.x = None
        self.y = None
        self.__velocity_x = 0
        self.__velocity_y = 0
        self.__impact_energy = 0
        self.__x_MIN = None
        self.__x_MAX = None
        self.__y_MIN = None
        self.__y_MAX = None
        self.__can_move_x = False
        self.__can_move_y = False
        self.__can_bounce_x = False
        self.__can_bounce_y = False

        self.__is_dirty = True
        self.image = None
        self.rect = None

    def __str__(self):

        s = ""

        s += "This is the paddle"

        return s

    def reset(self):

        self.make_left_side()
        self.reset_position()

    def set_speed(self, s):

        self.speed = s

    def set_base_color(self, color):

        self.__color_base = color

        self.draw(True)

    def set_border_color(self, color):

        self.__color_border = color

        self.draw(True)

    def make_left_side(self):

        self.make_tall_paddle()

        self.__x_MIN = None
        self.__x_MAX = None
        self.__y_MIN = 0
        self.__y_MAX = self.screen_rect.height

        self.x = self.settings.paddle_wall_padding + int(self.width / 2)
        self.y = int(self.screen_rect.height / 2)
        self.reset_rect_basis()

        self.image = None
        self.reset_position()

    def make_right_side(self):

        self.make_tall_paddle()

        self.__x_MIN = None
        self.__x_MAX = None
        self.__y_MIN = 0
        self.__y_MAX = self.screen_rect.height

        self.x = self.screen_rect.width - self.settings.paddle_wall_padding - int(self.width / 2)
        self.y = int(self.screen_rect.height / 2)
        self.reset_rect_basis()

        self.image = None
        self.reset_position()

    def make_top_left_side(self):

        self.make_wide_paddle()

        self.__x_MIN = 0
        self.__x_MAX = int(self.screen_rect.width / 2)
        self.__y_MIN = None
        self.__y_MAX = None

        self.x = int(self.screen_rect.width / 4)
        self.y = self.settings.paddle_wall_padding
        self.reset_rect_basis()

        self.image = None
        self.reset_position()

    def make_bottom_left_side(self):

        self.make_wide_paddle()

        self.__x_MIN = 0
        self.__x_MAX = int(self.screen_rect.width / 2)
        self.__y_MIN = None
        self.__y_MAX = None

        self.x = int(self.screen_rect.width / 4)
        self.y = self.screen_rect.height - self.settings.paddle_wall_padding
        self.reset_rect_basis()

        self.image = None
        self.reset_position()

    def make_top_right_side(self):

        self.make_wide_paddle()

        self.__x_MIN = int(self.screen_rect.width / 2)
        self.__x_MAX = self.screen_rect.width
        self.__y_MIN = None
        self.__y_MAX = None

        self.x = int(self.screen_rect.width * 3 / 4)
        self.y = self.settings.paddle_wall_padding
        self.reset_rect_basis()

        self.image = None
        self.reset_position()

    def make_bottom_right_side(self):

        self.make_wide_paddle()

        self.__x_MIN = int(self.screen_rect.width / 2)
        self.__x_MAX = self.screen_rect.width
        self.__y_MIN = None
        self.__y_MAX = None

        self.x = int(self.screen_rect.width * 3 / 4)
        self.y = self.screen_rect.height - self.settings.paddle_wall_padding
        self.reset_rect_basis()

        self.image = None
        self.reset_position()

    def make_tall_paddle(self):

        self.width = self.settings.paddle_length_short
        self.height = self.settings.paddle_length_long

        self.__can_move_x = False
        self.__can_move_y = True

        self.__can_bounce_x = True
        self.__can_bounce_y = False

    def make_wide_paddle(self):

        self.width = self.settings.paddle_length_long
        self.height = self.settings.paddle_length_short

        self.__can_move_x = True
        self.__can_move_y = False

        self.__can_bounce_x = False
        self.__can_bounce_y = True

    def reset_rect_basis(self):

        self.rect_basis = Rect(
            int(self.x - (self.width / 2)), int(self.y - (self.height / 2)),
            self.width, self.height
        )

    def reset_position(self):

        self.rect = self.rect_basis
        self.x = int(
            self.rect.left + (self.rect.width / 2)
        )
        self.y = int(
            self.rect.top + (self.rect.height / 2)
        )

        self.__velocity_x = 0
        self.__velocity_y = 0

        self.position_changed()
        self.draw(True)

    def position_changed(self):

        self.rect.left = self.x - int(self.width / 2)
        self.rect.top = self.y - int(self.height / 2)

    def move(self, x, y, speed_factor, elapsed_ms):

        # Save current x/y values for velocity later down
        x_previous = self.x
        y_previous = self.y

        #
        if self.__can_move_x:
            self.x += x * self.speed * speed_factor * elapsed_ms

        if self.__can_move_y:
            self.y += y * self.speed * speed_factor * elapsed_ms

        # Calculate instantaneous velocity using the last x/y values
        delta_x = self.x - x_previous
        delta_y = self.y - y_previous
        if elapsed_ms > 0:
            self.__velocity_x = delta_x / elapsed_ms
            self.__velocity_y = delta_y / elapsed_ms

        self.position_changed()

    def can_bounce_x(self):

        return self.__can_bounce_x

    def can_bounce_y(self):

        return self.__can_bounce_y

    def get_position(self):

        return self.x, self.y

    def get_rect(self):

        return self.rect

    def get_velocity(self):

        return self.__velocity_x, self.__velocity_y

    def update(self, elapsed_ms):

        self.keep_in_bounds()
        self.decay_impact_energy(elapsed_ms)

    def keep_in_bounds(self):

        if self.__x_MIN is not None and self.__x_MAX is not None:
            if self.x < self.__x_MIN:
                self.x = self.__x_MIN
            elif self.x > self.__x_MAX:
                self.x = self.__x_MAX

        if self.__y_MIN is not None and self.__y_MAX is not None:
            if self.y < 0:
                self.y = 0
            elif self.y > self.screen_rect.height:
                self.y = self.screen_rect.height

    def receive_impact(self, velocity_x, velocity_y):

        velocity = abs(velocity_x + velocity_y)

        self.__impact_energy += velocity

        self.dirty()

    def decay_impact_energy(self, elapsed_ms):

        if self.__impact_energy:
            if self.__impact_energy < self.settings.paddle_impact_zero:
                self.__impact_energy = 0
            else:
                self.__impact_energy *= pow(self.settings.paddle_impact_energy_decay_factor, elapsed_ms)
                self.dirty()

    def dirty(self):

        self.__is_dirty = True

    def draw(self, force=False):

        #
        if self.image and (force is not True) and (not self.__is_dirty):
            return

        # Create the image surface
        image = Surface(
            (self.rect.width, self.rect.height),
            0,
            self.screen
        )

        # Grab base color, and multiply by impact
        r, g, b, a = self.__color_base
        r *= (1 + self.__impact_energy)
        g *= (1 + self.__impact_energy)
        b *= (1 + self.__impact_energy)
        if r > 100:
            r = 100
        if g > 100:
            g = 100
        if b > 100:
            b = 100
        if r < 10:
            r = 10
        if g < 10:
            g = 10
        if b < 10:
            b = 10

        # Fill with modified base color
        image.fill((r, g, b, a))

        # Draw border
        border_rect = Rect(0, 0, self.rect.width, self.rect.height)
        pygame.draw.rect(image, self.__color_border, border_rect, self.settings.paddle_border_width)

        # Assign to internal
        self.image = image

        self.__is_dirty = False

    def blitme(self):

        self.draw(False)

        self.screen.blit(
            self.image,
            (self.rect.left, self.rect.top)
        )