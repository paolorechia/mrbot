from collections import deque

from fishing_bot import FishingBot
from game_state import GameState


def test_game_state():
    n = 15
    game_state = GameState(n)

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


def test_bot():
    game_state = GameState(15)
    bot = FishingBot()
    bot.take_action(game_state)
