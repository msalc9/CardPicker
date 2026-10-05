import os
import random
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Card Drawing Simulator", page_icon="🃏", layout="centered")

st.title("🃏 Card Drawing Simulator")

# Mappings for ranks and suits
SUITS = ["S", "H", "D", "C"]  # Spades, Hearts, Diamonds, Clubs
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
SUIT_NAMES = {"S": "Spades", "H": "Hearts", "D": "Diamonds", "C": "Clubs"}


def create_deck():
    """Generates a fresh standard 52-card deck."""
    return [{"rank": r, "suit": s, "image": f"{r}{s}.png"} for s in SUITS for r in RANKS]


# Initialize session state
if "deck" not in st.session_state:
    st.session_state.deck = create_deck()
    random.shuffle(st.session_state.deck)

if "drawn_cards" not in st.session_state:
    st.session_state.drawn_cards = []

# --- CONTROLS SECTION ---
st.subheader("Controls")

# Toggle for drawing with or without replacement
replace_immediately = st.toggle(
    "Replace card back into deck immediately",
    value=False,
    help="When enabled, cards are placed back into the deck right after being drawn, allowing duplicate draws."
)

col1, col2, col3 = st.columns([1, 1, 1])


def draw_cards(count=1):
    cards = []
    for _ in range(count):
        if replace_immediately:
            # Draw randomly without removing from deck
            cards.append(random.choice(st.session_state.deck))
        else:
            # Pop card from remaining deck
            if st.session_state.deck:
                cards.append(st.session_state.deck.pop())
            else:
                st.warning("The deck is empty! Click Reshuffle to continue.")
                break
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
        st.rerun()

# Deck Status Metric
if replace_immediately:
    st.caption("Mode: **With Replacement** | Deck count: **52 (Infinite Draws)**")
else:
    st.caption(f"Mode: **Without Replacement** | Cards remaining in deck: **{len(st.session_state.deck)}**")

st.divider()

# --- DISPLAY SECTION ---
if st.session_state.drawn_cards:
    st.subheader("Most Recent Draw")

    last_draw = st.session_state.drawn_cards[-1]
    
    # Option A: Local GitHub repo assets
    image_path = os.path.join("assets", "cards", last_draw["image"])
    
    # Option B: Fallback CDN URL if local image is missing
    rank_cdn = "0" if last_draw["rank"] == "10" else last_draw["rank"]
    cdn_url = f"https://deckofcardsapi.com/static/img/{rank_cdn}{last_draw['suit']}.png"

    # Display image (tries local file first, falls back to public CDN)
    if os.path.exists(image_path):
        st.image(image_path, width=160, caption=f"{last_draw['rank']} of {SUIT_NAMES[last_draw['suit']]}")
    else:
        st.image(cdn_url, width=160, caption=f"{last_draw['rank']} of {SUIT_NAMES[last_draw['suit']]}")

    # Gallery of All Drawn Cards
    if len(st.session_state.drawn_cards) > 1:
        st.subheader("Draw History")
        cols = st.columns(6)
        for i, card in enumerate(reversed(st.session_state.drawn_cards)):
            card_path = os.path.join("assets", "cards", card["image"])
            rank_c = "0" if card["rank"] == "10" else card["rank"]
            card_cdn = f"https://deckofcardsapi.com/static/img/{rank_c}{card['suit']}.png"
            
            with cols[i % 6]:
                if os.path.exists(card_path):
                    st.image(card_path, use_container_width=True)
                else:
                    st.image(card_cdn, use_container_width=True)
