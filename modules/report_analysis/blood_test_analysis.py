import streamlit as st


def blood_test_analysis():

    st.subheader("🩸 Blood Test Analysis")

    hemoglobin = st.number_input(
        "Hemoglobin (g/dL)",
        min_value=0.0,
        value=13.5
    )

    wbc = st.number_input(
        "WBC Count",
        min_value=0,
        value=7000
    )

    platelets = st.number_input(
        "Platelet Count",
        min_value=0,
        value=250000
    )

    if st.button("Analyze Blood Test"):

        findings = []

        if hemoglobin < 12:
            findings.append("Low Hemoglobin (Possible Anemia)")

        if wbc > 11000:
            findings.append("High WBC (Possible Infection)")

        if platelets < 150000:
            findings.append("Low Platelets")

        if not findings:
            findings.append("All Values Within Normal Range")

        st.success("Analysis Complete")

        for item in findings:
            st.write("✔️", item)