import random
from logic_utils import check_guess, parse_guess, update_score, get_range_for_difficulty


def simulate_new_game(state: dict, low: int, high: int) -> dict:
    """Mirrors the new_game block in app.py."""
    state["attempts"] = 0
    state["secret"] = random.randint(low, high)
    state["status"] = "playing"
    state["history"] = []
    state["score"] = 0
    return state


def test_new_game_resets_status_after_win():
    state = {"attempts": 5, "secret": 42, "status": "won", "history": [10, 42], "score": 80}
    result = simulate_new_game(state, 1, 100)
    assert result["status"] == "playing"


def test_new_game_resets_status_after_loss():
    state = {"attempts": 8, "secret": 77, "status": "lost", "history": [1, 2, 3], "score": -10}
    result = simulate_new_game(state, 1, 100)
    assert result["status"] == "playing"


def test_new_game_resets_attempts_history_score():
    state = {"attempts": 6, "secret": 30, "status": "lost", "history": [5, 20, 30], "score": 50}
    result = simulate_new_game(state, 1, 100)
    assert result["attempts"] == 0
    assert result["history"] == []
    assert result["score"] == 0


def test_new_game_secret_within_difficulty_range():
    state = {"attempts": 3, "secret": 10, "status": "won", "history": [], "score": 70}
    for _ in range(20):  # run several times to catch range violations
        result = simulate_new_game(state.copy(), 1, 20)
        assert 1 <= result["secret"] <= 20


def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"
