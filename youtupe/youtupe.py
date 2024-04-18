import streamlit as st
from pytube import YouTube
from PIL import Image 
import os

# Function to download YouTube video with specified resolution and English subtitles
def download_youtube_video_with_subtitles(video_url, output_path, resolution):
    try:
        # Create a YouTube object
        yt = YouTube(video_url)

        # Get the stream with the specified resolution
        stream = yt.streams.filter(res=resolution, file_extension='mp4').first()

        # Calculate total size of the video
        total_size = stream.filesize

        # Create a progress bar
        progress_bar = st.progress(0)

        # Download the video with English subtitles
        with st.spinner("Downloading..."):
            stream.download(output_path, filename_prefix="")

        # Update progress bar as the video is being downloaded
        bytes_downloaded = 0
        while bytes_downloaded < total_size:
            bytes_downloaded = os.path.getsize(os.path.join(output_path, f"{stream.default_filename}"))
            progress_bar.progress(min(bytes_downloaded / total_size, 1.0))

        st.write("Download complete!")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Streamlit UI
st.markdown("<h1 style='text-align: center;'>YOUTUBE VIDEO DOWNLOADER</h1>", unsafe_allow_html=True)
st.title('')
image = Image.open(r"img.png")
st.image(image, use_column_width=True)

st.write('')
st.write('')
st.write('')
video_url = st.text_input("Enter YouTube Video URL:")

# Display YouTube video thumbnail below the input field
if video_url:
    try:
        yt = YouTube(video_url)
        thumbnail_url = yt.thumbnail_url
        st.image(thumbnail_url, caption='YouTube Video Thumbnail', use_column_width=True)
        st.markdown(f"<p style='text-align: center; font-weight: bold;'>Video Name: {yt.title}</p>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Failed to fetch video thumbnail: {str(e)}")

st.write('')
st.write('')
resolution = st.selectbox("Select Resolution:", ['720p', '480p', '360p'])
st.write('')
st.write('')

if st.button("Download"):
    if video_url:
        output_path = "downloaded_video"
        download_youtube_video_with_subtitles(video_url, output_path, resolution)
    else:
        st.warning("Please enter a YouTube video URL.")
