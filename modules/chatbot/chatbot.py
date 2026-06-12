import streamlit as st


def chatbot():

    st.subheader("🤖 Healthcare Chatbot")

    user_query = st.text_input(
        "Ask a healthcare question"
    )

    if st.button("Send"):

        query = user_query.lower()

        if "fever" in query:
            response = (
                "Drink plenty of fluids, rest well, "
                "and consult a doctor if symptoms persist."
            )

        elif "diabetes" in query:
            response = (
                "Monitor blood sugar levels regularly "
                "and follow your doctor's advice."
            )

        elif "heart" in query:
            response = (
                "Maintain a healthy diet and consult a "
                "cardiologist for persistent symptoms."
            )

        elif "covid" in query:
            response = (
                "Monitor symptoms and seek medical care "
                "if breathing difficulties occur."
            )

        else:
            response = (
                "Please consult a healthcare professional "
                "for accurate medical advice."
            )

        st.success(response)