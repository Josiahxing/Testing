import streamlit as st
import fitz  # PyMuPDF
import io

st.title("PDF Combiner + JS Script Generator")

# --- PDF Combiner Section ---
st.header("📎 Combine PDFs with Copies")

uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)
num_copies = st.number_input("# of Copies", min_value=1, max_value=4, value=1, step=1)

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

    st.download_button(
        label="Download Combined PDF",
        data=output,
        file_name="combined.pdf",
        mime="application/pdf"
    )

# --- JavaScript Generator Section ---
st.header("📜 Generate JavaScript for Order Downloads")

order_input = st.text_area("Enter Order Numbers (comma or newline separated):")

if st.button("Generate Script") and order_input:
    orders = [o.strip() for o in order_input.replace('\n', ',').split(',') if o.strip()]
    script_lines = ['<script>']
    for order in orders:
        script_lines.append(f'window.open("https://yourserver.com/downloads/order_{order}.pdf", "_blank");')
    script_lines.append('</script>')
    script = '\n'.join(script_lines)

    st.code(script, language='html')
    st.text_input("Copy the script below:", value=script)
