import streamlit as st
from PIL import Image
import io
import cv2
import numpy as np
import easyocr
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
import docx
from docx.shared import Pt
import time

# Hide the menu
st.config.showMenu = False

# Create a Streamlit app
st.title("EasyOCR-Based OCR App")

# Language selection option
languages = ["English", "Hindi", "Marathi", "Other"]
selected_language = st.selectbox("Select the language of the text", languages)

# Load the image file
uploaded_file = st.file_uploader("Select an image file", type=["jpg", "png", "pdf","jpeg","webp"])

if uploaded_file is not None:
    with st.spinner("Loading..."):
        image = Image.open(io.BytesIO(uploaded_file.read()))

        # Convert to grayscale
        image = image.convert('L')

        # Apply binary thresholding to segment out the text
                # Apply binary thresholding to segment out the text
        image = np.array(image)
        thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # Use EasyOCR to recognize text in the image
        if selected_language == "English":
            reader = easyocr.Reader(['en'])
        elif selected_language == "Hindi":
            reader = easyocr.Reader(['hi'])
        elif selected_language == "Marathi":
            reader = easyocr.Reader(['mr'])
        else:
            reader = easyocr.Reader(['en'])

        text = reader.readtext(thresh)

        # Extract the text from the output
        extracted_text = ''
        for item in text:
            extracted_text += item[1] + '\n'

        # Remove unwanted characters and numbers
        extracted_text = extracted_text.strip()  # Remove leading and trailing whitespace

    # Display the recognized text
    st.write("Recognized Text:")
    st.write(extracted_text)

    # Download options
    download_options = st.expander("Download Options")
    with download_options:
        download_format = st.selectbox("Select the download format", ["PDF", "Word", "TXT"])

        if download_format == "PDF":
            c = canvas.Canvas("output.pdf", pagesize=letter)
            styles = getSampleStyleSheet()
            styleN = styles["BodyText"]
            styleN.alignment = TA_LEFT
            styleN.fontSize = 12
            styleN.leading = 14
            styleN.fontName = "Helvetica"
            textobject = c.beginText(50, 750)
            for line in extracted_text.splitlines():
                textobject.textLine(line)
            c.drawText(textobject)
            c.showPage()
            c.save()
            with open("output.pdf", "rb") as f:
                file_name = uploaded_file.name.split('.')[0] + " OCR by Hindav" + '.pdf'
                st.download_button("Download as PDF", f, file_name=file_name, type="primary", key="pdf_download")

        elif download_format == "Word":
            doc = docx.Document()
            doc.add_paragraph(extracted_text)
            doc.save("output.docx")
            with open("output.docx", "rb") as f:
                file_name = uploaded_file.name.split('.')[0] + " OCR by Hindav" + '.docx'
                st.download_button("Download as Word", f, file_name=file_name, type="primary", key="word_download")

        elif download_format == "TXT":
            with open("output.txt", "w", encoding='utf-8') as f:
                f.write(extracted_text)
            with open("output.txt", "rb") as f:
                file_name = uploaded_file.name.split('.')[0] + " OCR by Hindav" + '.txt'
                st.download_button("Download as TXT", f, file_name=file_name, type="primary", key="txt_download")

# Add a message below the "Deploy" button
st.markdown("<p style='text-align: center; margin-top: 20px;'>Developed by <a href='https://github.com/hindav'>Hindav</a></p>", unsafe_allow_html=True)
