import streamlit as st

st.image("logo_dit.png", width=300)
st.image("logo_expat.png", width=300)
st.title("EXAMEN DE SCRAPING DIT ")
st.write("👋 Salut ! Bienvenue dans l'interface de scraping de données.")

st.sidebar.title("MENU")
st.sidebar.markdown("[🏗️ Scraper les données avec SELENIUM](/1_scraping)")
st.sidebar.markdown("[📊 Visualiser les données](/2_visualisation)")
st.sidebar.markdown("[📝 Évaluation](/3_evaluation)")

st.write("🤓 Etudiant : Abdoulaye DRAME")
st.write("🎒 Niveau   : Master 1 IA, Groupe 1")
st.write("👨‍💻 Projet   : Projet 1, scraping de donné :  🌍 Expat-Dakar")
st.write("Veuillez utiliser les liens dans la barre latérale pour naviguer dans l'application.")
st.write("- Utilisez **Scraper les données** pour collecter des informations depuis les sites web.")
st.write("- Utilisez **Visualiser les données** pour consulter les données collectées.")
