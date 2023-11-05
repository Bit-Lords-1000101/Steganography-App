import streamlit as st
from PIL import Image
from utils import text_to_binary, hide_text_in_image, extract_text_from_image, verify_image_integrity
from loguru import logger
import sys

# Logging
logger.add("app.log")

class StreamlitLogToCustomLog:
    def write(self, message, type):
        if type == "stdout":
            logger.info(message)
        elif type == "stderr":
            logger.error(message)

# Streamlit UI
st.title("Steganography and Forensic Tool")
st.text("Hide text in an image and then decode it back and verify image integrity.")

sys.stdout = StreamlitLogToCustomLog()
sys.stderr = StreamlitLogToCustomLog()

task = st.radio("Select a task:", ("Encode Text into Image", "Decode Text from Image", "Verify Image Integrity"))

if task == "Encode Text into Image":
    logger.info("Encode Text into Image selected.")
    st.header("Encode Text into an Image")

    uploaded_image = st.file_uploader("Upload an image (PNG or JPG):", type=["png", "jpg", "jpeg"])
    if uploaded_image:
        original_image = Image.open(uploaded_image)
        st.image(original_image, caption="Original Image", use_column_width=True)

        text_to_hide = st.text_area("Enter text to hide:")
        if st.button("Encode Text"):
            if text_to_hide:
                steganographic_image_path = uploaded_image.name.split(".")[0] + "_steganographic.png"
                hide_text_in_image(uploaded_image, text_to_hide, steganographic_image_path)

elif task == "Decode Text from Image":
    logger.info("Decode Text from Image selected.")
    st.header("Decode Text from an Image")

    uploaded_steganographic_image = st.file_uploader("Upload a steganographic image (PNG or JPG):", type=["png", "jpg", "jpeg"])
    if uploaded_steganographic_image:
        steganographic_image = Image.open(uploaded_steganographic_image)
        st.image(steganographic_image, caption="Steganographic Image", use_column_width=True)

        if st.button("Decode Text"):
            try:
                extracted_text = extract_text_from_image(uploaded_steganographic_image)
                st.success("Hidden Text: " + extracted_text)
            except Exception as e:
                logger.error(str(e))
                st.error(str(e))

elif task == "Verify Image Integrity":
    logger.info("Verify Image Integrity selected.")
    st.header("Verify Image Integrity")

    uploaded_original_image = st.file_uploader("Upload an original image (PNG or JPG):", type=["png", "jpg", "jpeg"])
    uploaded_steganographic_image = st.file_uploader("Upload a steganographic image (PNG or JPG):", type=["png", "jpg", "jpeg"])

    if uploaded_original_image and uploaded_steganographic_image:
        original_image = Image.open(uploaded_original_image)
        st.image(original_image, caption="Original Image", use_column_width=True)

        steganographic_image = Image.open(uploaded_steganographic_image)
        st.image(steganographic_image, caption="Steganographic Image", use_column_width=True)

        if st.button("Verify Image Integrity"):
            try:
                uploaded_original_image_path = uploaded_original_image.name
                uploaded_steganographic_image_path = uploaded_steganographic_image.name
                is_integrity_verified = verify_image_integrity(uploaded_original_image_path, uploaded_steganographic_image_path)
                if is_integrity_verified:
                    st.success("Image integrity verified.")
                else:
                    st.error("Image integrity not verified.")
            except Exception as e:
                logger.error(str(e))
                st.error(str(e))