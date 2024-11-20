import streamlit as st
import base64
import cv2
import numpy as np
from PIL import Image
import easyocr
import PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import os

# Function to add background image to the app
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

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

# Function to add background with blur effect to the sidebar
def add_bg_sidebar_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

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

# Adding background images
add_bg_from_local('BG.jpg')
add_bg_sidebar_from_local('BG.jpg')

# Main application title
st.title("Hindav's Digital Toolbox")

# Sidebar menu for app selection
app_mode = st.sidebar.selectbox("Select a tool", ["OCR Tool", "Image to PDF", "Image & PDF Resizer"])

# OCR Tool
if app_mode == "OCR Tool":
    st.header("EasyOCR-Based OCR Tool")

    # Language selection option
    languages = ["English", "Hindi", "Marathi", "Other"]
    selected_language = st.selectbox("Select the language of the text", languages)

    # Upload an image file for OCR
    uploaded_file = st.file_uploader("Select an image file for OCR", type=["jpg", "png", "pdf", "jpeg", "webp"])

    if uploaded_file is not None:
        with st.spinner("Processing image..."):
            try:
                image = Image.open(io.BytesIO(uploaded_file.read()))

                # Convert image to grayscale for OCR processing
                image = image.convert('L')
                image = np.array(image)
                thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

                # Perform OCR
                if selected_language == "English":
                    reader = easyocr.Reader(['en'])
                elif selected_language == "Hindi":
                    reader = easyocr.Reader(['hi'])
                elif selected_language == "Marathi":
                    reader = easyocr.Reader(['mr'])
                else:
                    reader = easyocr.Reader(['en'])

                text = reader.readtext(thresh)
                extracted_text = '\n'.join([item[1] for item in text])

                # Display recognized text
                st.subheader("Recognized Text:")
                st.write(extracted_text)

                # Create PDF with extracted text
                c = canvas.Canvas("output.pdf", pagesize=letter)
                textobject = c.beginText(50, 750)
                for line in extracted_text.splitlines():
                    textobject.textLine(line)
                c.drawText(textobject)
                c.showPage()
                c.save()

                # Provide download option
                file_name = uploaded_file.name.split('.')[0] + " OCR by Hindav.pdf"
                with open("output.pdf", "rb") as f:
                    st.download_button("Download as PDF", f, file_name=file_name)

                os.remove("output.pdf")

            except Exception as e:
                st.error("Couldn't process the image. Please try again.")

# Image to PDF Tool
elif app_mode == "Image to PDF":
    st.header("Image to PDF Converter")

    # Toggle switch for OCR
    toggle = st.checkbox("Use OCR (Experimental)", value=False)

    # Upload an image file for conversion
    uploaded_file = st.file_uploader("Select an image file", type=["jpg", "png", "jpeg", "webp"], key="image_to_pdf")

    if uploaded_file is not None:
        with st.spinner("Loading..."):
            try:
                image = Image.open(io.BytesIO(uploaded_file.read()))

                if toggle:
                    # Process image for OCR
                    image = image.convert('RGB')  # Ensure image is in RGB mode for saving as JPEG
                    image = np.array(image)
                    thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

                    # OCR processing
                    reader = easyocr.Reader(['en'])
                    text = reader.readtext(thresh)
                    extracted_text = '\n'.join([item[1] for item in text])

                    # Create PDF with extracted text
                    c = canvas.Canvas("output.pdf", pagesize=letter)
                    textobject = c.beginText(50, 750)
                    for line in extracted_text.splitlines():
                        textobject.textLine(line)
                    c.drawText(textobject)
                    c.showPage()
                    c.save()

                    file_name = uploaded_file.name.split('.')[0] + " PDF by Hindav.pdf"
                    with open("output.pdf", "rb") as f:
                        st.download_button("Download as PDF", f, file_name=file_name)

                    os.remove("output.pdf")
                else:
                    # Direct image-to-PDF conversion
                    image = image.convert('RGB')  # Convert to RGB mode for JPEG
                    image_path = "image.jpg"
                    image.save(image_path, "JPEG")

                    c = canvas.Canvas("output.pdf", pagesize=letter)
                    c.drawImage(image_path, 0, 0, width=letter[0], height=letter[1])
                    c.showPage()
                    c.save()

                    os.remove(image_path)

                    file_name = uploaded_file.name.split('.')[0] + " PDF by Hindav.pdf"
                    with open("output.pdf", "rb") as f:
                        st.download_button("Download as PDF", f, file_name=file_name)

                    os.remove("output.pdf")

            except Exception as e:
                st.error("Couldn't process the image. Please try again.")

# Image & PDF Resizer
elif app_mode == "Image & PDF Resizer":
    st.header("Image & PDF Resizer")

    # Tabs for Image and PDF Resizer
    tab1, tab2 = st.tabs(["Image Resizer", "PDF Resizer"])

    # Image Resizer Tab
    with tab1:
        uploaded_image = st.file_uploader("Select an image file", type=["jpg", "png", "jpeg", "webp"], key="image_uploader")

        if uploaded_image is not None:
            st.subheader("Original Image")
            st.image(uploaded_image)

            zoom_level_toggle = st.checkbox("Zoom to Fit Page", value=False)
            original_size = uploaded_image.size / 1024  # Convert to KB
            st.write(f"Original Image Size: {original_size:.2f} KB")
            storage_size_kb = st.text_input("Enter Storage Size (KB)", value=f"{original_size:.2f}")

            with st.form("image_resizer_form"):
                submit_button = st.form_submit_button("Resize Image")

            if submit_button:
                try:
                    storage_size_kb = float(storage_size_kb)
                    if storage_size_kb > original_size:
                        st.error("Invalid storage size.")
                    else:
                        img = Image.open(uploaded_image)
                        width, height = img.size
                        new_width = int((storage_size_kb / original_size) * width)
                        new_height = int((storage_size_kb / original_size) * height)
                        img = img.resize((new_width, new_height))

                        st.subheader("Resized Image")
                        st.image(img)

                        original_image_name = os.path.splitext(uploaded_image.name)[0]
                        image_extension = uploaded_image.name.split('.')[-1]
                        file_name = f"{original_image_name} + Image Resize by Hindav.{image_extension}"
                        img.save(file_name)
                        with open(file_name, "rb") as file:
                            st.download_button("Download Resized Image", file, file_name=file_name)

                except ValueError:
                    st.error("Invalid storage size. Please enter a valid number.")

    # PDF Resizer Tab
    with tab2:
        uploaded_pdf = st.file_uploader("Select a PDF file", type=["pdf"], key="pdf_uploader")

        if uploaded_pdf is not None:
            pdf = PyPDF2.PdfReader(uploaded_pdf)
            st.subheader("Original PDF")
            st.write("Page Count: " + str(len(pdf.pages)))

            compression_level = st.selectbox("Select Compression Level", ["Low", "Medium", "High"])

            with st.form("pdf_compressor_form"):
                submit_button = st.form_submit_button("Compress PDF")

            if submit_button:
                compression_quality = 50 if compression_level == "Low" else 30 if compression_level == "Medium" else 10
                compressed_pdf = PyPDF2.PdfWriter()

                for page in pdf.pages:
                    compressed_pdf.add_page(page )

                with io.BytesIO() as buffer:
                    compressed_pdf.write(buffer)
                    compressed_pdf_data = buffer.getvalue()

                original_pdf_name = os.path.splitext(uploaded_pdf.name)[0]
                file_name = f"{original_pdf_name} + PDF Resize by Hindav.pdf"
                st.download_button("Download Compressed PDF", compressed_pdf_data, file_name=file_name)

# Custom footer
st.markdown("<p style='text-align: center; margin-top: 20px;'>Developed by <a href='https://github.com/hindav' target='_blank'>Hindav</a></p>", unsafe_allow_html=True)
