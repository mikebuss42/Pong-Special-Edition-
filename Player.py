
from AI import AI
from Paddle import Paddle


class Player:

    def __init__(self, settings, screen, scoreboard):

        super().__init__()

        self.settings = settings
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.scoreboard = scoreboard

        self.__label = None

        self.__moving_up = None
        self.__moving_down = None
        self.__moving_left = None
        self.__moving_right = None

        self.paddles = None

        self.__is_ai = False
        self.ai = AI(self, settings)

        self.__score = 0

        self.reset()

    def __str__(self):

        s = ""

        s += "Pong Player: " + self.get_label()

        if self.is_ai():
            s += " (AI)"

        return s

    def reset(self):

        self.paddles = []

        self.prepare_for_round()

    def set_label(self, l):

        self.__label = l

    def get_label(self):

        if self.__label:
            return self.__label

        return "[no label]"

    def prepare_for_round(self):

        self.__moving_up = False
        self.__moving_down = False
        self.__moving_left = False
        self.__moving_right = False

    def set_is_human(self, b):

        self.set_is_ai(not b)

    def is_human(self):

        return not self.is_ai()

    def set_is_ai(self, b):

        self.__is_ai = b

        if b:
            speed = self.settings.paddle_speed_factor_ai
            color_base = self.settings.paddle_color_base_ai
            color_border = self.settings.paddle_color_border_ai
        else:
            speed = self.settings.paddle_speed_factor_human
            color_base = self.settings.paddle_color_base_human
            color_border = self.settings.paddle_color_border_human

        self.__moving_up = False
        self.__moving_down = False
        self.__moving_left = False
        self.__moving_right = False

        for paddle in self.paddles:
            paddle.set_speed(speed)
            paddle.set_base_color(color_base)
            paddle.set_border_color(color_border)
            paddle.draw(True)

    def is_ai(self):

        return self.__is_ai

    def make_left_side(self):

        self.paddles = []

        self.set_label("Left Player")

        # Left paddle
        paddle_left = Paddle(self, self.settings, self.screen)
        paddle_left.make_left_side()
        self.paddles.append(paddle_left)

        # Top paddle
        paddle_top = Paddle(self, self.settings, self.screen)
        paddle_top.make_top_left_side()
        self.paddles.append(paddle_top)

        # Bottom paddle
        paddle_bottom = Paddle(self, self.settings, self.screen)
        paddle_bottom.make_bottom_left_side()
        self.paddles.append(paddle_bottom)

    def make_right_side(self):

        self.paddles = []

        self.set_label("Right Player")

        # Right paddle
        paddle_right = Paddle(self, self.settings, self.screen)
        paddle_right.make_right_side()
        self.paddles.append(paddle_right)

        # Top paddle
        paddle_top = Paddle(self, self.settings, self.screen)
        paddle_top.make_top_right_side()
        self.paddles.append(paddle_top)

        # Bottom paddle
        paddle_bottom = Paddle(self, self.settings, self.screen)
        paddle_bottom.make_bottom_right_side()
        self.paddles.append(paddle_bottom)

    def set_moving_up(self, b):

        self.__moving_up = b

    def set_moving_down(self, b):

        self.__moving_down = b

    def set_moving_left(self, b):

        self.__moving_left = b

    def set_moving_right(self, b):

        self.__moving_right = b

    def get_paddles(self):

        return self.paddles

    def set_score(self, s):

        self.__score = s

        self.scoreboard.dirty()

    def adjust_score(self, a):

        self.set_score(self.__score + a)

    def get_score(self):

        return self.__score

    def set_ai_difficulty(self, v):

        self.ai.set_difficulty(v)

    def update(self, ball, elapsed_ms):

        self.move_paddles(ball, elapsed_ms)

        for paddle in self.paddles:
            paddle.update(elapsed_ms)

    def move_paddles(self, ball, elapsed_ms):

        move_x = 0
        move_y = 0
        move_speed = 1

        # Move by AI
        if self.__is_ai:

            move_x, move_y, move_speed = self.ai.think(ball, elapsed_ms)

        # Move by Human Input
        else:

            # Move up or down
            if self.__moving_up != self.__moving_down:
                if self.__moving_up:
                    move_y = -1
                else:
                    move_y = 1

            # Move left or right
            if self.__moving_left != self.__moving_right:
                if self.__moving_left:
                    move_x = -1
                else:
                    move_x = 1

        #
        for paddle in self.paddles:
            paddle.move(move_x, move_y, move_speed, elapsed_ms)

    def blitme(self):

        for paddle in self.paddles:
            paddle.blitme()