import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# App state
if "score" not in st.session_state:
    st.session_state.score = 0
if "rounds" not in st.session_state:
    st.session_state.rounds = 0
if "x" not in st.session_state:
    st.session_state.x = None
    st.session_state.y = None
    st.session_state.r_actual = None

# Generate new scatterplot
def generate_data():
    r = np.round(np.random.uniform(-1, 1), 2)
    x = np.random.normal(0, 1, 100)
    noise = np.random.normal(0, 1, 100)
    y = r * x + np.sqrt(1 - r**2) * noise
    return x, y, r

# Plot
def plot_data(x, y):
    fig, ax = plt.subplots()
    ax.scatter(x, y)
    ax.set_title("Guess the Correlation")
    st.pyplot(fig)

# Header
st.title("📈 Correlation Guessing Game")
st.markdown("Guess the correlation coefficient (r) for the scatterplot below. Enter a value between **-1** and **1**.")

# Start or continue game
if st.session_state.x is None:
    x, y, r_actual = generate_data()
    st.session_state.x = x
    st.session_state.y = y
    st.session_state.r_actual = r_actual
else:
    x = st.session_state.x
    y = st.session_state.y
    r_actual = st.session_state.r_actual

# Show plot
plot_data(x, y)

# Input
guess = st.number_input("Your guess:", min_value=-1.0, max_value=1.0, step=0.01, format="%.2f")

# Submit
if st.button("Submit Guess"):
    r_true = round(r_actual, 2)
    r_guess = round(guess, 2)
    error = abs(r_guess - r_true)
    st.session_state.rounds += 1

    if error <= 0.1:
        st.success(f"✅ Correct! Actual r = {r_true}. You were very close!")
        st.session_state.score += 1
    else:
        st.error(f"❌ Oops! Actual r = {r_true}. Your guess was {r_guess}.")

    st.markdown(f"**Current Score:** {st.session_state.score} / {st.session_state.rounds}")

    # Reset for next round
    x, y, r_actual = generate_data()
    st.session_state.x = x
    st.session_state.y = y
    st.session_state.r_actual = r_actual

# Reset button
if st.button("Reset Game"):
    st.session_state.score = 0
    st.session_state.rounds = 0
    st.session_state.x = None
    st.session_state.y = None
    st.session_state.r_actual = None
