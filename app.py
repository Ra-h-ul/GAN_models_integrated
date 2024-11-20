import streamlit as st
import os
import subprocess
import sys

# Set fixed parameters for both ESRGAN and Fast-AgingGAN
UPLOAD_DIR_1 = "ESRGAN/LR"  # For ESRGAN
RESULTS_DIR_1 = "ESRGAN/results"   # For ESRGAN

UPLOAD_DIR_2 = "FAST_AGINGGAN/img"  # For FAST_AGINGGAN
RESULTS_DIR_2 = ""   # For FAST_AGINGGAN

VENV_ESRGAN_DIR = "ESRGAN/myenv"  # ESRGAN virtual environment directory
VENV_FAST_AGINGGAN_DIR = "FAST_AGINGGAN/myenv"  # Fast-AgingGAN virtual environment directory

ESRGAN_DIR = "ESRGAN"
FAST_AGINGGAN_DIR = "FAST_AGINGGAN"

# Function to clean a directory
def clean_directory(directory):
    if os.path.exists(directory):
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Remove file
                elif os.path.isdir(file_path):
                    os.rmdir(file_path)  # Remove directory
            except Exception as e:
                st.warning(f"Failed to delete {file_path}: {e}")
    else:
        os.makedirs(directory)  # Create directory if it doesn't exist

# Clean the upload and results directories at the start
clean_directory(UPLOAD_DIR_1)
clean_directory(UPLOAD_DIR_2)
clean_directory(RESULTS_DIR_1)

# Set page config for a custom layout
st.set_page_config(page_title="CycleGAN Projects", layout="wide")

# Add a custom header
st.markdown("""
    <h1 style="text-align:center; color:#4CAF50;">CycleGAN Projects</h1>
    <p style="text-align:center;">Choose a model and upload an image to see the results.</p>
""", unsafe_allow_html=True)

# Add a sidebar for navigation
st.sidebar.header("Navigation")
st.sidebar.markdown("Select a model to run.")

# Option to choose between ESRGAN and Fast-AgingGAN
model_choice = st.sidebar.selectbox("Select Model", ["ESRGAN", "Fast-AgingGAN"])

# File uploader widget
st.subheader("1. Upload Image")
if model_choice == "ESRGAN":
    uploaded_file = st.file_uploader("Upload an image file for ESRGAN", type=["jpg", "jpeg", "png"], accept_multiple_files=False)
else:
    uploaded_file = st.file_uploader("Upload an image file for Fast-AgingGAN", type=["jpg", "jpeg", "png"], accept_multiple_files=False)

if uploaded_file is not None:
    # Define the file save path based on model choice
    if model_choice == "ESRGAN":
        file_path = os.path.join(UPLOAD_DIR_1, uploaded_file.name)
    else:
        file_path = os.path.join(UPLOAD_DIR_2, uploaded_file.name)
    
    # Save the uploaded file
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success(f"File '{uploaded_file.name}' has been saved to '{file_path}'.")
    
    # Display the uploaded image
    st.image(file_path, caption="Uploaded Image", use_container_width=True)

# Button to run the selected model
if st.button(f"Run {model_choice}"):
    try:
        # Check if Python 3.8 is installed
        if sys.version_info < (3, 8):
            st.error("Python 3.8 or higher is required for this environment.")
            st.stop()

        # Define the command based on the selected model
        if model_choice == "ESRGAN":
            st.info("Running ESRGAN...")
            command = f"cd ESRGAN/ && pwd && source myenv/bin/activate && python 'test.py' --image_dir {UPLOAD_DIR_1} --results_dir {RESULTS_DIR_1}"
            
        else:
            st.info("Running Fast-AgingGAN...")
            command = f"source {VENV_FAST_AGINGGAN_DIR}/bin/activate && python {os.path.join(FAST_AGINGGAN_DIR, 'infer.py')} --image_dir {UPLOAD_DIR_2}"
        
        # Run the command in a subprocess using bash shell
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Display the command output
        st.subheader("Command Output")
        st.text(result.stdout)
        
        # Display any errors
        if result.stderr:
            st.subheader("Errors")
            st.text(result.stderr)

        # Check if the results folder contains the generated image
        st.subheader("Generated Results")
        
        if model_choice == "ESRGAN":
            result_images = [f for f in os.listdir(RESULTS_DIR_1) if f.lower().endswith(('png', 'jpg', 'jpeg'))]
        else:
            result_images = ["mygraph.png"]
        
        # Display results
        if result_images:
            for image_file in result_images:
                image_path = os.path.join(RESULTS_DIR_1,image_file) if model_choice == "ESRGAN" else os.path.join(RESULTS_DIR_2, image_file)
                st.image(image_path, caption=f"Generated Image: {image_file}", use_container_width=True)
        else:
            st.warning("No images found in the results folder.")
    
    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.info("Please upload an image to get started.")