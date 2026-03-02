import streamlit as st
import numpy as np
import statsmodels.api as sm

def regression_section(df):

    st.subheader("📈 Régression")

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    if len(numeric_cols) >= 2:

        y_var = st.selectbox("Variable dépendante", numeric_cols)
        X_vars = [c for c in numeric_cols if c != y_var]

        if st.button("Lancer OLS"):
            X = sm.add_constant(df[X_vars])
            model = sm.OLS(df[y_var], X, missing="drop").fit()
            st.text(model.summary())