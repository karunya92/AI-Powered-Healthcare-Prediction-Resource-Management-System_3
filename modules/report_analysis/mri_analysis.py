import streamlit as st


def mri_analysis():

    st.subheader("🧠 MRI Analysis")

    uploaded_file = st.file_uploader(
        "Upload MRI Scan",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_file:

        st.image(
            uploaded_file,
            caption="Uploaded MRI",
            use_container_width=True
        )

        if st.button("Analyze MRI"):

            st.success(
                "MRI appears normal (Demo Analysis)"
            )

            st.info(
                "Integrate CNN/TensorFlow MRI model later."
            )