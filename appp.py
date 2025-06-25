import streamlit as st
import requests

API_URL = "http://localhost:5000/api"

def login():
    st.title("Connexion")
    email = st.text_input("Email")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        res = requests.post(f"{API_URL}/login", json={"email": email, "password": password})
        if res.status_code == 200:
            st.session_state["user"] = res.json()
            st.experimental_rerun()
        else:
            st.error("Email ou mot de passe incorrect")

def logout():
    st.session_state.pop("user", None)
    st.experimental_rerun()

def main():
    if "user" not in st.session_state:
        login()
    else:
        user = st.session_state["user"]
        st.sidebar.write(f"Connecté : {user['Nom']} ({user['Role']})")
        if st.sidebar.button("Déconnexion"):
            logout()

        role = user["Role"].lower()
        pages = {
            "employé": ["Dashboard", "Rechercher Salle", "Réserver Salle", "Calendrier"],
            "manager": ["Dashboard", "Rechercher Salle", "Réserver Salle", "Validation", "Calendrier"],
            "admin": ["Dashboard", "Rechercher Salle", "Réserver Salle", "Validation", "Calendrier"]
        }
        choix = st.sidebar.selectbox("Navigation", pages.get(role, ["Dashboard"]))

        if choix == "Dashboard":
            import pages.dashboard as dash
            dash.app(user)
        elif choix == "Rechercher Salle":
            import pages.recherche_salle as rs
            rs.app()
        elif choix == "Réserver Salle":
            import pages.reservation as res
            res.app(user)
        elif choix == "Validation" and role in ["manager", "admin"]:
            import pages.validation as val
            val.app(user)
        elif choix == "Calendrier":
            import pages.calendrier as cal
            cal.app(user)

if __name__ == "__main__":
    main()
