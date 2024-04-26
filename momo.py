import streamlit as st  # Importi streamlit bach tdir interface web
import requests  # Importi requests bach t'envoyi des requêtes HTTP
import pandas as pd  # Importi pandas bach tdir manipulation dial data b DataFrame
import matplotlib.pyplot as plt  # Importi matplotlib bach tdir des graphiques

def get_nationality(name):
    # T'sift requête GET l'API nationalize.io bach tjib lik les origines dial smiya li dkhlti
    response = requests.get(f"https://api.nationalize.io?name={name}")
    if response.status_code == 200:  # Ila kanat réponse réussie (code 200)
        return response.json()  # Rje3 JSON dial résultat
    else:
        return None  # Rje3 None ila kan chi problème m3a requête

def display_nationality(data):
    if data and 'country' in data:  # T'checki ila jatk data w fihom 'country'
        results = []  # Khlli tableau fih résultat
        for country in data['country']:  # Loopi 3la koll country f data
            result = {
                "Pays": country['country_id'],  # Sauvgardi id dial country
                "Probabilité (%)": f"{country['probability']*100:.2f}"  # Calculi probabilité w formattiha b %.2f
            }
            results.append(result)  # Zidi résultat f tableau
        df = pd.DataFrame(results)  # Converti résultats en DataFrame
        return df
    else:
        st.write("Aucune donnée trouvée pour ce nom de famille.")  # Affichi message ila ma jatch data
        return pd.DataFrame()

st.title('Devinez l’origine des noms de famille')  # Titre dial page

name_input = st.text_input('Entrez un nom de famille:', '')  # Khlli utilisateur ydakhel smiya

if st.button('Devinez l’origine'):  # Khlli bouton bach utilisateur yklikki 3lih
    if name_input:  # T'checki ila utilisateur dakhel chi smiya
        data = get_nationality(name_input)  # Sift smiya l function get_nationality
        result_df = display_nationality(data)  # Khddem function display_nationality b data li jat
        if not result_df.empty:
            st.download_button(
                label="Télécharger les données",  # Titre dial bouton
                data=result_df.to_csv(index=False).encode('utf-8'),  # Prépari data b format CSV bach ytelechargiha
                file_name=f"{name_input}_origins.csv",  # Smmi fichier
                mime='text/csv',  # Type dial fichier
            )

            # Créer un graphique à barres des probabilités
            fig, ax = plt.subplots()
            ax.bar(result_df['Pays'], result_df['Probabilité (%)'].astype(float), color='skyblue')
            plt.xlabel('Pays')
            plt.ylabel('Probabilité (%)')
            plt.title('Probabilité que le nom soit originaire de')
            st.pyplot(fig)  # Affichi le graphique dans Streamlit
