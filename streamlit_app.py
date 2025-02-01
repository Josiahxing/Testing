import re
import streamlit as st
import fitz  # PyMuPDF
import pytesseract
import pandas as pd
from PIL import Image, ImageEnhance, ImageFilter
from io import BytesIO
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE

# Set the Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

# Function to clean text data
def clean_text(text):
    return ILLEGAL_CHARACTERS_RE.sub(r'', text)

# Function to pre-process images
def preprocess_image(img):
    img = img.convert('L')  # Convert to grayscale
    img = img.filter(ImageFilter.MedianFilter())  # Apply median filter
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2)  # Enhance contrast
    return img

# Function to extract text from images in a PDF
def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text_data = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.open(BytesIO(pix.tobytes("png")))
        img = preprocess_image(img)
        text = pytesseract.image_to_string(img, config='--psm 6 -l eng')  # Use page segmentation mode 6 and English language
        cleaned_text = clean_text(text)
        paragraphs = cleaned_text.split('\n\n')  # Split text into paragraphs
        for paragraph in paragraphs:
            if paragraph.strip():  # Skip empty paragraphs
                text_data.append({"Page": page_num + 1, "Paragraph": paragraph.strip()})

    return text_data

# Function to extract text from an image file
def extract_text_from_image(image_file):
    img = Image.open(image_file)
    img = preprocess_image(img)
    text = pytesseract.image_to_string(img, config='--psm 6 -l eng')  # Use page segmentation mode 6 and English language
    cleaned_text = clean_text(text)
    paragraphs = cleaned_text.split('\n\n')  # Split text into paragraphs
    text_data = [{"Paragraph": paragraph.strip()} for paragraph in paragraphs if paragraph.strip()]
    return text_data

# Streamlit app
st.title("PDF and Image Scanner")
uploaded_file = st.file_uploader("Upload a PDF or Image file", type=["pdf", "jpg", "jpeg", "png"])

if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        text_data = extract_text_from_pdf(uploaded_file)
    else:
        text_data = extract_text_from_image(uploaded_file)
    
    df = pd.DataFrame(text_data)
    
    st.write("Extracted Text:")
    st.dataframe(df)

    # Export to Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Extracted Text')
    output.seek(0)

    st.download_button(
        label="Download Excel file",
        data=output,
        file_name="extracted_text.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
