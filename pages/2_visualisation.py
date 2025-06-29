import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(layout="wide")

st.title("📊 Dashboard de Visualisation des Données")
st.write("Cette page vous permet de consulter et d'analyser les données collectées.")

# Sidebar pour les filtres
st.sidebar.header("Filtres")

fichiers = ["tv-home-cinema.csv", "telephones.csv", "ordinateurs.csv"]
fichier = st.sidebar.selectbox("Choisissez un fichier :", fichiers)

try:

    df = pd.read_csv("donnee/"+fichier)


    if 'prix' in df.columns:

        if df['prix'].dtype == 'object':
            df['prix_num'] = pd.to_numeric(df['prix'].str.extract(r'(\d+(?:\s\d+)*)').iloc[:, 0].str.replace(' ', ''), errors='coerce')
            df['prix_num'] = df['prix_num'].fillna(0)
        else:
            df['prix_num'] = pd.to_numeric(df['prix'], errors='coerce').fillna(0)


    if 'prix_num' in df.columns:
        df['prix_num'] = pd.to_numeric(df['prix_num'], errors='coerce').fillna(0)

    # Affichage des données dans un tableau qui peut s'etendre
    with st.expander(f"📄 Données brutes de {fichier}", expanded=False):
        st.dataframe(df)

    # Dashboard principal
    st.subheader("Tableau de bord analytique")

    # Première ligne de visualisations
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Répartition par marque")
        if 'marque' in df.columns:
            # Remplacement Des valeurs N/A par "Non spécifié"
            df['marque'] = df['marque'].replace('N/A', 'Non spécifié')

            # comptage du nobre de produit de chaque marque
            nombre_par_marque = df['marque'].value_counts().reset_index()
            nombre_par_marque.columns = ['Marque', 'Nombre']

            # Création un graphique à barres
            fig = px.bar(nombre_par_marque, x='Marque', y='Nombre', 
                         color='Marque', 
                         title="Nombre de produits par marque")
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Distribution des prix")
        if 'prix_num' in df.columns:
            # Create a temporary numeric series for visualization to avoid any type issues
            prix_numerique = pd.to_numeric(df['prix_num'], errors='coerce').fillna(0)

            # creation d'un dataframem temporaiaren
            temp_df = pd.DataFrame({'prix_num': prix_numerique})

            # Création d'un histogramme des prix
            fig = px.histogram(temp_df, x='prix_num',
                              title="Distribution des prix",
                              labels={'prix_num': 'Prix (F CFA)'},
                              nbins=20)
            st.plotly_chart(fig, use_container_width=True)

    # Deuxième ligne de visualisations
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Répartition géographique")
        if 'adresse' in df.columns:
            # Extraire la ville de l'adresse
            df['ville'] = df['adresse'].str.split(',').str[1].str.strip()

            # Compter les occurrences de chaque ville
            location_counts = df['ville'].value_counts().reset_index()
            location_counts.columns = ['Ville', 'Nombre']

            # Créer un graphique circulaire
            fig = px.pie(location_counts, values='Nombre', names='Ville',
                         title="Répartition par ville")
            st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.subheader("Comparaison des prix par marque")
        if 'marque' in df.columns and 'prix_num' in df.columns:
            # Create a temporary dataframe with numeric prices for the box plot
            temp_df = df.copy()
            temp_df['prix_num'] = pd.to_numeric(temp_df['prix_num'], errors='coerce').fillna(0)

            # Créer un box plot des prix par marque
            fig = px.box(temp_df, x='marque', y='prix_num',
                        title="Comparaison des prix par marque",
                        labels={'prix_num': 'Prix (F CFA)', 'marque': 'Marque'})
            st.plotly_chart(fig, use_container_width=True)

    # Troisième ligne - Statistiques clés
    st.subheader("Statistiques clés")

    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

    with metric_col1:
        st.metric(label="Nombre total de produits", value=len(df))

    # Create a single numeric series for all statistics to ensure consistency
    prix_numerique = None
    if 'prix_num' in df.columns:
        prix_numerique = pd.to_numeric(df['prix_num'], errors='coerce').fillna(0)

    with metric_col2:
        if prix_numerique is not None:
            st.metric(label="Prix moyen", value=f"{int(prix_numerique.mean()):,} F CFA")

    with metric_col3:
        if prix_numerique is not None:
            st.metric(label="Prix minimum", value=f"{int(prix_numerique.min()):,} F CFA")

    with metric_col4:
        if prix_numerique is not None:
            st.metric(label="Prix maximum", value=f"{int(prix_numerique.max()):,} F CFA")

    # Tableau détaillé filtrable
    st.subheader("Tableau détaillé")

    try:
        # bornes en float
        min_prix = float(df['prix_num'].min())
        max_prix = float(df['prix_num'].max())
        prix_range = st.slider(
            "Gamme de prix:",
            min_value=min_prix,
            max_value=max_prix,
            value=(min_prix, max_prix),
            step=1.0
        )

        # application du filtre
        filt = pd.to_numeric(df['prix_num'], errors='coerce').fillna(0)
        filtered_df = df[(filt >= prix_range[0]) & (filt <= prix_range[1])]

        # Affichage du tableau filtré
        st.dataframe(filtered_df)

        # Bouton de téléchargement des données
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="⬇️ Télécharger les données",
            data=csv,
            file_name=f"{fichier.split('.')[0]}_filtered.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"Erreur dans le filtrage des prix : {e}")
        st.dataframe(df)

        # Bouton de téléchargement des données non filtrées en cas d'erreur
        csv = df.to_csv(index=False)
        st.download_button(
            label="⬇️ Télécharger les données complètes",
            data=csv,
            file_name=f"{fichier.split('.')[0]}_complet.csv",
            mime="text/csv"
        )

except FileNotFoundError:
    st.warning("⚠️ Fichier introuvable. Lancez d'abord le scraping.")
except Exception as e:
    st.error(f"Une erreur s'est produite lors du chargement ou de l'analyse des données: {e}")
