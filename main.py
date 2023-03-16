import os
from base64 import b64encode

import pandas as pd
import streamlit as st

STYLE = """
<style>
img {
    max-width: 100%;
}
</style>
"""

PUBLIC_DIRECTORY = "public"

if not os.path.exists(PUBLIC_DIRECTORY):
    os.makedirs(PUBLIC_DIRECTORY)


def save_file(file):
    file_path = os.path.join(PUBLIC_DIRECTORY, file.name)
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())
    return file_path


class FileUpload(object):

    def __init__(self):
        self.fileTypes = ["csv", "png", "jpg", "jpeg", "mp4", "webm", "ogg"]

    def run(self):
        """
        Upload File on Streamlit Code
        :return:
        """
        st.info(__doc__)
        st.markdown(STYLE, unsafe_allow_html=True)
        files = st.file_uploader("Upload files", type=self.fileTypes, accept_multiple_files=True)
        if not files:
            st.warning("Please upload a file of type: " + ", ".join(self.fileTypes))
            return
        selected_files = []
        uploaded_images = []
        for file in files:
            if file.type.startswith('image/'):
                uploaded_images.append(file)
            elif file.type.startswith('video/'):
                st.video(file)
            elif file.type == 'text/csv':
                data = pd.read_csv(file)
                st.dataframe(data.head(10))
            else:
                st.warning("Unsupported file type: " + file.type)
                continue
            file_path = save_file(file)
            selected_files.append(file_path)
        if selected_files:
            st.success("Saved files:")
            for file_path in selected_files:
                st.write(file_path)
                file_name = os.path.basename(file_path)
                st.markdown(get_download_link(file_path, file_name), unsafe_allow_html=True)
        if uploaded_images:
            st.success("Uploaded images:")
            col_num = 3
            rows = [uploaded_images[i:i + col_num] for i in range(0, len(uploaded_images), col_num)]
            for row in rows:
                cols = st.columns(col_num)
                for i, file in enumerate(row):
                    with cols[i]:
                        st.image(file, use_column_width=True)


def get_download_link(file_path, file_name):
    """
    Generate a download link for a file.
    """
    with open(file_path, "rb") as f:
        data = f.read()
    href = f'<a href="data:application/octet-stream;base64,{b64encode(data).decode()}" download="{file_name}">Download {file_name}</a>'
    return href


if __name__ == "__main__":
    helper = FileUpload()
    helper.run()
