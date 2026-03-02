import streamlit as st

def cleaning_section(df):
    st.subheader("🧹 Diagnostic des données")

    col1, col2, col3 = st.columns(3)
    col1.metric("Observations", df.shape[0])
    col2.metric("Variables", df.shape[1])
    col3.metric("Valeurs manquantes", df.isna().sum().sum())

    if st.checkbox("Supprimer lignes avec valeurs manquantes"):
        df.dropna(inplace=True)
        st.success("Valeurs manquantes supprimées")