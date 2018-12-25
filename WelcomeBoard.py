
import pygame
from pygame import Surface
from pygame import Rect

from OverlayBoard import OverlayBoard


class WelcomeBoard(OverlayBoard):

    def __init__(self, settings, screen, pong):

        super().__init__(settings, screen, pong)

        #----------------------------------------#
        width = int(self.screen_rect.width * self.settings.welcome_board_size_factor)
        height = int(self.screen_rect.height * self.settings.welcome_board_size_factor)
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

        self.image_play_button = None
        self.image_play_button_rect = None
        self.image_play_button_ai = None
        self.image_play_button_ai_rect = None

        #
        self.title_rect = None

        self.points_selections_with_rects = None
        self.__selected_points_value = self.settings.game_default_points

        self.difficulty_selections_with_rects = None
        self.__selected_difficulty_value = self.settings.game_default_difficulty_value

        self.__wants_to_play = False
        self.__wants_to_play_ai = False

        self.set_opacity(self.settings.welcome_board_opacity)

    def wants_to_play(self, do_clear):

        if self.__wants_to_play:
            if do_clear:
                self.__wants_to_play = False
            return True

        return False

    def wants_to_play_ai(self, do_clear):

        if self.__wants_to_play_ai:
            if do_clear:
                self.__wants_to_play_ai = False
            return True

        return False

    def set_selected_points_value(self, v):

        print("Welcome board: Setting selected points value to:", v)
        self.__selected_points_value = v

        self.dirty()

    def set_selected_difficulty_value(self, v):

        print("Welcome board: Setting selected difficulty value to:", v)
        self.__selected_difficulty_value = v

        self.dirty()

    def get_selected_points_value(self):

        return self.__selected_points_value

    def get_selected_difficulty_value(self):

        return self.__selected_difficulty_value

    def handle_event(self, event):

        if self.handle_click_points_selection(event):
            return True

        if self.handle_click_difficulty_selection(event):
            return True

        if self.handle_click_play_buttons(event):
            return True

    def handle_click_play_buttons(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            # ----------------------------------------#
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_x -= self.rect.left
            mouse_y -= self.rect.top

            # ----------------------------------------#
            bound_left = self.image_play_button_rect.left
            bound_right = self.image_play_button_rect.left + self.image_play_button_rect.width
            bound_top = self.image_play_button_rect.top
            bound_bottom = self.image_play_button_rect.top + self.image_play_button_rect.height
            if (
                    bound_left <= mouse_x <= bound_right
                    and bound_top <= mouse_y <= bound_bottom
            ):
                self.__wants_to_play = True
                return True

            # ----------------------------------------#
            bound_left = self.image_play_button_ai_rect.left
            bound_right = self.image_play_button_ai_rect.left + self.image_play_button_ai_rect.width
            bound_top = self.image_play_button_ai_rect.top
            bound_bottom = self.image_play_button_ai_rect.top + self.image_play_button_ai_rect.height
            if (
                    bound_left <= mouse_x <= bound_right
                    and bound_top <= mouse_y <= bound_bottom
            ):
                self.__wants_to_play_ai = True
                return True

        return False

    def handle_click_points_selection(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_x -= self.rect.left
            mouse_y -= self.rect.top

            # ----------------------------------------#
            for item in self.points_selections_with_rects:

                points, rect = item

                if(
                        rect.left <= mouse_x <= rect.left + rect.width
                        and rect.top <= mouse_y <= rect.top + rect.height
                ):
                    self.set_selected_points_value(points)

                    return True

        return False

    def handle_click_difficulty_selection(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_x -= self.rect.left
            mouse_y -= self.rect.top

            # ----------------------------------------#
            for item in self.difficulty_selections_with_rects:

                difficulty_value, rect = item

                if (
                        rect.left <= mouse_x <= rect.left + rect.width
                        and rect.top <= mouse_y <= rect.top + rect.height
                ):
                    self.set_selected_difficulty_value(difficulty_value)

                    return True

        return False

    def update(self, elapsed_me):

        super().update(elapsed_me)

    def draw(self):

        super().draw()

        #----------------------------------------#
        self.image.fill(self.settings.welcome_board_background_color, None)

        y = 0
        y = self.draw_title(y)
        y = self.draw_info(y)
        y = self.draw_points_selection(y)
        y = self.draw_difficulty_selection(y)
        self.draw_play_buttons(y)

        self.draw_adjust_opacity()

    def draw_title(self, y):

        # Draw the main title
        image = self.font_huge.render(
            self.settings.welcome_board_title, True,
            self.settings.welcome_board_title_color, self.settings.welcome_board_background_color
        )
        image_rect = image.get_rect()
        #
        x = int(
            (self.rect.width / 2) - (image_rect.width / 2)
        )
        y += self.settings.welcome_board_padding_border
        self.image.blit(image, (x, y))
        y += image_rect.height + self.settings.welcome_board_padding_items

        # Draw the subheading
        image = self.font_large.render(
            self.settings.welcome_board_subheading, True,
            self.settings.welcome_board_subheading_color, self.settings.welcome_board_background_color
        )
        image_rect = image.get_rect()
        x = int(
            (self.rect.width / 2) - (image_rect.width / 2)
        )
        self.image.blit(image, (x, y))
        y += image_rect.height + self.settings.welcome_board_padding_items

        return y

    def draw_info(self, y):

        lines = [
            "Player 1: Up / Down / Left / Right",
            "Player 2: W / S / A / D"
        ]

        x = int(
            self.settings.welcome_board_padding_border
        )

        for line in lines:
            image = self.font_small.render(
                line, True,
                self.settings.welcome_board_text_color, self.settings.welcome_board_background_color
            )
            image_rect = image.get_rect()
            self.image.blit(image, (x, y))
            y += image_rect.height + self.settings.welcome_board_padding_items

        return y

    def draw_points_selection(self, y):

        max_height = 0

        #----------------------------------------#
        text = "Play up to: "
        x = self.settings.welcome_board_padding_border
        image = self.font_small.render(
            text, True,
            self.settings.welcome_board_text_color, self.settings.welcome_board_background_color
        )
        image_rect = image.get_rect()
        self.image.blit(image, (x, y))
        x += image_rect.width
        if image_rect.height > max_height:
            max_height = image_rect.height

        #----------------------------------------#
        self.points_selections_with_rects = []
        for value in self.settings.game_available_points_selections:
            text = str(value) + " "
            if value == self.__selected_points_value:
                color = self.settings.welcome_board_text_emphasized_color
            else:
                color = self.settings.welcome_board_text_color
            image = self.font_small.render(
                text, True,
                color, self.settings.welcome_board_background_color
            )
            image_rect = image.get_rect()
            image_rect.left = x
            image_rect.top = y
            self.points_selections_with_rects.append((value, image_rect))
            self.image.blit(image, (x, y))
            x += image_rect.width
            if image_rect.height > max_height:
                max_height = image_rect.height

        #----------------------------------------#
        text = " points (click)"
        image = self.font_small.render(
            text, True,
            self.settings.welcome_board_text_color, self.settings.welcome_board_background_color
        )
        image_rect = image.get_rect()
        self.image.blit(image, (x, y))
        if image_rect.height > max_height:
            max_height = image_rect.height

        y += max_height + self.settings.welcome_board_padding_items

        return y

    def draw_difficulty_selection(self, y):

        max_height = 0

        #----------------------------------------#
        text = "Select difficulty: "
        x = self.settings.welcome_board_padding_border
        image = self.font_small.render(
            text, True,
            self.settings.welcome_board_text_color, self.settings.welcome_board_background_color
        )
        image_rect = image.get_rect()
        self.image.blit(image, (x, y))
        x += image_rect.width
        if image_rect.height > max_height:
            max_height = image_rect.height

        #----------------------------------------#
        self.difficulty_selections_with_rects = []
        for difficulty_value in self.settings.game_available_difficulty_selections.keys():

            difficulty_text = self.settings.game_available_difficulty_selections[difficulty_value]

            text = difficulty_text + " "
            if difficulty_value == self.__selected_difficulty_value:
                color = self.settings.welcome_board_text_emphasized_color
            else:
                color = self.settings.welcome_board_text_color
            image = self.font_small.render(
                text, True,
                color, self.settings.welcome_board_background_color
            )
            image_rect = image.get_rect()
            image_rect.left = x
            image_rect.top = y
            self.difficulty_selections_with_rects.append((difficulty_value, image_rect))
            self.image.blit(image, (x, y))
            x += image_rect.width
            if image_rect.height > max_height:
                max_height = image_rect.height

        #----------------------------------------#
        text = " (click)"
        image = self.font_small.render(
            text, True,
            self.settings.welcome_board_text_color, self.settings.welcome_board_background_color
        )
        image_rect = image.get_rect()
        self.image.blit(image, (x, y))
        if image_rect.height > max_height:
            max_height = image_rect.height

        y += max_height + self.settings.welcome_board_padding_items

        return y

    def draw_play_buttons(self, y):

        #----------------------------------------#
        image_text_normal = self.font_large.render(
            "Play", True,
            self.settings.welcome_board_play_button_text_color, self.settings.welcome_board_play_button_background_color
        )
        image_text_normal_rect = image_text_normal.get_rect()

        #----------------------------------------#
        image_text_ai = self.font_large.render(
            "Watch (AI Only)", True,
            self.settings.welcome_board_play_button_text_color, self.settings.welcome_board_play_button_background_color
        )
        image_text_ai_rect = image_text_ai.get_rect()

        #----------------------------------------#
        if not self.image_play_button:
            self.image_play_button = Surface(
                (
                    image_text_normal_rect.width + (self.settings.welcome_board_padding_items * 2),
                    image_text_normal_rect.height + (self.settings.welcome_board_padding_items * 2)
                ),
                0, self.screen
            )
            self.image_play_button_rect = self.image_play_button.get_rect()
        if not self.image_play_button_ai:
            self.image_play_button_ai = Surface(
                (
                    image_text_ai_rect.width + (self.settings.welcome_board_padding_items * 2),
                    image_text_ai_rect.height + (self.settings.welcome_board_padding_items * 2)
                ),
                0, self.screen
            )
            self.image_play_button_ai_rect = self.image_play_button_ai.get_rect()

        #----------------------------------------#
        self.image_play_button.fill(self.settings.welcome_board_play_button_background_color, None)
        self.image_play_button_ai.fill(self.settings.welcome_board_play_button_background_color, None)

        #----------------------------------------#
        pygame.draw.rect(
            self.image_play_button,
            self.settings.welcome_board_play_button_border_color,
            Rect(0, 0, self.image_play_button_rect.width, self.image_play_button_rect.height),
            self.settings.welcome_board_play_button_border_width
        )
        pygame.draw.rect(
            self.image_play_button_ai,
            self.settings.welcome_board_play_button_border_color,
            Rect(0, 0, self.image_play_button_ai_rect.width, self.image_play_button_ai_rect.height),
            self.settings.welcome_board_play_button_border_width
        )

        #----------------------------------------#
        self.image_play_button.blit(
            image_text_normal,
            (
                int((self.image_play_button_rect.width - image_text_normal_rect.width) / 2),
                int((self.image_play_button_rect.height - image_text_normal_rect.height) / 2)
            )
        )
        self.image_play_button_ai.blit(
            image_text_ai,
            (
                int((self.image_play_button_ai_rect.width - image_text_ai_rect.width) / 2),
                int((self.image_play_button_ai_rect.height - image_text_ai_rect.height) / 2)
            )
        )

        #----------------------------------------#
        x = self.settings.welcome_board_padding_border
        self.image.blit(self.image_play_button, (x, y))
        self.image_play_button_rect.left = x
        self.image_play_button_rect.top = y

        #----------------------------------------#
        x += self.image_play_button_rect.width + self.settings.welcome_board_padding_items
        self.image.blit(self.image_play_button_ai, (x, y))
        self.image_play_button_ai_rect.left = x
        self.image_play_button_ai_rect.top = y

        y += (
                max(self.image_play_button_rect.height, self.image_play_button_ai_rect.height)
                + self.settings.welcome_board_padding_items
        )

        return y