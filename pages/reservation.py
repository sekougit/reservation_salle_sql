import streamlit as st
import requests
from datetime import date, time

API_URL = "https://monapi.herokuapp.com/api"

def app(user):
    st.title("Réserver une salle")
    salles = requests.get(f"{API_URL}/salles").json()
    types_evenements = requests.get(f"{API_URL}/types_evenements").json()

    salle = st.selectbox("Salle", [s['NomSalle'] for s in salles])
    type_event = st.selectbox("Type d'événement", [t['NomType'] for t in types_evenements])
    date_resa = st.date_input("Date réservation", date.today())
    heure_debut = st.time_input("Heure début", time(9,0))
    heure_fin = st.time_input("Heure fin", time(10,0))
    objet = st.text_input("Objet réunion")
    nb_participants = st.number_input("Nombre participants", min_value=1, value=1)

    if st.button("Réserver"):
        data = {
            "UserID": user["UserID"],
            "SalleNom": salle,
            "TypeEventNom": type_event,
            "DateReservation": str(date_resa),
            "HeureDebut": heure_debut.strftime("%H:%M:%S"),
            "HeureFin": heure_fin.strftime("%H:%M:%S"),
            "ObjetReunion": objet,
            "NombreParticipants": nb_participants
        }
        res = requests.post(f"{API_URL}/reservations", json=data)
        if res.status_code == 201:
            st.success("Réservation créée !")
        else:
            st.error(f"Erreur : {res.text}")
