from game_state import GameState
from mouse import (
    mouseup,
    mousedown,
    move_mouse_to_default_spot,
    slow_click_random,
    click,
)

class FishingBot:
    def __init__(self, reaction_rate = 5) -> None:
        self.reaction_rate = reaction_rate
        self.cooldown_rate = self.reaction_rate * 10
        self.is_fishing_cooldown = False


    def take_action(self, game_state: GameState):
        if game_state.frame_counter % self.cooldown_rate == 0:
            self.is_fishing_cooldown = False

        if game_state.frame_counter % self.reaction_rate == 0:            
            if not game_state.is_fishing and not self.is_fishing_cooldown:
                self.start_fishing()

            if game_state.is_baited and not game_state.is_catching:
                self.start_catching()

            if game_state.is_catching:
                self.handle_catch(game_state)

    def handle_catch(self, game_state: GameState):
        if game_state.percentage < 0.2:
            move_mouse_to_default_spot()
            mousedown()
        if game_state.percentage > 0.5:
            move_mouse_to_default_spot()
            mouseup()

    def start_catching(self):
        move_mouse_to_default_spot()
        click()

    def start_fishing(self):
        move_mouse_to_default_spot()
        slow_click_random()
        self.is_fishing_cooldown = True