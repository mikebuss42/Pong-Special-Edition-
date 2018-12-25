
import pygame
from pygame.mixer import Sound


from Settings import Settings
from Background import Background
from WelcomeBoard import WelcomeBoard
from Scoreboard import Scoreboard
from VictoryBoard import VictoryBoard
from Ball import Ball
from Player import Player


import os
import sys


class Pong:

    def __init__(self):

        self.settings = Settings()

        self.screen = None
        self.screen_rect = None
        self.clock = None

        self.background = None
        self.welcome_board = None
        self.scoreboard = None
        self.victory_board = None
        self.ball = None
        self.players = None
        self.player_left = None
        self.player_right = None

        self.time_since_left_player_human_input = 0
        self.time_since_right_player_human_input = 0

        self.initialize_pygame()

        self.sound_game_start = None
        self.sound_game_end = None
        self.sound_you_lose = None
        self.load_sounds()

        self.__round = 0
        self.__points_max = None
        self.is_playing = False
        self.time_since_last_game = 0

        self.__ai_difficulty = self.settings.game_default_difficulty_value

        self.set_max_points(self.settings.game_default_points)
        self.start_ai_game()
        self.main_loop()

    def initialize_pygame(self):

        print("Initializing Pong game ...")

        pygame.mixer.pre_init(self.settings.sound_sample_rate, -16, self.settings.sound_channels, 1024)
        pygame.mixer.init()
        pygame.init()

        self.clock = pygame.time.Clock()

        width = int(self.settings.screen_width * self.settings.screen_resize)
        height = int(self.settings.screen_height * self.settings.screen_resize)
        self.screen = pygame.display.set_mode((width, height))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption(self.settings.screen_title)

        self.background = Background(self.settings, self.screen)

        self.welcome_board = WelcomeBoard(self.settings, self.screen, self)

        self.scoreboard = Scoreboard(self.settings, self.screen, self)

        self.victory_board = VictoryBoard(self.settings, self.screen, self)

        self.ball = Ball(self.settings, self.screen)
        self.scoreboard.set_ball(self.ball)

        self.initialize_players()

    def initialize_players(self):

        self.players = [
            Player(self.settings, self.screen, self.scoreboard),
            Player(self.settings, self.screen, self.scoreboard)
        ]
        self.player_left = self.players[0]
        self.player_right = self.players[1]

        self.scoreboard.set_players(self.player_left, self.player_right)

    def load_sounds(self):

        samples_dir = os.path.join("assets", "audio", "samples")

        self.sound_game_start = Sound(os.path.join(samples_dir, "GameStart.wav"))
        self.sound_game_end = Sound(os.path.join(samples_dir, "GameEnd.wav"))
        self.sound_you_lose = Sound(os.path.join(samples_dir, "Sad.wav"))

    def set_max_points(self, p):

        self.__points_max = p

        self.scoreboard.set_max_points(p)

    def start_ai_game(self):

        self.start_game()

        self.player_left.set_is_ai(True)
        self.player_right.set_is_ai(True)

        self.welcome_board.activate()

    def start_game(self):

        self.is_playing = True

        self.__round = 0

        self.player_left.set_score(0)
        self.player_left.make_left_side()
        self.time_since_left_player_human_input = 0
        self.player_left.set_is_ai(False)
        self.player_left.set_ai_difficulty(self.__ai_difficulty)

        self.player_right.set_score(0)
        self.player_right.make_right_side()
        self.time_since_right_player_human_input = 0
        self.player_right.set_is_ai(True)
        self.player_right.set_ai_difficulty(self.__ai_difficulty)

        self.welcome_board.deactivate()

        channel = pygame.mixer.find_channel()
        if channel:
            channel.play(self.sound_game_start)

        self.start_round()

    def end_game(self):

        self.is_playing = False
        self.time_since_last_game = 0

        self.scoreboard.dirty()

        #----------------------------------------#
        if self.player_left.get_score() > self.player_right.get_score():
            player_winner = self.player_left
        else:
            player_winner = self.player_right
        self.victory_board.set_winner(player_winner)

        #----------------------------------------#
        if not self.welcome_board.is_activated():
            self.victory_board.activate()

        #----------------------------------------#
        pygame.mixer.stop()
        channel = pygame.mixer.find_channel()
        if channel:
            channel.play(self.sound_game_end)

        #----------------------------------------#
        self.welcome_board.activate()

    def get_round(self):

        return self.__round

    def set_ai_difficulty(self, n):

        self.__ai_difficulty = n

    def start_round(self):

        #----------------------------------------#
        if self.player_left.get_score() >= self.__points_max:
            self.end_game()
            return
        if self.player_right.get_score() >= self.__points_max:
            self.end_game()
            return

        self.__round += 1

        #----------------------------------------#
        for p in self.players:
            p.prepare_for_round()

        #----------------------------------------#
        self.ball.reset()
        self.ball.init_start_velocity()

    def main_loop(self):

        while True:
            # ----------------------------------------#
            elapsed_ms = self.clock.tick()

            # ----------------------------------------#
            self.handle_game_state(elapsed_ms)
            self.handle_events()

            # ----------------------------------------#
            self.update_players(elapsed_ms)
            self.update_ball(elapsed_ms)
            self.update_background(elapsed_ms)
            self.update_victory_board(elapsed_ms)

            # ----------------------------------------#
            self.check_for_win()

            # ----------------------------------------#
            self.draw()

    def handle_game_state(self, elapsed_ms):

        if self.welcome_board.wants_to_play(True):
            self.set_max_points(self.welcome_board.get_selected_points_value())
            self.set_ai_difficulty(self.welcome_board.get_selected_difficulty_value())
            self.start_game()

        elif self.welcome_board.wants_to_play_ai(True):
            self.set_max_points(self.welcome_board.get_selected_points_value())
            self.set_ai_difficulty(self.welcome_board.get_selected_difficulty_value())
            self.start_ai_game()
            self.welcome_board.deactivate()

        elif (not self.is_playing) and self.settings.can_start_ai_game:
            self.time_since_last_game += elapsed_ms
            if self.time_since_last_game > self.settings.game_auto_ai_game_timeout:
                self.start_ai_game()

    def handle_events(self):

        #----------------------------------------#
        for event in pygame.event.get():

            # ----------------------------------------#
            if event.type == pygame.QUIT:
                sys.exit()

            # ----------------------------------------#
            elif self.welcome_board.handle_event(event):
                pass

            # ----------------------------------------#
            elif event.type == pygame.KEYUP or event.type == pygame.KEYDOWN:
                self.handle_keyboard_events(event)

    def handle_keyboard_events(self, event):

        if self.is_playing:
            if not self.welcome_board.is_activated():
                self.handle_keyboard_player_events(event)

        # Q for Quit
        if event.key == pygame.K_q:
            sys.exit(0)

    def handle_keyboard_player_events(self, event):

        # If there are two players, use W/A/S/D and UP/DOWN/LEFT/RIGHT
        if (not self.player_left.is_ai()) and (not self.player_right.is_ai()):
            left_up = pygame.K_w
            left_down = pygame.K_s
            left_left = pygame.K_a
            left_right = pygame.K_d
            #
            right_up = pygame.K_UP
            right_down = pygame.K_DOWN
            right_left = pygame.K_LEFT
            right_right = pygame.K_RIGHT
        else:
            left_up = pygame.K_UP
            left_down = pygame.K_DOWN
            left_left = pygame.K_LEFT
            left_right = pygame.K_RIGHT

            right_up = pygame.K_w
            right_down = pygame.K_s
            right_left = pygame.K_a
            right_right = pygame.K_d

        #----------------------------------------#
        if event.key == left_up:
            self.time_since_left_player_human_input = 0
            if self.player_left.is_ai():
                self.player_left.set_is_ai(False)
            if event.type == pygame.KEYUP:
                self.player_left.set_moving_up(False)
            elif event.type == pygame.KEYDOWN:
                self.player_left.set_moving_up(True)
        #----------------------------------------#
        if event.key == left_down:
            self.time_since_left_player_human_input = 0
            if self.player_left.is_ai():
                self.player_left.set_is_ai(False)
            if event.type == pygame.KEYUP:
                self.player_left.set_moving_down(False)
            elif event.type == pygame.KEYDOWN:
                self.player_left.set_moving_down(True)
        #----------------------------------------#
        if event.key == left_left:
            self.time_since_left_player_human_input = 0
            if self.player_left.is_ai():
                self.player_left.set_is_ai(False)
            if event.type == pygame.KEYUP:
                self.player_left.set_moving_left(False)
            elif event.type == pygame.KEYDOWN:
                self.player_left.set_moving_left(True)
        #----------------------------------------#
        if event.key == left_right:
            self.time_since_left_player_human_input = 0
            if self.player_left.is_ai():
                self.player_left.set_is_ai(False)
            if event.type == pygame.KEYUP:
                self.player_left.set_moving_right(False)
            elif event.type == pygame.KEYDOWN:
                self.player_left.set_moving_right(True)

        #----------------------------------------#
        if event.key == right_up:
            self.time_since_right_player_human_input = 0
            if self.player_right.is_ai():
                self.player_right.set_is_ai(False)
            if event.type == pygame.KEYUP:
                self.player_right.set_moving_up(False)
            elif event.type == pygame.KEYDOWN:
                self.player_right.set_moving_up(True)
        #----------------------------------------#
        if event.key == right_down:
            self.time_since_right_player_human_input = 0
            if self.player_right.is_ai():
                self.player_right.set_is_ai(False)
            if event.type == pygame.KEYUP:
                self.player_right.set_moving_down(False)
            elif event.type == pygame.KEYDOWN:
                self.player_right.set_moving_down(True)
        #----------------------------------------#
        if event.key == right_left:
            self.time_since_right_player_human_input = 0
            if self.player_right.is_ai():
                self.player_right.set_is_ai(False)
            if event.type == pygame.KEYUP:
                self.player_right.set_moving_left(False)
            elif event.type == pygame.KEYDOWN:
                self.player_right.set_moving_left(True)
        #----------------------------------------#
        if event.key == right_right:
            self.time_since_right_player_human_input = 0
            if self.player_right.is_ai():
                self.player_right.set_is_ai(False)
            if event.type == pygame.KEYUP:
                self.player_right.set_moving_right(False)
            elif event.type == pygame.KEYDOWN:
                self.player_right.set_moving_right(True)

    def update_players(self, elapsed_ms):

        if not self.is_playing:
            return

        self.time_since_left_player_human_input += elapsed_ms
        self.time_since_right_player_human_input += elapsed_ms

        #----------------------------------------#
        if self.player_left.is_ai() != self.player_right.is_ai():
            if self.player_left.is_ai():
                self.player_left.set_is_ai(False)
                self.player_right.set_is_ai(True)

        #
        for p in self.players:
            p.update(self.ball, elapsed_ms)

    def update_ball(self, elapsed_ms):

        if not self.is_playing:
            return

        self.ball.update(self.players, elapsed_ms)

    def check_for_win(self):

        if not self.is_playing:
            return

        x, y = self.ball.get_position()

        #----------------------------------------#
        if x < 0:
            self.player_wins_round(self.player_right)
        elif x > self.screen_rect.width:
            self.player_wins_round(self.player_left)

        #----------------------------------------#
        elif not (0 <= y < self.screen_rect.height):
            print("Ball out of bounds:", (x, y))
            half = self.screen_rect.width / 2
            if x > half:
                self.player_wins_round(self.player_left)
            else:
                self.player_wins_round(self.player_right)

    def update_background(self, elapsed_ms):

        self.background.update(elapsed_ms)

    def update_victory_board(self, elapsed_ms):

        self.victory_board.update(elapsed_ms)

    def player_wins_round(self, player):

        #
        print("Player:", player, " wins round!")

        player.adjust_score(1)
        self.scoreboard.dirty()

        channel = pygame.mixer.find_channel()
        if channel:
            channel.play(self.sound_you_lose)

        self.start_round()

    def draw(self):

        self.background.blitme()
        self.scoreboard.blitme()

        for p in self.players:
            p.blitme()

        self.ball.blitme()

        self.welcome_board.blitme()
        self.victory_board.blitme()

        pygame.display.flip()


if __name__ == "__main__":
    pong = Pong()