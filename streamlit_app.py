import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

st.title("Streamlit + Selenium Demo")

url = st.text_input("Enter a URL to visit")

if st.button("Get Page Title"):
    # Set up headless Chrome
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Path to your ChromeDriver (adjust if needed)
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        title = driver.title
        st.success(f"Page Title: {title}")
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        driver.quit()
