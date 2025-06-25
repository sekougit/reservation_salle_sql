import streamlit as st
import requests
from datetime import date

API_URL = "https://monapi.herokuapp.com/api"

def app(user):
    st.title("Calendrier des réservations")

    date_sel = st.date_input("Choisir une date", value=date.today())
    res = requests.get(f"{API_URL}/reservations", params={"date": str(date_sel), "statut": "Validée"})
    if res.status_code != 200:
        st.error("Erreur récupération réservations")
        return

    reservations = res.json()
    if not reservations:
        st.info("Aucune réservation ce jour.")
        return

    for r in reservations:
        st.write(f"{r['HeureDebut']} - {r['HeureFin']} | {r['NomSalle']} | {r['ObjetReunion']}")
