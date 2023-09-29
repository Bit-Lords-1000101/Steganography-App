import streamlit as st
from PIL import Image
from utils import text_to_binary, hide_text_in_image, extract_text_from_image

# Streamlit UI
st.title("LSB Steganography Tool")

task = st.radio("Select a task:", ("Encode Text into Image", "Decode Text from Image"))

if task == "Encode Text into Image":
    st.header("Encode Text into an Image")

    uploaded_image = st.file_uploader("Upload an image (PNG or JPG):", type=["png", "jpg", "jpeg"])
    if uploaded_image:
        original_image = Image.open(uploaded_image)
        st.image(original_image, caption="Original Image", use_column_width=True)

        text_to_hide = st.text_area("Enter text to hide:")
        if st.button("Encode Text"):
            if text_to_hide:
                steganographic_image_path = "steganographic_image.png"
                hide_text_in_image(uploaded_image, text_to_hide, steganographic_image_path)

elif task == "Decode Text from Image":
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
                st.error(str(e))
