import os
import random
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Card Drawing Simulator", page_icon="🃏", layout="centered")

st.title("🃏 Card Drawing Simulator")

# Mappings for ranks and suits to filenames
SUITS = ["S", "H", "D", "C"]  # Spades, Hearts, Diamonds, Clubs
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
SUIT_NAMES = {"S": "Spades", "H": "Hearts", "D": "Diamonds", "C": "Clubs"}


def create_deck():
    """Generates a standard 52-card deck."""
    return [{"rank": r, "suit": s, "image": f"{r}{s}.png"} for s in SUITS for r in RANKS]


# Initialize session state
if "deck" not in st.session_state:
    st.session_state.deck = create_deck()
    random.shuffle(st.session_state.deck)

if "drawn_cards" not in st.session_state:
    st.session_state.drawn_cards = []

# Sidebar controls
st.sidebar.header("Controls")
if st.sidebar.button("🔄 Reshuffle Deck", use_container_width=True):
    st.session_state.deck = create_deck()
    random.shuffle(st.session_state.deck)
    st.session_state.drawn_cards = []
    st.rerun()

# Draw action
def draw_cards(count=1):
    cards = []
    for _ in range(count):
        if st.session_state.deck:
            cards.append(st.session_state.deck.pop())
    st.session_state.drawn_cards.extend(cards)


col1, col2 = st.columns(2)
with col1:
    if st.button("🂠 Draw 1 Card", use_container_width=True):
        draw_cards(1)
with col2:
    if st.button("🂠 Draw 5 Cards", use_container_width=True):
        draw_cards(5)

st.caption(f"Cards remaining: **{len(st.session_state.deck)}**")

# Display Last Drawn Card / Hand
if st.session_state.drawn_cards:
    st.subheader("Most Recent Draw")

    last_draw = st.session_state.drawn_cards[-1]
    image_path = os.path.join("assets", "cards", last_draw["image"])

    if os.path.exists(image_path):
        st.image(image_path, width=160, caption=f"{last_draw['rank']} of {SUIT_NAMES[last_draw['suit']]}")
    else:
        # Fallback if image file is missing
        st.warning(f"Image not found at `{image_path}`. Showing text instead:")
        st.info(f"**{last_draw['rank']} of {SUIT_NAMES[last_draw['suit']]}**")

    # Display full history in a multi-column gallery
    if len(st.session_state.drawn_cards) > 1:
        st.subheader("All Drawn Cards")
        cols = st.columns(5)
        for i, card in enumerate(reversed(st.session_state.drawn_cards)):
            card_img = os.path.join("assets", "cards", card["image"])
            with cols[i % 5]:
                if os.path.exists(card_img):
                    st.image(card_img, use_container_width=True)
                else:
                    st.write(f"{card['rank']}{card['suit']}")
