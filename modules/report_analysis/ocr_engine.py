import streamlit as st
from PIL import Image


def ocr_engine():

    st.subheader("📄 OCR Report Reader")

    uploaded_file = st.file_uploader(
        "Upload Report Image",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_file is not None:

        try:

            image = Image.open(uploaded_file)

            st.image(
                image,
                caption="Uploaded Report",
                use_container_width=True
            )

            st.success(
                "Image uploaded successfully."
            )

            st.info(
                """
                OCR functionality can be integrated later using
                Tesseract OCR or EasyOCR.

                Current version is a placeholder module
                for the healthcare system.
                """
            )

        except Exception as e:

            st.error(
                f"Unable to process image: {e}"
            )