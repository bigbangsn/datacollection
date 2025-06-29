import streamlit as st

st.set_page_config(layout="wide")

st.title("📝 Évaluation")
st.write("Cette page vous permet de remplir un formulaire d'évaluation de l'application de scrapping.")

# Description du formulaire
st.markdown("""
## Formulaire d'évaluation
Veuillez remplir ce formulaire pour nous aider à améliorer notre application de scraping de données.
""")

# Conteneur pour le formulaire Kobo Toolbox
form_container = st.container()

with form_container:
    kobo_form_url = "https://ee.kobotoolbox.org/x/u2ERyw0E"

    st.components.v1.iframe(kobo_form_url, width=500,  height=800, scrolling=True)
