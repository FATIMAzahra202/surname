import streamlit as st  # Import Streamlit for creating web interfaces
import requests  # Import requests to make HTTP requests
import pandas as pd  # Import pandas for data manipulation
import matplotlib.pyplot as plt  # Import matplotlib for plotting graphs

def get_nationality(name):
    # Send a GET request to the nationalize.io API to predict the origins of a name
    try:
        response = requests.get(f"https://api.nationalize.io?name={name}")
        response.raise_for_status()  # Raises an exception for HTTP errors
        return response.json()  # Return the JSON response if successful
    except requests.RequestException as e:
        st.error(f"Failed to retrieve data: {e}")  # Display error in Streamlit interface
        return None

def display_nationality(data):
    # Display nationality data if available
    if data and 'country' in data:  # Check if the data contains 'country'
        results = []  # List to store results
        for country in data['country']:  # Iterate through each country in the response
            result = {
                "Pays": country['country_id'],  # Country ID
                "Probabilité (%)": f"{country['probability']*100:.2f}"  # Probability formatted to two decimal places
            }
            results.append(result)
        df = pd.DataFrame(results)  # Convert results list to DataFrame
        return df
    else:
        st.write("Aucune donnée trouvée pour ce nom de famille.")  # Display message if no data is found
        return pd.DataFrame()

st.title('Devinez l’origine des noms de famille')  # Page title

name_input = st.text_input('Entrez un nom de famille:', '')  # Text input for entering a name

if st.button('Devinez l’origine'):  # Button to trigger origin guess
    if name_input:  # Check if a name has been entered
        data = get_nationality(name_input)  # Fetch nationality data for the entered name
        result_df = display_nationality(data)  # Display nationality data
        if not result_df.empty:
            st.download_button(
                label="Télécharger les données",  # Download button text
                data=result_df.to_csv(index=False).encode('utf-8'),  # Prepare data as CSV for download
                file_name=f"{name_input}_origins.csv",  # Set the file name for the download
                mime='text/csv',  # MIME type for the file
            )

            # Create a bar chart of probabilities
            fig, ax = plt.subplots()
            ax.bar(result_df['Pays'], result_df['Probabilité (%)'].astype(float), color='skyblue')
            plt.xlabel('Pays')
            plt.ylabel('Probabilité (%)')
            plt.title('Probabilité que le nom soit originaire de')
            st.pyplot(fig)  # Display the plot in Streamlit

