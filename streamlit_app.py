import streamlit as st
import fitz  # PyMuPDF
import tempfile
import os

st.title("🖨️ PDF Print Manager")

st.markdown("""
Upload multiple PDF files and specify how many copies of each you'd like to print. 
Click 'Print All' to simulate printing.
""")

uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)

copies = {}
if uploaded_files:
    st.subheader("Uploaded Files and Copy Settings")
    for file in uploaded_files:
        file_name = file.name
        copies[file_name] = st.number_input(f"Copies for {file_name}", min_value=1, max_value=100, value=1)

if st.button("Print All"):
    if not uploaded_files:
        st.warning("Please upload at least one PDF file.")
    else:
        for file in uploaded_files:
            file_name = file.name
            num_copies = copies[file_name]
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(file.read())
                    tmp_path = tmp.name

                doc = fitz.open(tmp_path)
                st.success(f"🖨️ Printing {num_copies} copies of '{file_name}' ({doc.page_count} pages)")
                doc.close()
                os.remove(tmp_path)
            except Exception as e:
                st.error(f"❌ Failed to print '{file_name}': {e}")
