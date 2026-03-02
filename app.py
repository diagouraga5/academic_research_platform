# app.py
import streamlit as st
import pandas as pd

# Modules personnalisés
from modules.stats_analysis import stats_section
from modules.panel_models import panel_section
from modules.diff_in_diff import diff_in_diff_section
from modules.time_series import time_series_section

st.set_page_config(
    page_title="Academic Research Hub",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🎓 Academic Research Hub")
st.markdown("""
Plateforme interactive pour toutes vos analyses de données :
- Statistiques descriptives et avancées
- Modèles économétriques Panel
- Analyse d'impact (Difference-in-Differences)
- Séries temporelles et prévisions
""")

# Upload fichier multi-format
uploaded_file = st.file_uploader(
    "📂 Importez votre fichier (Excel, CSV, SPSS, Stata)",
    type=["xlsx","csv","sav","dta"],
    key="upload_data"
)

if uploaded_file is not None:
    file_type = uploaded_file.name.split('.')[-1]
    try:
        if file_type == "csv":
            df = pd.read_csv(uploaded_file)
        elif file_type == "xlsx":
            df = pd.read_excel(uploaded_file)
        elif file_type == "sav":
            import pyreadstat
            df, meta = pyreadstat.read_sav(uploaded_file)
        elif file_type == "dta":
            df = pd.read_stata(uploaded_file)
        else:
            st.error("Type de fichier non supporté")
            st.stop()
    except Exception as e:
        st.error(f"Erreur lors du chargement : {e}")
        st.stop()

    st.success(f"✅ Fichier chargé : {uploaded_file.name}")
    st.dataframe(df.head())

    # Menu latéral
    st.sidebar.header("🔹 Sections analytiques")
    analysis_type = st.sidebar.selectbox(
        "Choisissez la section",
        [
            "Statistiques descriptives & tests",
            "Panel Models",
            "Difference-in-Differences",
            "Séries temporelles"
        ],
        key="sidebar_select"
    )

    # Affichage section
    if analysis_type == "Statistiques descriptives & tests":
        stats_section(df)
    elif analysis_type == "Panel Models":
        panel_section(df)
    elif analysis_type == "Difference-in-Differences":
        diff_in_diff_section(df)
    elif analysis_type == "Séries temporelles":
        time_series_section(df)
else:
    st.info("⬆️ Importez un fichier pour commencer l'analyse")