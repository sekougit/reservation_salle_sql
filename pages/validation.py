import streamlit as st
import requests

API_URL = "https://monapi.herokuapp.com/api"

def app(user):
    st.title("Validation des réservations")
    res = requests.get(f"{API_URL}/reservations", params={"statut": "En attente"})
    if res.status_code != 200:
        st.error("Erreur récupération réservations")
        return

    reservations = res.json()
    if not reservations:
        st.info("Aucune réservation en attente.")
        return

    for r in reservations:
        st.write(f"Salle: {r['NomSalle']}")
        st.write(f"Date: {r['DateReservation']} {r['HeureDebut']} - {r['HeureFin']}")
        st.write(f"Objet: {r['ObjetReunion']}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"Valider {r['ReservationID']}"):
                r2 = requests.post(f"{API_URL}/reservations/{r['ReservationID']}/valider", json={"ManagerID": user["UserID"]})
                if r2.status_code == 200:
                    st.success("Réservation validée")
                    st.experimental_rerun()
                else:
                    st.error("Erreur validation")
        with col2:
            if st.button(f"Annuler {r['ReservationID']}"):
                r2 = requests.post(f"{API_URL}/reservations/{r['ReservationID']}/annuler", json={"ManagerID": user["UserID"]})
                if r2.status_code == 200:
                    st.success("Réservation annulée")
                    st.experimental_rerun()
                else:
                    st.error("Erreur annulation")

        st.markdown("---")
