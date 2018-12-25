
import os
import random

import pygame
from pygame import Surface
from pygame.sprite import Sprite
from pygame.sprite import Group
from pygame import Rect
from pygame.mixer import Sound


class Ball(Sprite):

    #
    def __init__(self, settings, screen):

        super().__init__()

        self.settings = settings
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.image = None

        self.radius = None
        self.rect = None
        self.x = None
        self.y = None

        self.velocity_x = None
        self.velocity_y = None

        self.sound_bounce_paddle = None
        self.sound_bounce_wall = None
        self.load_sounds()

        self.reset()

    def reset(self):

        self.radius = self.settings.ball_radius

        self.x = self.screen_rect.width / 2
        self.y = self.screen_rect.height / 2
        self.rect = Rect(
            int(self.x - self.radius), int(self.y - self.radius),
            int(self.radius * 2), int(self.radius * 2)
        )

        self.velocity_x = 0
        self.velocity_y = 0

        self.draw()

    def load_sounds(self):

        dir_samples = os.path.join("assets/audio/samples")
        self.sound_bounce_paddle = Sound(os.path.join(dir_samples, "Blip1.wav"))
        self.sound_bounce_wall = Sound(os.path.join(dir_samples, "Blip2.wav"))

    def get_position(self):

        return self.x, self.y

    def init_start_velocity(self):

        # Launch the ball off in a random direction
        velocity_x = random.uniform(self.settings.ball_start_velocity_base, self.settings.ball_start_velocity_std)
        velocity_y = random.uniform(self.settings.ball_start_velocity_base, self.settings.ball_start_velocity_std)

        # Enforce minimums
        if 0 < velocity_x < self.settings.ball_start_velocity_minimum:
            velocity_x = self.settings.ball_start_velocity_minimum
        elif 0 > velocity_x > -self.settings.ball_start_velocity_minimum:
            velocity_x = -self.settings.ball_start_velocity_minimum
        #
        if 0 < velocity_y < self.settings.ball_start_velocity_minimum:
            velocity_y = self.settings.ball_start_velocity_minimum
        elif 0 > velocity_y > -self.settings.ball_start_velocity_minimum:
            velocity_y = -self.settings.ball_start_velocity_minimum

        self.set_velocity(velocity_x, velocity_y)

    def get_velocity(self):

        return self.velocity_x, self.velocity_y

    def set_velocity(self, x, y):

        self.velocity_x = x
        self.velocity_y = y

    def add_velocity(self, x, y):

        self.velocity_x += x
        self.velocity_y += y

    def update(self, players, elapsed_ms):

        self.handle_bouncing(players)

        x_change = self.velocity_x * self.settings.ball_speed_factor * elapsed_ms
        y_change = self.velocity_y * self.settings.ball_speed_factor * elapsed_ms

        # Keep changes bound to the ball's radius
        if x_change > self.radius:
            x_change = self.radius
            self.velocity_x *= self.settings.ball_amok_dampening_factor
        elif x_change < -self.radius:
            x_change = -self.radius
            self.velocity_x *= self.settings.ball_amok_dampening_factor
        if y_change > self.radius:
            y_change = self.radius
            self.velocity_y *= self.settings.ball_amok_dampening_factor
        elif y_change < -self.radius:
            y_change = -self.radius
            self.velocity_y *= self.settings.ball_amok_dampening_factor

        self.x += x_change
        self.y += y_change

        self.rect.left = self.x - self.radius
        self.rect.top = self.y - self.radius

    def handle_bouncing(self, players):

        self.handle_ball_paddle_bounces(players)
        self.handle_ball_wall_bounces()

    def handle_ball_paddle_bounces(self, players):

        paddles = Group()
        for player in players:
            for paddle in player.get_paddles():
                paddles.add(paddle)

        collisions = pygame.sprite.groupcollide(paddles, Group(self), False, False)
        for paddle in collisions:

            paddle_x, paddle_y = paddle.get_position()
            paddle_velocity_x, paddle_velocity_y = paddle.get_velocity()
            paddle_rect = paddle.get_rect()

            # ----------------------------------------#
            if paddle.can_bounce_x():
                if paddle_x < self.x and self.velocity_x > 0:
                    continue
                if self.x < paddle_x and self.velocity_x < 0:
                    continue

            # ----------------------------------------#
            if paddle.can_bounce_y():
                if paddle_y < self.y and self.velocity_y > 0:
                    continue
                if self.y < paddle_y and self.velocity_y < 0:
                    continue

            # ----------------------------------------#
            if paddle.can_bounce_x():

                # ----------------------------------------#
                paddle.receive_impact(self.velocity_x, self.velocity_y)

                # ----------------------------------------#
                self.velocity_x *= -1

                # ----------------------------------------#
                if self.velocity_x > 0:
                    self.velocity_x += self.settings.paddle_ball_bounce_velocity_increase
                else:
                    self.velocity_x -= self.settings.paddle_ball_bounce_velocity_increase

                # ----------------------------------------#
                difference_y = self.y - paddle_y
                influence_power = difference_y / (paddle_rect.height / 2)
                self.velocity_y += influence_power * self.settings.paddle_ball_bounce_velocity_influence_y

                # ----------------------------------------#
                self.velocity_y += paddle_velocity_y

            # ----------------------------------------#
            if paddle.can_bounce_y():

                paddle.receive_impact(self.velocity_x, self.velocity_y)

                self.velocity_y *= -1

                if self.velocity_y > 0:
                    self.velocity_y += self.settings.paddle_ball_bounce_velocity_increase
                else:
                    self.velocity_y -= self.settings.paddle_ball_bounce_velocity_increase

                difference_x = self.x - paddle_x
                influence_power = difference_x / (paddle_rect.width / 2)
                self.velocity_x += influence_power * self.settings.paddle_ball_bounce_velocity_influence_x

                self.velocity_x += paddle_velocity_x

            # ----------------------------------------#
            channel = pygame.mixer.find_channel()
            if channel:
                channel.play(self.sound_bounce_paddle)

    def handle_ball_wall_bounces(self):

        #----------------------------------------#
        did_bounce = False
        if not self.settings.ball_can_bounce_wall:
            return

        #----------------------------------------#
        if self.y < 0 and self.velocity_y < 0:
            self.velocity_y *= -1
            self.velocity_y += self.settings.ball_bounce_wall_velocity_increase_y
            did_bounce = True
        elif self.y > self.screen_rect.height and self.velocity_y > 0:
            self.velocity_y *= -1
            self.velocity_y -= self.settings.ball_bounce_wall_velocity_increase_y
            did_bounce = True

        #----------------------------------------#
        if did_bounce:
            channel = pygame.mixer.find_channel()
            if channel:
                channel.play(self.sound_bounce_wall)

    def draw(self):

        if not self.image:
            self.image = Surface(
                (self.radius * 2, self.radius * 2),
                pygame.SRCALPHA,
                self.screen
            )

        #----------------------------------------#
        self.image.fill((255, 0, 0, 0))

        #----------------------------------------#
        circle_x = int(self.rect.width / 2)
        circle_y = int(self.rect.height / 2)
        pygame.draw.circle(
            self.image,
            self.settings.ball_color,
            (circle_x, circle_y),
            self.radius,
            0
        )

    def blitme(self):

        self.screen.blit(
            self.image,
            (self.rect.left, self.rect.top)
        )