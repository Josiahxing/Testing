import streamlit as st
import fitz  # PyMuPDF
import pytesseract
import pandas as pd
from io import BytesIO

# Function to extract text from images in a PDF
def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text_data = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img = pix.tobytes("png")
        text = pytesseract.image_to_string(img)
        text_data.append({"Page": page_num + 1, "Text": text})

    return text_data

# Streamlit app
st.title("PDF Scanner")
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    text_data = extract_text_from_pdf(uploaded_file)
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
