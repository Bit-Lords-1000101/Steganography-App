import streamlit as st
from PIL import Image
import hashlib

# Function to calculate the hash of an image
def calculate_image_hash(image_path):
    hasher = hashlib.sha256()
    with open(image_path, "rb") as image_file:
        while True:
            data = image_file.read(65536)  # Read the image in chunks
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()

# Function to verify image integrity
def verify_image_integrity(original_image_path, steganographic_image_path):
    original_hash = calculate_image_hash(original_image_path)
    steganographic_hash = calculate_image_hash(steganographic_image_path)

    if original_hash == steganographic_hash:
        return True
    else:
        return False

# Function to convert text to binary
def text_to_binary(text):
    binary = ''.join(format(ord(char), '08b') for char in text)
    return binary

def hide_text_in_image(image_path, text_to_hide, output_path):
    binary_text = text_to_binary(text_to_hide)
    binary_text += '1111111100000000'  # Add a delimiter '1111111100000000' to mark the end
    img = Image.open(image_path)
    width, height = img.size
    max_chars = (width * height * 3) // 8

    if len(binary_text) > max_chars:
        raise ValueError("Text is too large to hide in the image.")

    data_index = 0
    img_data = img.getdata()
    encoded_pixels = []

    for pixel in img_data:
        if data_index < len(binary_text):
            red = pixel[0]
            green = pixel[1]
            blue = pixel[2]
            red = red & 254 | int(binary_text[data_index])
            data_index += 1
            encoded_pixels.append((red, green, blue))
        else:
            encoded_pixels.append(pixel)

    encoded_img = Image.new('RGB', (width, height))
    encoded_img.putdata(encoded_pixels)
    encoded_img.save(output_path)
    st.image(encoded_img, caption="Steganographic Image", use_column_width=True)
    st.success(f"Text hidden in the image and saved as {output_path}")

def extract_text_from_image(image_path):
    img = Image.open(image_path)
    img_data = img.getdata()
    binary_text = ''
    delimiter = '1111111100000000'  # Delimiter to mark the end of the hidden message

    for pixel in img_data:
        red = pixel[0]
        binary_text += str(red & 1)

    # Find the position of the delimiter
    delimiter_position = binary_text.find(delimiter)

    if delimiter_position != -1:
        binary_text = binary_text[:delimiter_position]
        text = ''.join(chr(int(binary_text[i:i+8], 2)) for i in range(0, len(binary_text), 8))
        return text
    else:
        raise ValueError("Delimiter not found, could not extract text.")