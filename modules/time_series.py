# time_series.py
import streamlit as st
from statsmodels.tsa.arima.model import ARIMA
import pandas as pd

def time_series_section(df: pd.DataFrame):
    st.subheader("📊 Séries temporelles (ARIMA)")

    ts_var = st.selectbox(
        "Variable à modéliser",
        df.select_dtypes(include="number").columns,
        key="ts_var"
    )
    order_input = st.text_input(
        "Ordre ARIMA (p,d,q)",
        "1,1,1",
        key="arima_order"
    )

    if st.button("Lancer ARIMA", key="run_arima"):
        try:
            p, d, q = [int(x) for x in order_input.split(",")]
            model = ARIMA(df[ts_var].dropna(), order=(p,d,q)).fit()
            st.success("✅ Modèle ARIMA estimé !")
            st.text(model.summary())
        except Exception as e:
            st.error(f"Erreur ARIMA : {e}")