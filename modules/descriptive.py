import streamlit as st
import numpy as np
import plotly.express as px
from scipy import stats

def descriptive_section(df):

    st.subheader("📊 Statistiques descriptives")

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    if numeric_cols:
        st.write(df[numeric_cols].describe())

        var = st.selectbox("Variable à visualiser", numeric_cols)
        fig = px.histogram(df, x=var, marginal="box")
        st.plotly_chart(fig, use_container_width=True)

        skew = stats.skew(df[var].dropna())
        kurt = stats.kurtosis(df[var].dropna())

        st.write(f"Skewness : {round(skew,3)}")
        st.write(f"Kurtosis : {round(kurt,3)}")