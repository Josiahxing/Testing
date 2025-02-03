import streamlit as st
import random
import time

# Sample sentences for the typing race
sentences = [
    "The quick brown fox jumps over the lazy dog.",
    "Streamlit makes it easy to build web apps in Python.",
    "Typing speed is measured in words per minute.",
    "Practice makes perfect when it comes to typing.",
    "Python is a versatile programming language."
]

# Select a random sentence
sentence = random.choice(sentences)

st.title("Typing Racing Game")
st.write("Type the following sentence as quickly as you can:")

st.write(f"**{sentence}**")

# Input field for user to type the sentence
user_input = st.text_input("Start typing here:")

# Start the timer when the user starts typing
if user_input:
    start_time = time.time()

# Check if the user has finished typing the sentence
if user_input == sentence:
    end_time = time.time()
    time_taken = end_time - start_time
    words_per_minute = len(sentence.split()) / (time_taken / 60)
    st.success(f"Congratulations! You finished in {time_taken:.2f} seconds.")
    st.write(f"Your typing speed is {words_per_minute:.2f} words per minute.")

# Display instructions
st.write("Start typing the sentence above to begin the race!")

# Reset button
if st.button("Reset"):
    st.experimental_rerun()
