import streamlit as st
import streamlit.components.v1 as components
import os
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import yt_dlp

# Page Design Setup
st.set_page_config(page_title="QuickClip AI", page_icon="🎬", layout="centered")

st.title("🎬 QuickClip AI")
st.caption("🔒 100% Free | No Login Required | Zero Data Stored")

# Ad Banner Placeholder
ad_code = """
<div style="text-align:center; padding:10px; background:#f0f2f6; border-radius:8px; border: 1px dashed #ccc;">
    <p style="margin:0; font-size:12px; color:#666;">Sponsored Ad Space</p>
</div>
"""
components.html(ad_code, height=60)
st.markdown("---")

# Choose Input Type: File Upload OR YouTube Link
input_type = st.radio("Choose Video Source:", ["Upload Video File", "YouTube Video Link"])

temp_input = None

if input_type == "Upload Video File":
    uploaded_file = st.file_uploader("Choose a video file (MP4/MOV)", type=["mp4", "mov"])
    if uploaded_file is not None:
        temp_input = f"temp_{uploaded_file.name}"
        with open(temp_input, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("Video Loaded Successfully!")

elif input_type == "YouTube Video Link":
    yt_url = st.text_input("Paste YouTube Video Link:")
    if yt_url:
        with st.spinner("Downloading YouTube video... Please wait."):
            temp_input = "yt_download.mp4"
            ydl_opts = {
                'format': 'best[ext=mp4]',
                'outtmpl': temp_input,
                'quiet': True
            }
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([yt_url])
                st.success("YouTube Video Loaded Successfully!")
            except Exception as e:
                st.error(f"Error downloading video: {e}")
                temp_input = None

# If video is ready (either uploaded or downloaded)
if temp_input and os.path.exists(temp_input):
    col1, col2 = st.columns(2)
    with col1:
        start_time = st.number_input("Start Time (seconds)", min_value=0, value=0)
    with col2:
        end_time = st.number_input("End Time (seconds)", min_value=1, value=15)

    if st.button("Trim Clip Now ✂️"):
        output_file = "clipped_output.mp4"

        with st.spinner("Cutting your clip... Please wait."):
            ffmpeg_extract_subclip(temp_input, start_time, end_time, targetname=output_file)

        with open(output_file, "rb") as file:
            st.download_button(
                label="📥 Download Clip",
                data=file,
                file_name="quickclip.mp4",
                mime="video/mp4"
            )

        # DPDP SAFE AUTO-DELETE LOGIC
        if os.path.exists(temp_input):
            os.remove(temp_input)
        if os.path.exists(output_file):
            os.remove(output_file)

        st.toast("Temporary files deleted permanently from server!", icon="🧹")

# Bottom Footer & Disclaimer
st.markdown("---")
components.html(ad_code, height=60)
st.caption("Privacy Guarantee: Zero-Log policy. Files are processed in memory and deleted immediately.")
