import streamlit as st
from helpers import reserver_salle, annuler_reservation, afficher_reservations
from calendrier import afficher_calendrier

def show_dashboard():
    st.sidebar.title("📁 Menu")
    page = st.sidebar.selectbox("Navigation", [
        "Liste des réservations",
        "Réserver une salle",
        "Annuler une réservation",
        "Calendrier"
    ])

    role = st.session_state.role

    if role == "Admin":
        page_admin = st.sidebar.selectbox("Admin", [
            "Gérer les utilisateurs",
            "Gérer les salles"
        ])
        if page_admin == "Gérer les utilisateurs":
            st.subheader("🔧 Gestion des utilisateurs (à développer)")
        elif page_admin == "Gérer les salles":
            st.subheader("🏢 Gestion des salles (à développer)")

    st.sidebar.markdown(f"👤 Connecté : **{st.session_state.user_name}** ({st.session_state.role})")
    if st.sidebar.button("🔓 Déconnexion"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()

    st.title("🗂️ Tableau de bord des Réservations")

    if page == "Liste des réservations":
        afficher_reservations()
    elif page == "Réserver une salle":
        reserver_salle()
    elif page == "Annuler une réservation":
        annuler_reservation()
    elif page == "Calendrier":
        afficher_calendrier()
