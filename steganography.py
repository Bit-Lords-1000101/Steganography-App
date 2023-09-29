import streamlit as st
from PIL import Image
from stegano import lsb
import base64
import io

# Function to generate a download link for a file
def get_binary_file_downloader_html(bin_data, file_label='File', button_label='Download'):
    bin_str = base64.b64encode(bin_data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_label}">{button_label}</a>'
    return href

# Streamlit UI
st.title("Steganography Tool")

# Option to Encode or Decode
task = st.radio("Select a task:", ("Encode", "Decode"))

if task == "Encode":
    st.header("Encode Text into an Image")

    # Upload Image
    uploaded_image = st.file_uploader("Upload an image (PNG or JPG):", type=["png", "jpg", "jpeg"])
    if uploaded_image:
        original_image = Image.open(uploaded_image)
        st.image(original_image, caption="Original Image", use_column_width=True)

        # Enter Text to Hide
        text_to_hide = st.text_area("Enter text to hide:")
        if st.button("Encode Text"):
            if text_to_hide:
                # Encode the text into the image
                steganographic_image = lsb.hide(original_image, text_to_hide)

                # Convert steganographic image to bytes
                img_byte_array = io.BytesIO()
                steganographic_image.save(img_byte_array, format="PNG")
                st.image(steganographic_image, caption="Steganographic Image", use_column_width=True)

                # Download Button
                st.markdown(get_binary_file_downloader_html(img_byte_array.getvalue(), "Steganographic_Image.png", "Download Image"), unsafe_allow_html=True)

else:
    st.header("Decode Text from an Image")

    # Upload Steganographic Image
    uploaded_steganographic_image = st.file_uploader("Upload a steganographic image (PNG or JPG):", type=["png", "jpg", "jpeg"])
    if uploaded_steganographic_image:
        steganographic_image = Image.open(uploaded_steganographic_image)
        st.image(steganographic_image, caption="Steganographic Image", use_column_width=True)

        # Decode Button
        if st.button("Decode Text"):
            hidden_text = lsb.reveal(steganographic_image)
            st.write("Hidden Text:", hidden_text)
