import streamlit as st
import pandas as pd
from urllib.parse import urlparse
from scrapping import scrape_data, save_to_csv

st.title("🏗️ Scraper les données avec SELENIUM")
st.write("Cette page vous permet de collecter des données depuis différentes sources.")

# URLs disponibles
URLS_DISPONIBLES = {
    "TV & Home Cinema": "https://www.expat-dakar.com/tv-home-cinema",
    "Téléphones": "https://www.expat-dakar.com/telephones",
    "Ordinateurs": "https://www.expat-dakar.com/ordinateurs"
}

# Initialiser les états de session
if "stop" not in st.session_state:
    st.session_state.stop = False
if "scraping_complete" not in st.session_state:
    st.session_state.scraping_complete = False
if "scraped_data" not in st.session_state:
    st.session_state.scraped_data = {}
if "show_data" not in st.session_state:
    st.session_state.show_data = False

st.subheader("Scraping des sources sélectionnées")

choix_urls = st.multiselect("Choisissez les catégories :", list(URLS_DISPONIBLES.keys()))
nb_pages = st.number_input("Nombre de pages à scraper :", min_value=1, max_value=50, value=2)

lancer = st.button("🚀 Lancer le scraping")
stopper = st.button("🛑 Stopper le scraping")

if stopper:
    st.session_state.stop = True
    st.warning("⏹️ Le scraping sera interrompu après la page en cours.")

if lancer and choix_urls:
    st.session_state.stop = False  # Réinitialiser le flag

    statut = st.empty()

    total_ops = len(choix_urls)

    # Réinitialiser les données scrapées
    st.session_state.scraped_data = {}

    for nom in choix_urls:
        if st.session_state.stop:
            st.error("⛔ Scraping interrompu par l'utilisateur.")
            break

        url = URLS_DISPONIBLES[nom]
        statut.info(f"🔄 Scraping : {nom}")

        with st.spinner(f"Scraping {nom} en cours..."):
            try:
                data = scrape_data(url, nb_pages)
                filename = f"{"donnee/"+urlparse(url).path.strip('/').split('/')[-1]}.csv"
                save_to_csv(filename, data)

                # Stocker les données dans la session
                st.session_state.scraped_data[nom] = {
                    "data": data,
                    "filename": filename
                }
            except Exception as e:
                st.error(f"❌ Erreur pour {nom} : {e}")

    # Marquer le scraping comme terminé
    st.session_state.scraping_complete = True
    statut.success("✅ Scraping terminé." if not st.session_state.stop else "⚠️ Scraping partiel terminé.")

elif lancer and not choix_urls:
    st.warning("Veuillez sélectionner au moins une catégorie à scraper.")

# Afficher le dialogue après la fin du scraping
if st.session_state.scraping_complete and st.session_state.scraped_data:
    with st.container():
        st.markdown("---")
        st.subheader("🎉 Scraping terminé avec succès!")
        st.write("Souhaitez-vous afficher les données collectées?")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("👁️ Afficher les données"):
                st.session_state.show_data = True
        with col2:
            if st.button("❌ Non merci"):
                st.session_state.show_data = False
                st.session_state.scraping_complete = False

    # Afficher les données si l'utilisateur le souhaite
    if "show_data" in st.session_state and st.session_state.show_data:
        st.markdown("---")
        st.subheader("📊 Données collectées")

        for nom, info in st.session_state.scraped_data.items():
            with st.expander(f"📄 Résultats de {nom}"):
                st.write(f"Fichier sauvegardé: {info['filename']}")
                st.write(pd.DataFrame(info['data'], columns=["Détails", "État", "Marque", "Adresse", "Prix", "Image"]))

                # Option pour télécharger les données
                csv = pd.DataFrame(info['data'], 
                                  columns=["Détails", "État", "Marque", "Adresse", "Prix", "Image"]).to_csv(index=False)
                st.download_button(
                    label=f"⬇️ Télécharger les données de {nom}",
                    data=csv,
                    file_name=f"{nom.lower().replace(' & ', '-').replace(' ', '-')}.csv",
                    mime="text/csv"
                )
