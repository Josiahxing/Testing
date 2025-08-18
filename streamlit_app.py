import streamlit as st
import fitz  # PyMuPDF
import io

# Title of the app
st.title("📄 PDF Combiner and Copier App")

# Upload multiple PDF files
uploaded_files = st.file_uploader(
    "Upload PDF files to combine", 
    type="pdf", 
    accept_multiple_files=True
)

# Input for number of copies
num_copies = st.number_input(
    "# of Copies", 
    min_value=1, 
    max_value=4, 
    value=1, 
    step=1,
    help="Each page will be duplicated this many times in the final PDF."
)

# Combine button
if st.button("Combine PDFs") and uploaded_files:
    combined_pdf = fitz.open()

    for uploaded_file in uploaded_files:
        pdf_bytes = uploaded_file.read()
        pdf_doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        for page in pdf_doc:
            for _ in range(num_copies):
                combined_pdf.insert_pdf(pdf_doc, from_page=page.number, to_page=page.number)

    output = io.BytesIO()
    combined_pdf.save(output)
    combined_pdf.close()
    output.seek(0)

    st.success("✅ PDF combined successfully!")
    st.download_button(
        label="📥 Download Combined PDF",
        data=output,
        file_name="combined.pdf",
        mime="application/pdf"
    )
