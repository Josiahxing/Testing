import streamlit as st
import fitz  # PyMuPDF
import io

st.title("PDF Combiner App")

uploaded_files = st.file_uploader("Upload PDF files to combine", type="pdf", accept_multiple_files=True)

if st.button("Combine PDFs") and uploaded_files:
    combined_pdf = fitz.open()

    for uploaded_file in uploaded_files:
        pdf_bytes = uploaded_file.read()
        pdf_doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        for page in pdf_doc:
            combined_pdf.insert_pdf(pdf_doc, from_page=page.number, to_page=page.number)

    output = io.BytesIO()
    combined_pdf.save(output)
    combined_pdf.close()
    output.seek(0)

    st.download_button(
        label="Download Combined PDF",
        data=output,
        file_name="combined.pdf",
        mime="application/pdf"
    )
