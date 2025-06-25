import streamlit as st
import requests

API_URL = "https://monapi.herokuapp.com/api"

def app():
    st.title("Recherche de salle")
    capacite = st.number_input("Capacité minimum", min_value=1, value=1)
    date = st.date_input("Date de réservation")
    heure_debut = st.time_input("Heure début")
    heure_fin = st.time_input("Heure fin")

    if st.button("Rechercher"):
        params = {
            "capacite": capacite,
            "date": str(date),
            "heure_debut": heure_debut.strftime("%H:%M:%S"),
            "heure_fin": heure_fin.strftime("%H:%M:%S")
        }
        res = requests.get(f"{API_URL}/salles/disponibles", params=params)
        if res.status_code == 200:
            salles = res.json()
            if salles:
                for s in salles:
                    st.write(f"**{s['NomSalle']}** - Capacité: {s['Capacite']}")
                    st.write(f"Equipements: {s['Equipements']}")
                    st.markdown("---")
            else:
                st.info("Aucune salle disponible")
        else:
            st.error("Erreur lors de la recherche")
