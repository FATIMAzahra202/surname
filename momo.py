import streamlit as st
import requests

def get_nationality(name):
    response = requests.get(f"https://api.nationalize.io?name={name}")
    if response.status_code == 200:
        return response.json()
    else:
        return None

def display_nationality(data):
    if data and 'country' in data:
        for country in data['country']:
            st.write(f"Probabilité : {country['probability']*100:.2f}% que le nom soit originaire de {country['country_id']}")
    else:
        st.write("Aucune donnée trouvée pour ce nom de famille.")

st.title('Devinez l’origine des noms de famille')

name_input = st.text_input('Entrez un nom de famille:', '')

if name_input:
    data = get_nationality(name_input)
    display_nationality(data)
