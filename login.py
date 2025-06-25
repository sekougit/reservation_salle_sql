import streamlit as st
from db import authenticate_user

def login_page():
    st.title("🔐 Connexion")

    email = st.text_input("Email")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        user = authenticate_user(email, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.user_id = user["UserID"]
            st.session_state.user_name = user["Nom"]
            st.session_state.role = user["Role"]
            st.success(f"Bienvenue {user['Nom']} ({user['Role']})")
            st.experimental_rerun()
        else:
            st.error("Identifiants incorrects.")
