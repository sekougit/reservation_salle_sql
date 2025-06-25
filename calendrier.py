import streamlit as st
import pandas as pd
from db import get_connection

def afficher_calendrier():
    st.subheader("📅 Calendrier des réservations validées")
    conn = get_connection()
    df = pd.read_sql("""
        SELECT r.DateReservation, r.HeureDebut, r.HeureFin,
               s.NomSalle, u.Nom + ' ' + u.Prenom AS Utilisateur,
               r.ObjetReunion
        FROM RESERVATIONS r
        JOIN SALLES s ON r.SalleID = s.SalleID
        JOIN UTILISATEURS u ON r.UserID = u.UserID
        WHERE r.Statut = 'Validée'
        ORDER BY r.DateReservation, r.HeureDebut
    """, conn)
    st.dataframe(df)
    conn.close()
