import streamlit as st
import fitz  # PyMuPDF
import tempfile
import os

st.title("📄 PDF Batch Printer")

uploaded_files = st.file_uploader("Upload PDF files to print", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    st.success(f"{len(uploaded_files)} PDF file(s) uploaded.")

    for uploaded_file in uploaded_files:
        st.write(f"🖨️ Printing: {uploaded_file.name}")

        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_file_path = tmp_file.name

        # Open the PDF using PyMuPDF to ensure it's valid
        try:
            doc = fitz.open(tmp_file_path)
            doc.close()

            # Send the file to the system's default printer
            os.startfile(tmp_file_path, "print")
        except Exception as e:
            st.error(f"❌ Failed to print {uploaded_file.name}: {e}")
