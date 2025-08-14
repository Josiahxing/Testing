import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

st.title("Selenium + Streamlit Example")

if st.button("Run Selenium Task"):
    options = Options()
    options.add_argument("--headless")  # Optional: run without opening browser window
    driver = webdriver.Chrome(options=options)

    driver.get("https://example.com")
    st.write("Page title:", driver.title)

    driver.quit()
