import streamlit as st
import fitz  # PyMuPDF
import io
import urllib.parse

st.title("📎 PDF Combiner + 📝 JS Bookmarklet Generator")

# --- PDF Combiner Section ---
st.header("Combine PDFs with Copies")

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

# --- JavaScript Bookmarklet Generator Section ---
st.header("Generate JavaScript Bookmarklet for Order Automation")

order_input = st.text_area("Enter Order Numbers (comma or newline separated):")

if st.button("Generate Bookmarklet") and order_input:
    orders = [f'"{o.strip()}"' for o in order_input.replace('\n', ',').split(',') if o.strip()]
    order_str = ','.join(orders)

    # JavaScript template
    js_code = f'''javascript:(async()=>{{const orders=[{order_str}],waitForElement=(x,t=15000)=>new Promise((r,j)=>{{const s=Date.now(),i=setInterval(()=>{{const e=document.evaluate(x,document,null,XPathResult.FIRST_ORDERED_NODE_TYPE,null).singleNodeValue;if(e&&e.offsetParent!==null){{clearInterval(i);r(e)}}else if(Date.now()-s>t){{clearInterval(i);j(`⏳ Timeout waiting for element: ${{x}}`)}}}},500)}}),delay=m=>new Promise(r=>setTimeout(r,m)),safeClick=async(x,n=5)=>{{for(let i=0;i<n;i++){{try{{const e=await waitForElement(x,10000);e.click();return}}catch{{console.warn(`⚠️ Retry ${{i+1}} for ${{x}}`);await delay(2000)}}}}throw new Error(`❌ Failed to click after ${{n}} retries: ${{x}}`)}},processOrder=async o=>{{console.log(`🔄 Processing order: ${{o}}`);const i=await waitForElement('//*[@id="ReportViewerMain_ctl08_ctl03_txtValue"]');i.value='';i.dispatchEvent(new Event('change'));await delay(500);i.value=o;i.dispatchEvent(new Event('change'));await safeClick('//*[@id="ReportViewerMain_ctl08_ctl00"]');await waitForElement('//*[@id="ReportViewerMain_ctl09"]',20000);await delay(3000);await safeClick('/html/body/form/div[3]/div/div/table/tbody/tr[3]/td/div[1]/div/div[5]/table/tbody/tr/td/div[1]/table/tbody/tr/td');await safeClick('/html/body/form/div[3]/div/div/table/tbody/tr[3]/td/div[1]/div/div[5]/table/tbody/tr/td/div[2]/div[4]/a');console.log(`✅ Finished order: ${{o}}`);await delay(4000)}},runAllOrders=async()=>{{for(const o of orders)try{{await processOrder(o)}}catch(e){{console.error(`❌ Error processing ${{o}}:`,e)}}console.log("🎉 All orders processed.")}};runAllOrders();}})();'''

    # URL encode the entire script
    encoded_script = urllib.parse.quote(js_code, safe='')

    bookmarklet = f'javascript:{encoded_script}'

    st.subheader("Generated JavaScript Bookmarklet")
    st.code(bookmarklet, language='javascript')
    st.text_input("Copy the bookmarklet below:", value=bookmarklet)

