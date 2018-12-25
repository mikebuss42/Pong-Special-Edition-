
import pygame
from pygame import Surface


class Scoreboard:

    def __init__(self, settings, screen, pong):

        self.settings = settings

        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.pong = pong

        self.font_large = pygame.font.SysFont(None, 48)
        self.font_small = pygame.font.SysFont(None, 24)

        self.ball = None

        self.player_left = None
        self.player_right = None

        self.__max_points = None

        self.__is_dirty = True
        self.image = None

    def set_ball(self, ball):

        self.ball = ball

    def set_players(self, player_left, player_right):

        self.player_left = player_left
        self.player_right = player_right

    def set_max_points(self, p):

        self.__max_points = p

        self.dirty()

    def update(self):

        pass

    def dirty(self):

        self.__is_dirty = True

    def draw(self):

        if not self.image:
            self.image = Surface(
                (self.screen_rect.width, self.screen_rect.height),
                pygame.SRCALPHA, self.screen
            )

        #----------------------------------------#
        self.image.fill((255, 0, 0, 0), self.image.get_rect())

        #----------------------------------------#
        self.draw_player_score(True, self.player_left)
        self.draw_player_score(False, self.player_right)

        self.draw_round()

        self.__is_dirty = False

    def draw_player_score(self, is_left, player):

        score = player.get_score()

        #----------------------------------------#
        score_image = self.font_large.render(
            str(score), True,
            self.settings.scoreboard_text_color, self.settings.scoreboard_background_color
        )
        score_image_rect = score_image.get_rect()

        #----------------------------------------#
        score_left_y = int(
            self.screen_rect.height - self.settings.scoreboard_padding - score_image_rect.height
        )

        #----------------------------------------#
        if is_left:
            score_left_x = int(
                self.settings.scoreboard_padding
            )

        else:
            score_left_x = int(
                self.screen_rect.width
                - self.settings.scoreboard_padding
                - score_image_rect.width
            )

        #
        self.image.blit(
            score_image,
            (score_left_x, score_left_y)
        )

    def draw_round(self):

        current_round = self.pong.get_round()

        round_str = "Round " + str(current_round)
        round_image = self.font_large.render(
            str(round_str), True,
            self.settings.scoreboard_text_color, self.settings.scoreboard_background_color
        )
        round_image_rect = round_image.get_rect()
        x = int(
            (self.screen_rect.width / 2)
            - (round_image_rect.width / 2)
        )
        y = int(
            self.settings.scoreboard_padding
        )
        self.image.blit(round_image, (x, y))
        y += round_image_rect.height

        #----------------------------------------#
        first_str = "First to " + str(self.__max_points) + " points"
        first_image = self.font_small.render(
            str(first_str), True,
            self.settings.scoreboard_text_color, self.settings.scoreboard_background_color
        )
        first_image_rect = first_image.get_rect()
        x = int(
            (self.screen_rect.width / 2)
            - (first_image_rect.width / 2)
        )
        #----------------------------------------#
        y = int(self.screen_rect.height ) - int(first_image_rect.height )
        self.image.blit(first_image, (x, y))

    def blitme(self):

        if not self.image or self.__is_dirty:
            self.draw()

        self.screen.blit(self.image, (0, 0))