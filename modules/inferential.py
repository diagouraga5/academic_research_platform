import streamlit as st
import numpy as np
from scipy import stats

def inferential_section(df):

    st.subheader("🧪 Tests statistiques")

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    categorical_cols = df.select_dtypes(include="object").columns.tolist()

    if len(numeric_cols) >= 2:

        if st.checkbox("Corrélation Pearson"):
            x = st.selectbox("Variable X", numeric_cols)
            y = st.selectbox("Variable Y", numeric_cols, index=1)
            r, p = stats.pearsonr(df[x].dropna(), df[y].dropna())
            st.write(f"r = {round(r,3)} | p = {round(p,4)}")

        if st.checkbox("ANOVA"):
            if categorical_cols:
                group = st.selectbox("Variable catégorielle", categorical_cols)
                num = st.selectbox("Variable quantitative", numeric_cols)
                groups = df[group].unique()
                if len(groups) > 2:
                    samples = [df[df[group] == g][num] for g in groups]
                    f, p = stats.f_oneway(*samples)
                    st.write(f"F = {round(f,3)} | p = {round(p,4)}")