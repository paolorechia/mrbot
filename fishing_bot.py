from game_state import GameState
from mouse import (
    click,
    mousedown,
    mouseup,
    move_mouse_to_default_spot,
    slow_click_random,
)
from capture_screenshot import take_screenshot


class Action:
    START_FISHING = "START_FISHING"
    START_CATCHING = "START_CATCHING"
    CONTINUE_CATCHING = "CONTINUE_CATCHING"
    GO_IDLE = "GO_IDLE"
    NOOP = "NOOP"
    RESET_COOLDOWN = "RESET_COOLDOWN"


class State:
    IDLE = "IDLE"
    FISHING = "FISHING"
    CATCHING = "CATCHING"


class FishingBot:
    def __init__(self, reaction_rate=5) -> None:
        self.reaction_rate = reaction_rate
        self.fishing_cooldown_rate = reaction_rate * 10
        self.catching_cooldown_rate = reaction_rate * 5
        self.fishing_frames = 0
        self.max_fishing_frames = 2000
        self.state = State.IDLE

    def update_state(self, game_state: GameState):
        self.game_state = game_state

    def act(self, game_state: GameState):
        self.update_state(game_state)
        action = self.decide_action()
        print("\33]K action: ", action)
        self.execute_action(action)

    def decide_action(self) -> str:
        if self.state == State.FISHING:
            self.fishing_frames += 1
        else:
            self.fishing_frames = 0

        if self.fishing_frames > self.max_fishing_frames:
            return Action.GO_IDLE
         
        if self.state == State.CATCHING and self.game_state.is_catching:
            return Action.CONTINUE_CATCHING
        
        # Avoid taking too many repeated actions in small amount of time
        if self.game_state.frame_counter % self.reaction_rate == 0:
            if self.state == State.FISHING and self.game_state.is_baited:
                return Action.START_CATCHING

        if self.game_state.frame_counter % self.catching_cooldown_rate == 0:
            if self.state == State.CATCHING and not self.game_state.is_catching:
                return Action.GO_IDLE

        # Avoid taking changing state too many times in a small amount of time
        if self.game_state.frame_counter % self.fishing_cooldown_rate == 0:
            # Fix yourself if game state tells otherwise
            if self.state == State.IDLE and self.game_state.is_fishing:
                self.state = State.FISHING
                return Action.NOOP

            if self.state == State.IDLE:
                return Action.START_FISHING

            if self.state == State.FISHING and not self.game_state.is_fishing and not self.game_state.is_baited:
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

        if action == Action.START_CATCHING:
            self.start_catching()
            self.state = State.CATCHING

        if action == Action.CONTINUE_CATCHING:
            self.handle_catch()

    def handle_catch(self):
        if self.game_state.percentage <= 0.5:
            move_mouse_to_default_spot()
            mousedown()
        if self.game_state.percentage >= 0.6:
            move_mouse_to_default_spot()
            mouseup()

        # if self.game_state.frame_counter % self.reaction_rate == 0:
            # take_screenshot()

    def start_catching(self):
        take_screenshot()
        move_mouse_to_default_spot()
        click()
        self.tolerance_catching_frames = 0

    def start_fishing(self):
        move_mouse_to_default_spot()
        slow_click_random()
