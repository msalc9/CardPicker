
import random
import pandas as pd
import streamlit as st

# Page configuration
st.set_page_config(page_title="Card Drawing Simulator", page_icon="🃏", layout="centered")

st.title("🃏 Card Drawing Simulator")
st.caption("A simple interactive simulation built with Python and Streamlit.")

# Define standard 52-card deck
SUITS = ["♠", "♥", "♦", "♣"]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]


def create_deck():
    """Generates a fresh standard 52-card deck."""
    return [{"rank": r, "suit": s} for s in SUITS for r in RANKS]


# Initialize session state variables
if "deck" not in st.session_state:
    st.session_state.deck = create_deck()
    random.shuffle(st.session_state.deck)

if "drawn_cards" not in st.session_state:
    st.session_state.drawn_cards = []

# Sidebar Controls
st.sidebar.header("Controls & Options")

with_replacement = st.sidebar.checkbox(
    "Replace drawn cards back into deck",
    value=False,
    help="If checked, drawn cards are returned to the deck before the next draw.",
)

if st.sidebar.button("🔄 Reshuffle / Reset Deck", use_container_width=True):
    st.session_state.deck = create_deck()
    random.shuffle(st.session_state.deck)
    st.session_state.drawn_cards = []
    st.rerun()

# Card Draw Actions
col1, col2 = st.columns(2)


def draw_card(num_cards=1):
    cards_drawn = []
    for _ in range(num_cards):
        if with_replacement:
            cards_drawn.append(random.choice(create_deck()))
        else:
            if len(st.session_state.deck) > 0:
                cards_drawn.append(st.session_state.deck.pop())
            else:
                st.warning("The deck is empty! Reshuffle to continue.")
                break
    st.session_state.drawn_cards.extend(cards_drawn)


with col1:
    if st.button("🂠 Draw 1 Card", use_container_width=True):
        draw_card(1)

with col2:
    if st.button("🂠 Draw 5 Cards", use_container_width=True):
        draw_card(5)

# Metrics Display
remaining = len(st.session_state.deck) if not with_replacement else "∞"
st.metric(label="Cards Remaining in Deck", value=f"{remaining}")

# Display Last Drawn Card
if st.session_state.drawn_cards:
    last_card = st.session_state.drawn_cards[-1]
    color = "red" if last_card["suit"] in ["♥", "♦"] else "black"

    st.markdown(
        f"""
        <div style="text-align: center; border: 2px solid #ddd; border-radius: 12px; padding: 20px; margin: 20px 0;">
            <p style="font-size: 1rem; color: #666; margin: 0;">Most Recent Draw</p>
            <h1 style="font-size: 4rem; color: {color}; margin: 0;">{last_card['rank']}{last_card['suit']}</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Historical Draws & Analytics
if st.session_state.drawn_cards:
    st.subheader("Draw Statistics & History")

    df = pd.DataFrame(st.session_state.drawn_cards)
    df["display"] = df["rank"] + df["suit"]

    tab1, tab2 = st.tabs(["Suit Distribution", "Draw History"])

    with tab1:
        suit_counts = df["suit"].value_counts().reindex(SUITS, fill_value=0)
        st.bar_chart(suit_counts)

    with tab2:
        st.dataframe(
            df[["rank", "suit", "display"]].rename(columns={"display": "Card"}),
            use_container_width=True,
        )
