# stats_analysis.py
import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from scipy import stats

def stats_section(df: pd.DataFrame):
    st.subheader("📊 Statistiques descriptives et tests avancés")

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    cat_cols = df.select_dtypes(include="object").columns.tolist()

    num_var = st.selectbox("Variable numérique", numeric_cols, key="num_var_stats")
    cat_var = st.selectbox("Variable catégorielle", [None]+cat_cols, key="cat_var_stats")

    # Résumé descriptif
    if cat_var:
        desc_df = df.groupby(cat_var)[num_var].describe()
    else:
        desc_df = df[num_var].describe()
    st.dataframe(desc_df)

    # Graphiques interactifs
    st.markdown("### 📈 Visualisations interactives")
    if cat_var:
        fig_box = px.box(df, x=cat_var, y=num_var, points="all", color=cat_var)
        fig_hist = px.histogram(df, x=num_var, color=cat_var, marginal="box", barmode="overlay")
    else:
        fig_box = px.box(df, y=num_var, points="all")
        fig_hist = px.histogram(df, x=num_var, marginal="box")
    st.plotly_chart(fig_box, use_container_width=True)
    st.plotly_chart(fig_hist, use_container_width=True)

    # Tests statistiques
    st.markdown("### ⚡ Tests statistiques")
    test_type = st.selectbox(
        "Sélectionnez un test",
        ["Aucun", "t-test (2 groupes)", "ANOVA", "Corrélation Pearson", "Corrélation Spearman"],
        key="test_stats"
    )

    if test_type == "t-test (2 groupes)" and cat_var:
        groups = df[cat_var].dropna().unique()
        if len(groups) == 2:
            g1 = df[df[cat_var]==groups[0]][num_var].dropna()
            g2 = df[df[cat_var]==groups[1]][num_var].dropna()
            tstat, pval = stats.ttest_ind(g1, g2)
            st.write(f"t-stat = {tstat:.3f}, p-value = {pval:.3f}")
        else:
            st.warning("⚠️ t-test : exactement 2 groupes requis")

    elif test_type == "ANOVA" and cat_var:
        groups = df[cat_var].dropna().unique()
        samples = [df[df[cat_var]==g][num_var].dropna() for g in groups]
        fstat, pval = stats.f_oneway(*samples)
        st.write(f"F-stat = {fstat:.3f}, p-value = {pval:.3f}")

    elif test_type == "Corrélation Pearson":
        st.dataframe(df[numeric_cols].corr(method="pearson"))

    elif test_type == "Corrélation Spearman":
        st.dataframe(df[numeric_cols].corr(method="spearman"))

    # Export Excel
    st.markdown("### 💾 Export des résultats")
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        desc_df.to_excel(writer, sheet_name="Descriptif")
        if cat_var:
            pd.crosstab(df[cat_var], df[num_var]).to_excel(writer, sheet_name="Crosstab")
    st.download_button(
        label="📥 Télécharger résultats Excel",
        data=buffer.getvalue(),
        file_name="stats_results.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )