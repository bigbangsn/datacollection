import streamlit as st
import pandas as pd
from urllib.parse import urlparse
from scrapping import scrape_data, save_to_csv

# URLs disponibles
URLS_DISPONIBLES = {
    "TV & Home Cinema": "https://www.expat-dakar.com/tv-home-cinema",
    "Téléphones": "https://www.expat-dakar.com/telephones",
    "Ordinateurs": "https://www.expat-dakar.com/ordinateurs"
}


def accueil():
    st.title("Bienvenue 👋")
    st.write("Salut ! Choisissez une action")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("1️⃣ Scraper les données"):
            st.session_state.page = "scraping"

    with col2:
        if st.button("2️⃣ Visualiser les données"):
            st.session_state.page = "visualisation"


def scraping():
    st.header("🔍 Scraping des données")

    choix_urls = st.multiselect(
        "Choisissez les catégories à scraper :",
        options=list(URLS_DISPONIBLES.keys())
    )

    nb_pages = st.number_input("Nombre de pages à scraper par catégorie :", min_value=1, max_value=100, value=2)

    if st.button("🚀 Lancer le scraping"):
        if not choix_urls:
            st.warning("Veuillez sélectionner au moins une catégorie.")
        else:
            for nom_categorie in choix_urls:
                url = URLS_DISPONIBLES[nom_categorie]
                st.info(f"Scraping de la catégorie : {nom_categorie}")
                try:
                    data = scrape_data(url, nb_pages)
                    filename = f"{urlparse(url).path.strip('/').split('/')[-1]}.csv"
                    save_to_csv(filename, data)
                    st.success(f"{len(data)} éléments scrappés pour {nom_categorie}. Fichier : {filename}")
                except Exception as e:
                    st.error(f"Erreur lors du scraping de {nom_categorie} : {e}")

    if st.button("⬅ Retour"):
        st.session_state.page = "accueil"


def visualisation():
    st.header("📊 Visualisation des données")

    fichiers = ["tv-home-cinema.csv", "telephones.csv", "ordinateurs.csv"]

    fichier_choisi = st.selectbox("Choisir un fichier CSV :", fichiers)

    try:
        df = pd.read_csv(fichier_choisi)
        st.dataframe(df)
    except FileNotFoundError:
        st.warning("Fichier non trouvé. Lancez le scraping d'abord.")

    if st.button("⬅ Retour"):
        st.session_state.page = "accueil"


# Gestion des pages
if "page" not in st.session_state:
    st.session_state.page = "accueil"

if st.session_state.page == "accueil":
    accueil()
elif st.session_state.page == "scraping":
    scraping()
elif st.session_state.page == "visualisation":
    visualisation()
