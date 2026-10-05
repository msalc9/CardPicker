import os
import random
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Card Game Simulator", page_icon="🃏", layout="centered")

# Mappings for ranks and suits
SUITS = ["S", "H", "D", "C"]  # Spades, Hearts, Diamonds, Clubs
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
SUIT_NAMES = {"S": "Spades", "H": "Hearts", "D": "Diamonds", "C": "Clubs"}


def create_deck():
    """Generates a fresh standard 52-card deck."""
    return [{"rank": r, "suit": s, "image": f"{r}{s}.png"} for s in SUITS for r in RANKS]


def check_win(card, game_mode):
    """Evaluates win condition based on selected game mode."""
    if game_mode == "Red Head":
        # Red Head: Red Suit (Hearts/Diamonds) + Picture heads (J, Q, K)
        return card["suit"] in ["H", "D"] and card["rank"] in ["J", "Q", "K"]
    elif game_mode == "Lucky Jack":
        # Lucky Jack: Black Suit (Spades/Clubs) + Jack (J)
        return card["suit"] in ["S", "C"] and card["rank"] == "J"
    return False


# Initialize session state
if "deck" not in st.session_state:
    st.session_state.deck = create_deck()
    random.shuffle(st.session_state.deck)

if "drawn_cards" not in st.session_state:
    st.session_state.drawn_cards = []

if "total_wins" not in st.session_state:
    st.session_state.total_wins = 0

if "total_draws" not in st.session_state:
    st.session_state.total_draws = 0

# --- SIDEBAR GAME MODE & DISPLAY SETTINGS ---
st.sidebar.header("⚙️ Game Settings")

game_mode = st.sidebar.radio(
    "Choose Game Mode:",
    ["Red Head", "Lucky Jack"],
    index=0,
    help="Select the game mode to change the winning condition."
)

st.sidebar.divider()
st.sidebar.header("📊 Scoreboard Settings")

# TOGGLE TO SHOW/HIDE PERCENTAGE
show_win_rate = st.sidebar.toggle(
    "Show Win Rate Percentage",
    value=True,
    help="Toggle off to hide the calculated win rate percentage metric."
)

st.title(f"🃏 {game_mode} Simulator")

# Game Info Header
if game_mode == "Red Head":
    st.info("🎯 **Objective:** Draw a **Red Head** (Red Jack, Queen, or King of Hearts ♥ or Diamonds ♦) to win! *(6 winning cards in deck)*")
elif game_mode == "Lucky Jack":
    st.info("🎯 **Objective:** Draw a **Lucky Jack** (Black Jack of Spades ♠ or Clubs ♣) to win! *(2 winning cards in deck)*")

# Reset score if game mode changes
if "current_mode" not in st.session_state or st.session_state.current_mode != game_mode:
    st.session_state.current_mode = game_mode
    st.session_state.deck = create_deck()
    random.shuffle(st.session_state.deck)
    st.session_state.drawn_cards = []
    st.session_state.total_wins = 0
    st.session_state.total_draws = 0

# --- CONTROLS SECTION ---
st.subheader("Controls")

replace_immediately = st.toggle(
    "Replace card back into deck immediately",
    value=False,
    help="When enabled, cards are placed back into the deck right after being drawn."
)

col1, col2, col3 = st.columns([1, 1, 1])


def draw_cards(count=1):
    cards = []
    for _ in range(count):
        if replace_immediately:
            if st.session_state.deck:
                card = random.choice(st.session_state.deck)
                cards.append(card)
        else:
            if st.session_state.deck:
                card = st.session_state.deck.pop()
                cards.append(card)
            else:
                st.warning("The deck is empty! Click Reshuffle to continue.")
                break

    for card in cards:
        st.session_state.total_draws += 1
        if check_win(card, game_mode):
            st.session_state.total_wins += 1

    st.session_state.drawn_cards.extend(cards)


with col1:
    if st.button("🂠 Draw 1 Card", use_container_width=True):
        draw_cards(1)

with col2:
    if st.button("🂠 Draw 5 Cards", use_container_width=True):
        draw_cards(5)

with col3:
    if st.button("🔄 Reshuffle Deck", use_container_width=True):
        st.session_state.deck = create_deck()
        random.shuffle(st.session_state.deck)
        st.session_state.drawn_cards = []
        st.session_state.total_wins = 0
        st.session_state.total_draws = 0
        st.rerun()

# --- SCOREBOARD METRICS ---
# Dynamically adjust column layout based on toggle state
if show_win_rate:
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Draws", st.session_state.total_draws)
    m2.metric(f"{game_mode} Wins 🏆", st.session_state.total_wins)
    
    if st.session_state.total_draws > 0:
        win_rate = (st.session_state.total_wins / st.session_state.total_draws) * 100
        m3.metric("Win Rate", f"{win_rate:.1f}%")
    else:
        m3.metric("Win Rate", "0.0%")
else:
    m1, m2 = st.columns(2)
    m1.metric("Total Draws", st.session_state.total_draws)
    m2.metric(f"{game_mode} Wins 🏆", st.session_state.total_wins)

# Deck Status Caption
if replace_immediately:
    st.caption("Mode: **With Replacement** | Remaining in deck: **52 (Infinite)**")
else:
    st.caption(f"Mode: **Without Replacement** | Remaining in deck: **{len(st.session_state.deck)}**")

st.divider()

# --- CENTERED DISPLAY FOR LAST DRAW ---
if st.session_state.drawn_cards:
    last_draw = st.session_state.drawn_cards[-1]
    won = check_win(last_draw, game_mode)

    if won:
        st.balloons()
        st.success(f"🎉 **YOU WIN!** You drew the **{last_draw['rank']} of {SUIT_NAMES[last_draw['suit']]}**!")
    else:
        st.write(f"Drawn: **{last_draw['rank']} of {SUIT_NAMES[last_draw['suit']]}** (Not a win)")

    # Centering the drawn card image using empty side columns
    c_left, c_center, c_right = st.columns([1, 1, 1])

    image_path = os.path.join("assets", "cards", last_draw["image"])
    rank_c = "0" if last_draw["rank"] == "10" else last_draw["rank"]
    cdn_url = f"https://deckofcardsapi.com/static/img/{rank_c}{last_draw['suit']}.png"

    with c_center:
        if os.path.exists(image_path):
            st.image(image_path, use_container_width=True)
        else:
            st.image(cdn_url, use_container_width=True)

    # --- DRAW HISTORY GALLERY ---
    if len(st.session_state.drawn_cards) > 1:
        st.subheader("Draw History")
        cols = st.columns(6)
        for i, card in enumerate(reversed(st.session_state.drawn_cards)):
            card_path = os.path.join("assets", "cards", card["image"])
            rank_code = "0" if card["rank"] == "10" else card["rank"]
            card_cdn = f"https://deckofcardsapi.com/static/img/{rank_code}{card['suit']}.png"

            with cols[i % 6]:
                if os.path.exists(card_path):
                    st.image(card_path, use_container_width=True)
                else:
                    st.image(card_cdn, use_container_width=True)

                if check_win(card, game_mode):
                    st.caption("🏆 WIN")
