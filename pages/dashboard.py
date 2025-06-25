import streamlit as st
import requests

API_URL = "http://localhost:5000/api"

def app(user):
    st.title("Dashboard")
    params = {}
    if user["Role"].lower() == "employé":
        params["user_id"] = user["UserID"]

    res = requests.get(f"{API_URL}/reservations", params=params)
    if res.status_code != 200:
        st.error("Erreur récupération réservations")
        return

    reservations = res.json()
    if not reservations:
        st.info("Aucune réservation trouvée")
        return

    for r in reservations:
        st.write(f"Salle: **{r['NomSalle']}**")
        st.write(f"Date: {r['DateReservation']} | {r['HeureDebut']} - {r['HeureFin']}")
        st.write(f"Objet: {r['ObjetReunion']}")
        st.write(f"Statut: {r['Statut']}")
        st.markdown("---")
