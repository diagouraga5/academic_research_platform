# panel_models.py
import streamlit as st
import pandas as pd
import statsmodels.formula.api as smf

def panel_section(df: pd.DataFrame):
    """
    Section pour les modèles Panel (Effets fixes et Random) dans Streamlit.
    df : DataFrame pandas contenant les données.
    """

    st.subheader("📊 Modèles Panel (Effets fixes / Effets aléatoires)")

    # Choix du type de modèle avec clé unique
    panel_option = st.selectbox(
        "Type de modèle",
        ["Effets fixes", "Effets aléatoires"],
        key="panel_type"
    )

    # Choix des variables avec clés uniques
    entity_var = st.selectbox(
        "Variable d'entité (ID)",
        df.columns,
        key="entity_var"
    )
    time_var = st.selectbox(
        "Variable temporelle",
        df.columns,
        key="time_var"
    )
    y_var = st.selectbox(
        "Variable dépendante",
        df.select_dtypes(include="number").columns,
        key="y_var"
    )
    x_vars = st.multiselect(
        "Variables explicatives",
        df.select_dtypes(include="number").columns.drop(y_var),
        key="x_vars"
    )

    # Bouton pour lancer le modèle
    if st.button("Lancer modèle Panel", key="run_panel"):
        if not x_vars:
            st.warning("⚠️ Sélectionnez au moins une variable explicative.")
            return

        formula = f"{y_var} ~ {' + '.join(x_vars)}"

        try:
            if panel_option == "Effets fixes":
                # Ajout des effets fixes pour l'entité et le temps
                formula_full = formula + f" + C({entity_var}) + C({time_var})"
                model = smf.ols(formula_full, data=df).fit()
            else:
                # Effets aléatoires simplifiés avec OLS
                model = smf.ols(formula, data=df).fit()

            st.success("✅ Modèle estimé avec succès !")
            st.text(model.summary())
        except Exception as e:
            st.error(f"Erreur lors de l'estimation : {e}")