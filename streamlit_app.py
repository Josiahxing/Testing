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

# Initialize session state variables
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'highscore' not in st.session_state:
    st.session_state.highscore = 0

st.title("Typing Racing Game")
st.write("Type the following sentence as quickly as you can:")

st.write(f"**{sentence}**")

# Input field for user to type the sentence
user_input = st.text_input("Start typing here:")

# Start the timer when the user starts typing
if user_input and st.session_state.start_time is None:
    st.session_state.start_time = time.time()

# Calculate errors
errors = sum(1 for a, b in zip(user_input, sentence) if a != b) + abs(len(user_input) - len(sentence))

# Highlight the current text position
highlighted_sentence = ""
for i, char in enumerate(sentence):
    if i < len(user_input):
        if user_input[i] == char:
            highlighted_sentence += f"<span style='color: green;'>{char}</span>"
        else:
            highlighted_sentence += f"<span style='color: red;'>{char}</span>"
    else:
        highlighted_sentence += char
st.markdown(f"**{highlighted_sentence}**", unsafe_allow_html=True)

# Check if the user has finished typing the sentence
if user_input == sentence:
    end_time = time.time()
    time_taken = end_time - st.session_state.start_time
    words_per_minute = len(sentence.split()) / (time_taken / 60)
    st.success(f"Congratulations! You finished in {time_taken:.2f} seconds.")
    st.write(f"Your typing speed is {words_per_minute:.2f} words per minute.")
    st.write(f"Number of errors: {errors}")

    # Update highscore
    if words_per_minute > st.session_state.highscore:
        st.session_state.highscore = words_per_minute
        st.balloons()
        st.write("New highscore!")

    st.write(f"Highscore: {st.session_state.highscore:.2f} WPM")

# Display instructions
st.write("Start typing the sentence above to begin the race!")

# Reset button
if st.button("Reset"):
    st.session_state.start_time = None
    st.experimental_rerun()
