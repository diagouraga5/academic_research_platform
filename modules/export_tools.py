import streamlit as st

def export_section(df):

    st.subheader("📤 Export")

    if st.button("Exporter en CSV"):
        df.to_csv("export_data.csv", index=False)
        st.success("Fichier exporté dans le dossier du projet")