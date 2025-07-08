import streamlit as st
import requests

# Set page layout
st.set_page_config(layout="wide")

# Title
st.title("Marketing Campaign Agent")

# Create two columns
col1, col2 = st.columns([1, 2])

# Left: user input
with col1:
    user_input = st.text_area("Enter your campaign idea or prompt:")
    submit = st.button("Generate Response")

# Right: display result
with col2:
    if submit and user_input.strip():
        try:
            with st.spinner("Generating campaign... Please wait."):
                response = requests.post(
                    "http://127.0.0.1:8000/prompt",
                    json={"prompt": user_input}
                )
                response.raise_for_status()
                result = response.json()

            st.markdown("### Agent Response:")
            st.markdown(result.get("prompt_response", "No response found."))

        except requests.exceptions.RequestException as e:
            st.error(f"Error: {e}")