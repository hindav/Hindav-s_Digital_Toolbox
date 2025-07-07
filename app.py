import streamlit as st
import base64
import cv2
import numpy as np
from PIL import Image
import easyocr
import PyPDF2
import pytesseract
import io
import os

# Background image functions
def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def add_bg_sidebar_from_local(image_file):
    with open(image_file, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        [data-testid="stSidebar"] {{
            background-image: url("data:image/jpg;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Background setup
add_bg_from_local('BG.jpg')
add_bg_sidebar_from_local('BG.jpg')

# Main title and sidebar
st.title("Hindav's Digital Toolbox")
app_mode = st.sidebar.selectbox("Select a tool", ["OCR Tool", "Image to PDF", "Image & PDF Resizer"])

# OCR Tool (unchanged)
if app_mode == "OCR Tool":
    st.header("EasyOCR-Based OCR Tool")
    languages = ["English", "Hindi", "Marathi", "Other"]
    selected_language = st.selectbox("Select the language of the text", languages)

    uploaded_file = st.file_uploader("Select an image file for OCR", type=["jpg", "png", "pdf", "jpeg", "webp"])

    if uploaded_file is not None:
        with st.spinner("Processing image..."):
            try:
                st.info("Sabar Karo... Chai Pio Biscut Khao..")
                file_bytes = uploaded_file.read()
                image = Image.open(io.BytesIO(file_bytes)).convert('RGB')
                image_np = np.array(image)

                st.image(image_np, caption="Uploaded Image Preview")

                if selected_language == "English":
                    reader = easyocr.Reader(['en'])
                elif selected_language == "Hindi":
                    reader = easyocr.Reader(['hi'])
                elif selected_language == "Marathi":
                    reader = easyocr.Reader(['mr'])
                else:
                    reader = easyocr.Reader(['en'])

                text = reader.readtext(image_np)

                if not text:
                    st.warning("No text detected. Try a clearer image.")
                else:
                    extracted_text = '\n'.join([item[1] for item in text])
                    st.subheader("Recognized Text:")
                    st.write(extracted_text)

                    from reportlab.pdfgen import canvas
                    from reportlab.lib.pagesizes import letter

                    c = canvas.Canvas("output.pdf", pagesize=letter)
                    textobject = c.beginText(50, 750)
                    for line in extracted_text.splitlines():
                        textobject.textLine(line)
                    c.drawText(textobject)
                    c.showPage()
                    c.save()

                    file_name = uploaded_file.name.split('.')[0] + " OCR by Hindav.pdf"
                    with open("output.pdf", "rb") as f:
                        st.download_button("Download as PDF", f, file_name=file_name)

                    os.remove("output.pdf")
            except Exception as e:
                st.error("Couldn't process the image. Please try again.")
                st.error(str(e))

# ✅ Image to PDF Tool - Simplified with Toggle
elif app_mode == "Image to PDF":
    st.header("Image to PDF Converter")

    toggle = st.checkbox("OCR (Experimental)", value=False)

    uploaded_file = st.file_uploader("Select an image file", type=["jpg", "png", "jpeg", "webp"], key="image_to_pdf")

    if uploaded_file is not None:
        with st.spinner("Processing..."):
            try:
                file_bytes = uploaded_file.read()
                image = Image.open(io.BytesIO(file_bytes)).convert('RGB')

                if toggle:
                    st.info("Sabar Karo... Chai Pio Biscut Khao..")
                    pdf_bytes = pytesseract.image_to_pdf_or_hocr(image, extension='pdf')
                    file_name = uploaded_file.name.split('.')[0] + " OCR Formatted PDF by Hindav.pdf"
                    st.download_button("Download OCR Formatted PDF", data=pdf_bytes, file_name=file_name)
                else:
                    st.info("Sabar Karo... Chai Pio Biscut Khao..")
                    pdf_bytes = io.BytesIO()
                    image.save(pdf_bytes, format="PDF")
                    pdf_bytes.seek(0)
                    file_name = uploaded_file.name.split('.')[0] + " PDF by Hindav.pdf"
                    st.download_button("Download as PDF", pdf_bytes, file_name=file_name)

            except Exception as e:
                st.error("Couldn't process the image. Please try again.")
                st.error(str(e))

# Image & PDF Resizer (unchanged)
elif app_mode == "Image & PDF Resizer":
    st.header("Image & PDF Resizer")
    tab1, tab2 = st.tabs(["Image Resizer", "PDF Resizer"])

    with tab1:
        uploaded_image = st.file_uploader("Select an image file", type=["jpg", "png", "jpeg", "webp"], key="image_uploader")

        if uploaded_image is not None:
            st.info("Sabar Karo... Chai Pio Biscut Khao..")
            st.subheader("Original Image")
            st.image(uploaded_image)
            image = Image.open(uploaded_image)
            original_size = len(uploaded_image.getvalue()) / 1024
            st.write(f"Original Image Size: {original_size:.2f} KB")

            storage_size_kb = st.text_input("Enter Storage Size (KB)", value=f"{original_size:.2f}")

            with st.form("image_resizer_form"):
                submit_button = st.form_submit_button("Resize Image")

            if submit_button:
                try:
                    storage_size_kb = float(storage_size_kb)
                    if storage_size_kb >= original_size:
                        st.error("Target size must be smaller than original size.")
                    else:
                        scale_factor = storage_size_kb / original_size
                        new_width = int(image.width * scale_factor)
                        new_height = int(image.height * scale_factor)
                        resized_img = image.resize((new_width, new_height))

                        st.subheader("Resized Image")
                        st.image(resized_img)

                        file_name = os.path.splitext(uploaded_image.name)[0] + " + Image Resize by Hindav." + uploaded_image.name.split('.')[-1]
                        resized_img.save(file_name)

                        with open(file_name, "rb") as file:
                            st.download_button("Download Resized Image", file, file_name=file_name)

                        os.remove(file_name)
                except Exception:
                    st.error("Invalid input. Please enter a valid storage size.")

    with tab2:
        uploaded_pdf = st.file_uploader("Select a PDF file", type=["pdf"], key="pdf_uploader")

        if uploaded_pdf is not None:
            st.info("Sabar Karo... Chai Pio Biscut Khao..")
            pdf = PyPDF2.PdfReader(uploaded_pdf)
            st.subheader("Original PDF")
            st.write(f"Page Count: {len(pdf.pages)}")

            compression_level = st.selectbox("Select Compression Level", ["Low", "Medium", "High"])

            with st.form("pdf_compressor_form"):
                submit_button = st.form_submit_button("Compress PDF")

            if submit_button:
                compressed_pdf = PyPDF2.PdfWriter()

                for page in pdf.pages:
                    compressed_pdf.add_page(page)

                with io.BytesIO() as buffer:
                    compressed_pdf.write(buffer)
                    compressed_pdf_data = buffer.getvalue()

                file_name = os.path.splitext(uploaded_pdf.name)[0] + " + PDF Resize by Hindav.pdf"
                st.download_button("Download Compressed PDF", compressed_pdf_data, file_name=file_name)

# Footer
st.markdown("<p style='text-align: center; margin-top: 20px;'>Developed by <a href='https://github.com/hindav' target='_blank'>Hindav</a></p>", unsafe_allow_html=True)
