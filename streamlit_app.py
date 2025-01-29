import streamlit as st
import random

st.title("Number Guessing Game")

if 'number' not in st.session_state:
    st.session_state.number = random.randint(1, 100)

guess = st.number_input("Enter your guess:", min_value=1, max_value=100, step=1)

if st.button("Submit"):
    if guess < st.session_state.number:
        st.write("Too low!")
    elif guess > st.session_state.number:
        st.write("Too high!")
    else:
        st.write("Congratulations! You guessed the number.")
        st.session_state.number = random.randint(1, 100)  # Reset the game
