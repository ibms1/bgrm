import streamlit as st
from rembg import remove
from PIL import Image, ImageOps
import io
import base64
from datetime import datetime

# Set page configuration and styling
st.set_page_config(
    page_title="🎨 AI Background Wizard",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Define color options
COLORS = {
    "Red": "#FF0000",
    "Green": "#00FF00",
    "Blue": "#0000FF",
    "Yellow": "#FFFF00",
    "Purple": "#FF00FF",
    "Cyan": "#00FFFF",
    "White": "#FFFFFF",
    "Black": "#000000",
    "Gray": "#808080",
    "Brown": "#A52A2A",
    "Orange": "#FFA500",
    "Pink": "#FFC0CB"
}

# Custom CSS styles
st.markdown("""
    <style>
        .main {
            padding: 2rem;
        }
        
        .title-container {
            background: linear-gradient(90deg, #1e88e5, #005cb2);
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            text-align: center;
            color: white;
        }
        
        .upload-container {
            background-color: #f8f9fa;
            padding: 2rem;
            border-radius: 10px;
            border: 2px dashed #1e88e5;
            margin-bottom: 1.5rem;
        }
        
        .preview-container {
            background-color: #ffffff;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 1rem 0;
        }
        
        .image-info {
            background-color: #f8f9fa;
            padding: 0.5rem;
            border-radius: 4px;
            margin-top: 0.5rem;
            font-size: 0.9rem;
        }
        
        .result-container {
            margin-top: 1rem;
            text-align: center;
            padding: 1rem;
            background-color: transparent;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .stButton button {
            background-color: #1e88e5;
            color: white;
            border-radius: 5px;
            padding: 0.5rem 2rem;
            transition: all 0.3s;
        }
        
        .download-link {
            display: inline-block;
            background-color: #4caf50;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 5px;
            margin-top: 1rem;
            transition: all 0.3s;
        }
        
        .footer {
            text-align: center;
            padding: 2rem;
            background: linear-gradient(90deg, #1e88e5, #005cb2);
            color: white;
            border-radius: 10px;
            margin-top: 2rem;
        }
        
        .transparent-bg {
            position: relative;
            width: 100%;
            background-color: white;
        }
        
        .transparent-bg::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-image: 
                linear-gradient(45deg, #808080 25%, transparent 25%),
                linear-gradient(-45deg, #808080 25%, transparent 25%),
                linear-gradient(45deg, transparent 75%, #808080 75%),
                linear-gradient(-45deg, transparent 75%, #808080 75%);
            background-size: 20px 20px;
            background-position: 0 0, 0 10px, 10px -10px, -10px 0px;
            z-index: 0;
        }
        
        .transparent-bg img {
            position: relative;
            z-index: 1;
            display: block;
            margin: 0 auto;
            max-width: 100%;
            height: auto;
        }
    </style>
""", unsafe_allow_html=True)

def get_file_info(file, image):
    """Get file information"""
    size_kb = file.size / 1024
    width, height = image.size
    return f"Size: {size_kb:.1f} KB • Format: {image.format} • Dimensions: {width}x{height}px"

def create_colored_background(color_hex, size):
    """Create a solid color background image"""
    return Image.new('RGBA', size, color_hex)

def convert_image_to_bytes(img):
    """Convert PIL Image to bytes"""
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()

def get_image_download_link(img, filename):
    """Generate a styled download link for the processed image"""
    bin_str = base64.b64encode(convert_image_to_bytes(img)).decode()
    href = f'''
        <a href="data:application/octet-stream;base64,{bin_str}" 
           download="{filename}" 
           class="download-link">
            📥 Download Image
        </a>
    '''
    return href

def merge_with_new_background(foreground, background):
    """Merge the foreground with a new background"""
    background = background.resize(foreground.size, Image.LANCZOS)
    background.paste(foreground, (0, 0), mask=foreground)
    return background

def process_image(image):
    """Process image for background removal"""
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    output_bytes = remove(img_byte_arr)
    return Image.open(io.BytesIO(output_bytes))

def main():
    # Title and Introduction
    st.markdown("""
        <div class="title-container">
            <h1>🎨 AI Background Wizard</h1>
            <p>Transform your images with our advanced background removal and replacement tool</p>
        </div>
    """, unsafe_allow_html=True)

    # Main content area
    st.markdown('<div class="upload-container">', unsafe_allow_html=True)
    st.markdown("### 📸 Upload Image")
    uploaded_file = st.file_uploader(
        "Choose an image",
        type=['png', 'jpg', 'jpeg', 'webp', 'bmp']
    )

    # Image preview and info
    if uploaded_file is not None:
        main_image = Image.open(uploaded_file)
        st.markdown('<div class="preview-container">', unsafe_allow_html=True)
        preview_col1, preview_col2 = st.columns([1, 2])
        
        with preview_col1:
            st.image(main_image, width=200, caption="Preview")
        
        with preview_col2:
            st.markdown("#### Image Details")
            st.markdown(f'<div class="image-info">{get_file_info(uploaded_file, main_image)}</div>', 
                       unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Background options
        st.markdown("### 🎨 Background Options")
        background_type = st.radio(
            "Choose background type",
            ["None", "Color", "Image"],
            horizontal=True
        )

        if background_type == "Color":
            color_name = st.selectbox("Select background color", list(COLORS.keys()))
            background_color = COLORS[color_name]
        elif background_type == "Image":
            background_file = st.file_uploader(
                "Upload background image",
                type=['png', 'jpg', 'jpeg', 'webp', 'bmp']
            )
            if background_file:
                bg_image = Image.open(background_file)
                st.markdown('<div class="preview-container">', unsafe_allow_html=True)
                preview_col1, preview_col2 = st.columns([1, 2])
                
                with preview_col1:
                    st.image(bg_image, width=200, caption="Background Preview")
                
                with preview_col2:
                    st.markdown("#### Background Image Details")
                    st.markdown(f'<div class="image-info">{get_file_info(background_file, bg_image)}</div>', 
                               unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Process button
        if st.button("🔮 Process Image", type="primary", use_container_width=True):
            try:
                with st.spinner("✨ Processing..."):
                    progress_bar = st.progress(0)
                    
                    # Remove background
                    progress_bar.progress(30)
                    foreground = process_image(main_image)
                    progress_bar.progress(60)

                    # Create final image based on background choice
                    if background_type == "Color":
                        background = create_colored_background(background_color, foreground.size)
                        final_image = merge_with_new_background(foreground, background)
                    elif background_type == "Image" and background_file is not None:
                        background = Image.open(background_file)
                        final_image = merge_with_new_background(foreground, background)
                    else:  # None option - transparent background
                        final_image = foreground

                    progress_bar.progress(90)

                    # Display result
                    st.markdown("### ✨ Final Result")
                    if background_type == "None":
                        st.markdown("""
                            <div class="transparent-bg">
                                <img src="data:image/png;base64,{}"/>
                            </div>
                        """.format(base64.b64encode(convert_image_to_bytes(final_image)).decode()), unsafe_allow_html=True)
                    else:
                        st.image(final_image, use_column_width=True)
                    
                    # Download button
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_filename = f"processed_{timestamp}.png"
                    st.markdown(get_image_download_link(final_image, output_filename), unsafe_allow_html=True)
                    
                    progress_bar.progress(100)
                    st.success("✅ Processing completed successfully!")

            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.error("Please try with a different image or check if the image format is supported.")

    # Footer
    st.markdown("""
        <div class="footer">
            <h3>🌟 AI Background Wizard</h3>
            <p>Made with ❤️ by EASYKW</p>
            <small>Maximum upload size: 200MB per image</small>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()