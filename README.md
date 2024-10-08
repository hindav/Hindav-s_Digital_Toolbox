Here’s a `README.md` file tailored for your Streamlit app based on the provided code:


# Hindav's Digital Toolbox

Hindav's Digital Toolbox is a versatile web application built with Streamlit, offering various tools for image processing, text extraction through OCR, and document conversion. This app is designed for users who need efficient solutions for managing images and PDFs.

## Features

- **OCR Tool**: Extract text from images using the EasyOCR library, supporting multiple languages.
- **Image to PDF Converter**: Convert images to PDF format, with an optional text extraction feature using OCR.
- **Image & PDF Resizer**: Resize images and PDFs based on user-defined storage sizes.
- **Custom Background**: The app features a custom background image for both the main content area and the sidebar with a blur effect.

## Demo

You can run the app locally by following the instructions below.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/hindav/hindavs-digital-toolbox.git
    cd hindavs-digital-toolbox
    ```

2. **Install dependencies**:
    Ensure you have Python 3.7 or above installed, then install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the app**:
    ```bash
    streamlit run app.py
    ```

4. **Access the app**:
    Open your web browser and navigate to:
    ```bash
    http://localhost:8501
    ```

## File Structure


hindavs-digital-toolbox/
│
├── app.py               # The main Streamlit application code
├── BG.jpg               # The background image for the app
├── requirements.txt      # List of required Python packages
└── README.md            # Project documentation


## Usage Instructions

1. Select a tool from the sidebar:
   - **OCR Tool**: Upload an image to extract text.
   - **Image to PDF**: Convert an image to PDF format.
   - **Image & PDF Resizer**: Resize images or PDFs based on specified storage sizes.

2. Follow the prompts to upload files, adjust settings, and download results.

## Dependencies

This project requires the following Python packages:

- `streamlit`: For building the web app interface.
- `easyocr`: For text extraction from images.
- `opencv-python`: For image processing.
- `numpy`: For numerical operations.
- `Pillow`: For image file handling.
- `PyPDF2`: For PDF file handling.
- `reportlab`: For generating PDF files.

You can install these dependencies using the provided `requirements.txt` file.

## Developed By

Developed by [Hindav](https://github.com/hindav).

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

