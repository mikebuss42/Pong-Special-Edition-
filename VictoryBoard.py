import pygame
from pygame import Surface
from pygame import Rect

from OverlayBoard import OverlayBoard


class VictoryBoard(OverlayBoard):

    def __init__(self, settings, screen, pong):

        super().__init__(settings, screen, pong)

        #----------------------------------------#
        width = int(self.screen_rect.width * self.settings.victory_board_size_factor)
        height = int(self.screen_rect.height * self.settings.victory_board_size_factor)
        self.image = Surface(
            (width, height),
            pygame.SRCALPHA, self.screen
        )
        self.rect = self.image.get_rect()
        self.rect.left = int(
            (self.screen_rect.width / 2)
            - (self.rect.width / 2)
        )
        self.rect.top = int(
            (self.screen_rect.height / 2)
            - (self.rect.height / 2)
        )

        self.__player_winner = None

    def set_winner(self, player):

        self.__player_winner = player

        self.dirty()

    def update(self, elapsed_me):

        super().update(elapsed_me)

        if self.get_activated_time() > self.settings.victory_board_max_activation_time_ms:
            self.deactivate()

    def draw(self):

        #----------------------------------------#
        if not self.__player_winner:
            return

        super().draw()

        #----------------------------------------#
        self.image.fill(self.settings.victory_board_background_color, None)

        #----------------------------------------#
        pygame.draw.rect(
            self.image,
            (255, 0, 0, 255),
            Rect(0, 0, self.rect.width, self.rect.height),
            1
        )

        y = 0
        y = self.draw_title(y)
        y = self.draw_info(y)

        return y

    def draw_title(self, y):


        image = self.font_huge.render(
            self.settings.victory_board_title, True,
            self.settings.victory_board_title_color, self.settings.victory_board_background_color
        )
        image_rect = image.get_rect()


        x = int(
            (self.rect.width / 2)
            - (image_rect.width / 2)
        )
        y += self.settings.victory_board_padding_border
        self.image.blit(image, (x, y))
        y += image_rect.height + self.settings.victory_board_padding_items

        return y

    def draw_info(self, y):

        text = self.__player_winner.get_label() + " wins!"

        #----------------------------------------#
        image = self.font_large.render(
            text, True,
            self.settings.victory_board_text_color, self.settings.victory_board_background_color
        )
        image_rect = image.get_rect()

        x = int(
            (self.rect.width / 2)
            - (image_rect.width / 2)
        )
        y += self.settings.victory_board_padding_border
        self.image.blit(image, (x, y))
        y += image_rect.height + self.settings.victory_board_padding_items

        #----------------------------------------#
        text = "Player failed..."
        image = self.font_small.render(
            text, True,
            self.settings.victory_board_text_color, self.settings.victory_board_background_color
        )
        image_rect = image.get_rect()

        x = int(
            (self.rect.width / 2)
            - (image_rect.width / 2)
        )
        y += self.settings.victory_board_padding_border
        self.image.blit(image, (x, y))
        y += image_rect.height + self.settings.victory_board_padding_items

        return y