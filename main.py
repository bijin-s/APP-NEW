import os

import pandas as pd
import streamlit as st

import pyrebase

config={
      "apiKey": "AIzaSyDxtA-8bpJRT8Go2Vj8dlHswfsAjSTSvo8",
  "authDomain": "solar-modem-381304.firebaseapp.com",
  "projectId": "solar-modem-381304",
  "storageBucket": "solar-modem-381304.appspot.com",
  "messagingSenderId": "971073651512",
  "appId": "1:971073651512:web:8f58f2d9b1ef5385dd37cd",
  "measurementId": "G-NKTJYNB0TY",
  "databaseURL":""
}

firebase=pyrebase.initialize_app(config)

storage=firebase.storage()

path_on_cloud= "images/"
#storage.child(path_on_cloud).put(path_local)

STYLE = """
<style>
img {
    max-width: 100%;
}
</style>
"""

UPLOAD_DIRECTORY = "uploads"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


def save_file(file):
    file_path = os.path.join(UPLOAD_DIRECTORY, file.name)
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
                mime_type = "auto"
                if file_name.endswith(".csv"):
                    mime_type = "text/csv"
                elif file_name.endswith(".jpg") or file_name.endswith(".jpeg"):
                    mime_type = "image/jpeg"
                elif file_name.endswith(".png"):
                    mime_type = "image/png"
                elif file_name.endswith(".mp4"):
                    mime_type = "video/mp4"
                elif file_name.endswith(".webm"):
                    mime_type = "video/webm"
                elif file_name.endswith(".ogg"):
                    mime_type = "audio/ogg"
                storage.child(os.path.join(mime_type,file_name)).put(file_path)
                st.write("File ",file_name," is uploaded to cloud")
                file_data = open(file_path, "rb").read()
                

                st.download_button(
                    label="Download " + file_name,
                    data=file_data,
                    file_name=file_name,
                    mime=mime_type
                )
        
        if uploaded_images:
            st.success("Uploaded images:")
            col_num = 3
            rows = [uploaded_images[i:i + col_num] for i in range(0, len(uploaded_images), col_num)]
            for row in rows:
                cols = st.columns(col_num)
                for i, file in enumerate(row):
                    with cols[i]:
                        st.image(file, use_column_width=True)


if __name__ == "__main__":
    helper = FileUpload()
    helper.run()
