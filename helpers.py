import streamlit as st
import pandas as pd
from db import get_connection

def reserver_salle():
    conn = get_connection()
    salles = pd.read_sql("SELECT SalleID, NomSalle FROM SALLES WHERE Active = 1", conn)
    types = pd.read_sql("SELECT TypeEventID, NomType FROM TYPES_EVENEMENTS", conn)

    with st.form("form_reservation"):
        objet = st.text_input("Objet de la réunion")
        salle_nom = st.selectbox("Salle", salles["NomSalle"])
        type_lib = st.selectbox("Type d’événement", types["NomType"])
        date = st.date_input("Date")
        h_debut = st.time_input("Heure de début")
        h_fin = st.time_input("Heure de fin")
        nb_participants = st.number_input("Nombre de participants", min_value=1, step=1)
        submitted = st.form_submit_button("Réserver")

        if submitted:
            salle_id = salles[salles["NomSalle"] == salle_nom]["SalleID"].values[0]
            type_id = types[types["NomType"] == type_lib]["TypeEventID"].values[0]
            user_id = st.session_state.user_id

            cursor = conn.cursor()
            try:
                res_id = 0
                cursor.execute("EXEC sp_ReserverSalle ?, ?, ?, ?, ?, ?, ?, ?, ? OUTPUT",
                               user_id, salle_id, type_id, date, h_debut, h_fin, objet, nb_participants, res_id)
                conn.commit()
                st.success("Réservation enregistrée avec succès.")
            except Exception as e:
                st.error(f"Erreur : {e}")
            finally:
                cursor.close()
                conn.close()

def annuler_reservation():
    conn = get_connection()
    df = pd.read_sql("""
        SELECT ReservationID, ObjetReunion FROM RESERVATIONS
        WHERE Statut = 'En attente' AND UserID = ?
    """, conn, params=[st.session_state.user_id])

    if df.empty:
        st.info("Aucune réservation à annuler.")
        return

    choix = st.selectbox("Choisir la réservation à annuler", df["ObjetReunion"])
    if st.button("Annuler"):
        res_id = df[df["ObjetReunion"] == choix]["ReservationID"].values[0]
        cursor = conn.cursor()
        try:
            cursor.execute("EXEC sp_AnnulerReservation ?, ?", st.session_state.user_id, res_id)
            conn.commit()
            st.success("Réservation annulée.")
        except Exception as e:
            st.error(f"Erreur : {e}")
        finally:
            cursor.close()
            conn.close()

def afficher_reservations():
    conn = get_connection()
    df = pd.read_sql("""
        SELECT r.ReservationID, r.ObjetReunion, r.DateReservation, r.HeureDebut, r.HeureFin,
               s.NomSalle, t.NomType, u.Nom + ' ' + u.Prenom AS Utilisateur, r.Statut
        FROM RESERVATIONS r
        JOIN UTILISATEURS u ON r.UserID = u.UserID
        JOIN SALLES s ON r.SalleID = s.SalleID
        JOIN TYPES_EVENEMENTS t ON r.TypeEventID = t.TypeEventID
        ORDER BY r.DateReservation DESC
    """, conn)
    st.dataframe(df)
    conn.close()
