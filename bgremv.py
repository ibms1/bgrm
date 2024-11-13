import streamlit as st
from rembg import remove
from PIL import Image
import io
import base64
from datetime import datetime

def convert_image_to_bytes(img):
    """Convert PIL Image to bytes"""
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()

def get_image_download_link(img, filename):
    """Generate a download link for the processed image"""
    bin_str = base64.b64encode(convert_image_to_bytes(img)).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{filename}">Download Processed Image</a>'
    return href

def main():
    # Set page configuration
    st.set_page_config(
        page_title="Background Remover",
        page_icon="🖼️",
        layout="centered"
    )

    # Add header with styling
    st.markdown("""
        <h1 style='text-align: center; color: #2e7d32;'>
            🖼️ Background Remover Tool
        </h1>
    """, unsafe_allow_html=True)

    # Add description
    st.markdown("""
        This tool removes backgrounds from images using AI. 
        Simply upload an image and download the processed result!
    """)

    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an image...", 
        type=['png', 'jpg', 'jpeg', 'webp', 'bmp'],
        help="Supported formats: PNG, JPG, JPEG, WebP, BMP"
    )

    # Add columns for layout
    col1, col2 = st.columns(2)

    if uploaded_file is not None:
        # Read the image
        image = Image.open(uploaded_file)
        
        # Show original image
        with col1:
            st.subheader("Original Image")
            st.image(image, use_column_width=True)

        # Add a processing button
        if st.button("Remove Background", type="primary"):
            with st.spinner("Processing image..."):
                try:
                    # Remove background
                    output_image = remove(image)
                    
                    # Show processed image
                    with col2:
                        st.subheader("Processed Image")
                        st.image(output_image, use_column_width=True)

                    # Generate timestamp for unique filename
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_filename = f"no_bg_{timestamp}.png"

                    # Create download link
                    st.markdown("### Download")
                    st.markdown(
                        get_image_download_link(output_image, output_filename),
                        unsafe_allow_html=True
                    )

                    # Add usage tips
                    with st.expander("📝 Tips for best results"):
                        st.markdown("""
                            - Use images with clear subjects and contrasting backgrounds
                            - Ensure good lighting in the original image
                            - For best quality, use PNG format
                            - If the result isn't perfect, try adjusting the lighting or contrast of your original image
                        """)

                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    st.error("Please try with a different image or check if the image format is supported.")

    # Add footer with additional information
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #666;'>
            Made with ❤️ EASYKW
            <br>
            Upload limit: 200MB per image
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()