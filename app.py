import streamlit as st
from dotenv import load_dotenv, find_dotenv
import os
import google.generativeai as genai
from PIL import Image

# 1. Load Environment Variables
load_dotenv(find_dotenv())
api_key = os.getenv("GOOGLE_API_KEY")

# 2. Page Configuration
st.set_page_config(page_title="Adonis AI", page_icon="🔮")

# 3. Secure API Configuration
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("❌ API Key not found. Check your .env file naming and location.")
    st.stop()

def get_gemini_response(input_prompt, image_parts):
    model = genai.GenerativeModel("gemini-2.5-flash") 
    response = model.generate_content([input_prompt, image_parts[0]])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No image uploaded.")

# --- UI Layout ---
st.sidebar.title("Navigation Bar")
st.sidebar.header("Upload Section")
uploaded_file = st.sidebar.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

st.header("Adonis AI")

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_container_width=True)

submit = st.button("Analyse this food") # Fixed spelling

input_prompt = """
You are an expert nutritionist. If the image contains food:
1. Identify the Meal Name.
2. List ingredients with estimated calories.
3. Provide Total Calories.
4. Give a health verdict and Macro split (Protein/Carbs/Fats %).
5. Mention fiber content.

If NO food is detected, simply say: "No food items detected in the image."
"""

if submit:
    if uploaded_file is not None:
        with st.spinner("Analyzing your meal..."):
            try:
                image_data = input_image_setup(uploaded_file)
                response = get_gemini_response(input_prompt, image_data)
                st.success("Analysis Complete!")
                st.subheader("Food Analysis Results")
                st.write(response)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please upload an image first!")

st.write("---")
st.caption("Upload a meal photo to get started.")