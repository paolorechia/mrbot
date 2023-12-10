from collections import deque

import pytest

from fishing_bot import Action, FishingBot, State
from game_state import GameState


@pytest.fixture(scope="function")
def n():
    return 15


@pytest.fixture(scope="function")
def game_state(n):
    state = GameState(n)
    state.catching_box_count_deque = deque([0 for _ in range(n)])
    state.percentage_deque = deque([0 for _ in range(n)])
    state.bait_count_deque = deque([1 for _ in range(n)])

    return state


@pytest.fixture(scope="function")
def bot(game_state):
    bot = FishingBot()
    bot.update_state(game_state)
    return bot


def test_game_state(game_state, n):
    assert game_state.is_fishing == False
    assert game_state.is_baited == False
    assert game_state.is_catching == False

    game_state.catching_box_count_deque = deque([0 for _ in range(n)])
    game_state.percentage_deque = deque([0 for _ in range(n)])
    game_state.bait_count_deque = deque([1 for _ in range(n)])

    game_state.update_state()

    assert game_state.is_fishing == True
    assert game_state.is_baited == False
    assert game_state.is_catching == False

    game_state.bait_count_deque = deque([0.7 for _ in range(n)])
    game_state.update_state()
    assert game_state.is_baited == True
    assert game_state.is_fishing == True
    assert game_state.is_catching == False

    game_state.catching_box_count_deque = deque([1.0 for _ in range(n)])
    game_state.update_state()
    assert game_state.is_baited == True
    assert game_state.is_fishing == True
    assert game_state.is_catching == True

    game_state.bait_count_deque = deque([0 for _ in range(n)])
    game_state.catching_box_count_deque = deque([0.0 for _ in range(n)])
    game_state.update_state()
    assert game_state.is_baited == False
    assert game_state.is_fishing == False
    assert game_state.is_catching == False


def test_bot_act(game_state: GameState, bot: FishingBot):
    bot.act(game_state)
    assert bot


def test_bot_noop(game_state: GameState, bot: FishingBot):
    game_state.frame_counter = 4
    bot.update_state(game_state)
    assert bot.decide_action() == Action.NOOP


def test_bot_start_fishing(game_state: GameState, bot: FishingBot):
    game_state.frame_counter = bot.cooldown_rate
    assert bot.decide_action() == Action.START_FISHING

    bot.act(game_state)
    assert bot.state == State.FISHING


def test_bot_start_catching(game_state: GameState, bot: FishingBot):
    game_state.frame_counter = bot.reaction_rate
    game_state.is_baited = True

    bot.state = State.FISHING
    assert bot.decide_action() == Action.START_CATCHING

    bot.act(game_state)
    assert bot.state == State.CATCHING


def test_bot_continue_catching(game_state: GameState, bot: FishingBot):
    game_state.frame_counter = bot.reaction_rate
    game_state.is_catching = True

    bot.state = State.CATCHING
    assert bot.decide_action() == Action.CONTINUE_CATCHING

    bot.act(game_state)
    assert bot.state == State.CATCHING


def test_bot_go_idle(game_state: GameState, bot: FishingBot):
    game_state.frame_counter = bot.cooldown_rate
    game_state.is_catching = False

    bot.tolerance_catching_frames = 10
    bot.state = State.CATCHING
    assert bot.decide_action() == Action.GO_IDLE

    bot.act(game_state)
    assert bot.state == State.IDLE
