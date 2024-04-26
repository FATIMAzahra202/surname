import streamlit as st 
import requests
import pandas as pd   

def get_nationality(name):
    response = requests.get(f"https://api.nationalize.io?name={name}")
    if response.status_code == 200:
        return response.json()
    else:
        return None

def display_nationality(data):
    if data and 'country' in data:
        results = []
        countries = []  # List to store country names
        probabilities = []  # List to store probabilities
        for country in data['country']:
            countries.append(country['country_id'])  # Append country name
            probabilities.append(country['probability']*100)  # Append probability
            result = {
                "Pays": country['country_id'],
                "Probabilité (%)": f"{country['probability']*100:.2f}"
            }
            results.append(result)
        st.bar_chart(pd.DataFrame({'Pays': countries, 'Probabilité (%)': probabilities}), use_container_width=True, height=500)  # Display horizontal bar chart
        st.write("Probabilités par pays:")
        for country, probability in zip(countries, probabilities):
            st.write(f"{country}: {probability:.2f}%")
        return pd.DataFrame(results)
    else:
        st.write("Aucune donnée trouvée pour ce nom de famille.")
        return pd.DataFrame()

st.title('Devinez l’origine des noms de famille')

name_input = st.text_input('Entrez un nom de famille:', '')

if st.button('Devinez l’origine'):
    if name_input:
        data = get_nationality(name_input)
        result_df = display_nationality(data)
        st.download_button(
            label="Télécharger les données",
            data=result_df.to_csv(index=False).encode('utf-8'),
            file_name=f"{name_input}_origins.csv",
            mime='text/csv',
        )

