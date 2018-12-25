
class Settings:

    def __init__(self):

        self.screen_title = "Pong with NO WALLS!"
        self.screen_width = 1280
        self.screen_height = 720
        self.screen_resize = 0.75

        #----------------------------------------#
        self.sound_sample_rate = 44100
        self.sound_channels = 20

        #----------------------------------------#
        self.background_color = (0, 0, 0)
        self.background_net_line_color = (100, 255, 0)
        self.background_net_line_width = 5
        self.background_net_line_spacing = 5

        #----------------------------------------#
        self.welcome_board_title = "Pong (Special Edition)"
        self.welcome_board_title_color = (100, 155, 100)
        self.welcome_board_subheading = "There's No Walls!"
        self.welcome_board_subheading_color = (255, 100, 0)
        self.welcome_board_size_factor = 0.75
        self.welcome_board_padding_border = 50
        self.welcome_board_padding_items = 10
        self.welcome_board_background_color = (50, 50, 50, 255)
        self.welcome_board_text_color = (100, 200, 200, 100)
        self.welcome_board_text_emphasized_color = (255, 0, 0, 255)
        self.welcome_board_opacity = 225
        self.welcome_board_play_button_width = 50
        self.welcome_board_play_button_height = 50
        self.welcome_board_play_button_text_color = (255, 255, 255)
        self.welcome_board_play_button_border_color = (255, 255, 255)
        self.welcome_board_play_button_border_width = 5
        self.welcome_board_play_button_background_color = (255, 0, 0)

        #----------------------------------------#
        self.game_auto_ai_game_timeout = 10000
        self.game_default_points = 7
        self.game_available_points_selections = [1, 3, 5]
        self.game_available_difficulty_selections = {
            0: "Beginner",
            1: "Medium",
            2: "Expert"
        }
        self.game_default_difficulty_value = 0

        #----------------------------------------#
        self.scoreboard_text_color = (200, 200, 200, 200)
        self.scoreboard_background_color = (10, 10, 10, 10)
        self.scoreboard_padding = 25

        #----------------------------------------#
        self.victory_board_max_activation_time_ms = 5000
        self.victory_board_size_factor = 0.8
        self.victory_board_title = "YOU WIN!"
        self.victory_board_title_color = (200, 200, 200, 0)
        self.victory_board_text_color = (150, 150, 150, 0)
        self.victory_board_background_color = (0, 0, 0, 150)
        self.victory_board_padding_border = 25
        self.victory_board_padding_items = 10

        #----------------------------------------#
        self.ball_radius = 10
        self.ball_color = (255, 250, 250, 255)
        self.ball_start_velocity_base = 0
        self.ball_start_velocity_std = .5
        self.ball_start_velocity_minimum = 0.1
        self.ball_speed_factor = 0.5
        self.ball_amok_dampening_factor = 0.9
        self.ball_can_bounce_wall = False
        self.ball_bounce_wall_velocity_increase_y = 0.01

        #----------------------------------------#
        self.can_start_ai_game = True
        self.player_ai_idle_time_to_ai = 10000
        self.player_ai_center_offset_think_delay = 3000
        self.player_ai_center_offset_think_delay_std = 500
        self.player_ai_difficulty_level_speed_increase = 2.0

        #----------------------------------------#
        self.paddle_wall_padding = 25
        self.paddle_length_short = 15
        self.paddle_length_long = 75
        self.paddle_color_base_human = (10, 10, 10, 200)
        self.paddle_color_border_human = (0, 200, 200, 200)
        self.paddle_color_base_ai = (100, 10, 10, 100)
        self.paddle_color_border_ai = (255, 10, 10, 100)
        self.paddle_border_width = 1
        self.paddle_speed_factor_human = 0.5
        self.paddle_speed_factor_ai = 0.2
        self.paddle_ball_bounce_velocity_increase = 0
        self.paddle_ball_bounce_velocity_influence_x = .1
        self.paddle_ball_bounce_velocity_influence_y = .1
        self.paddle_impact_energy_decay_factor = 0.99
        self.paddle_impact_zero = 0.01