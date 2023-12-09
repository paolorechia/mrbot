from game_state import GameState
from mouse import (
    click,
    mousedown,
    mouseup,
    move_mouse_to_default_spot,
    slow_click_random,
)


class Action:
    START_FISHING = 1
    START_CATCHING = 2
    CONTINUE_CATCHING = 3
    GO_IDLE = 4
    NOOP = 5


class State:
    IDLE = 1
    FISHING = 2
    CATCHING = 3


class FishingBot:
    def __init__(self, reaction_rate=5) -> None:
        self.reaction_rate = reaction_rate
        self.cooldown_rate = self.reaction_rate * 10
        self.state = State.IDLE
        self.is_in_cooldown = False

    def update_state(self, game_state: GameState):
        self.game_state = game_state

    def act(self, game_state: GameState):
        self.update_state(game_state)
        action = self.decide_action()
        self.execute_action(action)

    def decide_action(self) -> str:
        # Avoid taking too many repeated actions in small amount of time
        if self.game_state.frame_counter % self.cooldown_rate == 0:
            self.is_in_cooldown = False

        if self.is_in_cooldown:
            return Action.NOOP

        # Avoid taking too many actions in a small amount of time
        if self.game_state.frame_counter % self.reaction_rate == 0:
            if self.state == State.IDLE and not self.is_in_cooldown:
                return Action.START_FISHING

            if self.state == State.FISHING and self.game_state.is_baited:
                return Action.START_CATCHING

            if self.state == State.CATCHING and self.game_state.is_catching:
                return Action.CONTINUE_CATCHING

            if self.state == State.CATCHING and not self.game_state.is_catching:
                return Action.GO_IDLE

        return Action.NOOP

    def execute_action(self, action):
        if action == Action.NOOP:
            return

        if action == Action.GO_IDLE:
            self.state = State.IDLE

        if action == Action.START_FISHING:
            self.start_fishing()
            self.state = State.FISHING
            self.is_in_cooldown = True

        if action == Action.START_CATCHING:
            self.start_catching()
            self.state = State.CATCHING
            self.is_in_cooldown = False

        if action == Action.CONTINUE_CATCHING:
            self.handle_catch(self.game_state)

    def handle_catch(self):
        if self.game_state.percentage < 0.5:
            move_mouse_to_default_spot()
            mousedown()
        if self.game_state.percentage > 0.8:
            move_mouse_to_default_spot()
            mouseup()

    def start_catching(self):
        move_mouse_to_default_spot()
        click()

    def start_fishing(self):
        move_mouse_to_default_spot()
        slow_click_random()
