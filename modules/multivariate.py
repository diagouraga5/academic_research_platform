import streamlit as st
import numpy as np
import plotly.express as px
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def multivariate_section(df):

    st.subheader("🔬 Analyse Multivariée (ACP)")

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    if st.checkbox("Lancer ACP") and len(numeric_cols) >= 2:

        X = df[numeric_cols].dropna()
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        pca = PCA(n_components=2)
        components = pca.fit_transform(X_scaled)

        fig = px.scatter(x=components[:,0],
                         y=components[:,1],
                         title="Projection ACP")
        st.plotly_chart(fig, use_container_width=True)

        st.write("Variance expliquée :", pca.explained_variance_ratio_)