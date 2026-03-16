import random
import streamlit as st
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score  #FIX: moved game logic out of app.py into logic_utils.py for clean separation

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0  #FIX: changed initial value from 1 to 0 to match new game reset

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("Make a guess")

st.info(
    f"Guess a number between 1 and 100. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

show_hint = st.checkbox("Show hint", value=True)  #FIX: moved outside form so it toggles without requiring a submit click

with st.form("guess_form"):  #FIX: wrapped input and buttons in st.form to prevent double-click bug caused by text_input blur triggering a rerun before button click registers
    raw_guess = st.text_input(
        "Enter your guess:",
        key=f"guess_input_{difficulty}"
    )
    col1, col2 = st.columns(2)
    with col1:
        submit = st.form_submit_button("Submit Guess 🚀")
    with col2:
        new_game_form = st.form_submit_button("New Game 🔁")

new_game = new_game_form

if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)  #FIX: changed from hardcoded randint(1,100) to use difficulty range
    st.session_state.status = "playing"  #FIX: added missing status reset so game is no longer stuck after win/loss
    st.session_state.history = []  #FIX: added missing history reset
    st.session_state.score = 0  #FIX: added missing score reset
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        outcome, message = check_guess(guess_int, st.session_state.secret)  #FIX: removed odd/even type-switching that passed secret as str on even attempts, causing broken lexicographic comparisons

        if show_hint:
            st.warning(message)  #FIX: hint messages were inverted ("Go HIGHER" when too high, "Go LOWER" when too low) — fixed in logic_utils.check_guess

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
