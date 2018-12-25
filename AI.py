import random


class AI:

    def __init__(self, player, settings):

        self.player = player
        self.settings = settings

        self.delay_to_next_think_about_center_offsets = self.settings.player_ai_center_offset_think_delay
        self.time_since_think_about_center_offsets = 0
        self.last_desired_center_offset_x = 0
        self.last_desired_center_offset_y = 0

        self.__difficulty_value = self.settings.game_default_difficulty_value

    def set_difficulty(self, value):

        self.__difficulty_value = value

    def think(self, ball, elapsed_ms):

        self.think_about_center_offsets(elapsed_ms)

        #----------------------------------------#
        paddle_x = None
        paddle_y = None
        for p in self.player.paddles:
            if paddle_y is None and p.can_bounce_x():
                x, y = p.get_position()
                paddle_y = y
            if paddle_x is None and p.can_bounce_y():
                x, y = p.get_position()
                paddle_x = x

        #----------------------------------------#
        ball_velocity_x, ball_velocity_y = ball.get_velocity()
        ball_x, ball_y = ball.get_position()

        #----------------------------------------#
        offset_desired_y = self.last_desired_center_offset_y
        if ball_velocity_y > 0:
            offset_desired_y *= -1
        ball_y_with_offset = ball_y + offset_desired_y

        #----------------------------------------#
        offset_desired_x = self.last_desired_center_offset_x
        if ball_velocity_x > 0:
            offset_desired_x *= -1
        ball_x_with_offset = ball_x + offset_desired_x

        #----------------------------------------#
        move_x = 0
        move_y = 0

        #----------------------------------------#
        if ball_y_with_offset > paddle_y:
            move_y = 1
        elif ball_y_with_offset < paddle_y:
            move_y = -1

        #----------------------------------------#
        if ball_x_with_offset > paddle_x:
            move_x = 1
        elif ball_x_with_offset < paddle_x:
            move_x = -1

        speed = pow(self.settings.player_ai_difficulty_level_speed_increase, self.__difficulty_value)

        return move_x, move_y, speed

    def think_about_center_offsets(self, elapsed_ms):

        self.time_since_think_about_center_offsets += elapsed_ms
        if self.time_since_think_about_center_offsets < self.delay_to_next_think_about_center_offsets:
            return
        self.time_since_think_about_center_offsets = 0

        self.delay_to_next_think_about_center_offsets = random.normalvariate(
            self.settings.player_ai_center_offset_think_delay,
            self.settings.player_ai_center_offset_think_delay_std
        )

        self.think_about_center_offset_x()
        self.think_about_center_offset_y()

    def think_about_center_offset_x(self):

        #----------------------------------------#
        paddle = None
        for p in self.player.get_paddles():
            if p.can_bounce_y():
                paddle = p
                break

        #----------------------------------------#
        paddle_rect = paddle.get_rect()
        offset_max = int(paddle_rect.width / 2)
        self.last_desired_center_offset_x = random.randint(0, offset_max)

    def think_about_center_offset_y(self):

        #----------------------------------------#
        paddle = None
        for p in self.player.get_paddles():
            if p.can_bounce_x():
                paddle = p
                break

        #----------------------------------------#
        paddle_rect = paddle.get_rect()
        offset_max = int(paddle_rect.height / 2)
        self.last_desired_center_offset_y = random.randint(0, offset_max)