# diff_in_diff.py
import streamlit as st
import statsmodels.formula.api as smf
import pandas as pd

def diff_in_diff_section(df: pd.DataFrame):
    st.subheader("📈 Difference-in-Differences (DiD)")

    treatment = st.selectbox(
        "Variable traitement (0/1)",
        df.columns,
        key="did_treatment"
    )
    time = st.selectbox(
        "Variable temporelle (0=avant, 1=après)",
        df.columns,
        key="did_time"
    )
    outcome = st.selectbox(
        "Variable résultat / outcome",
        df.select_dtypes(include="number").columns,
        key="did_outcome"
    )

    if st.button("Lancer DiD", key="run_did"):
        formula = f"{outcome} ~ {treatment}*{time}"
        try:
            model = smf.ols(formula, data=df).fit()
            st.success("✅ Modèle DiD estimé !")
            st.text(model.summary())
        except Exception as e:
            st.error(f"Erreur lors de l'estimation DiD : {e}")