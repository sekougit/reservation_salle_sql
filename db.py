'''import pyodbc
#\\SQLEXPRESS;
def get_connection():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost"  # 🔁 change si besoin
        "DATABASE=GestionReservationsSalles;"
        "UID=DESKTOP-M4SD827"
        "PWD="
    )
    return conn

def authenticate_user(email, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT U.UserID, U.Nom + ' ' + U.Prenom AS NomComplet, R.NomRole
        FROM UTILISATEURS U
        JOIN ROLES R ON U.RoleID = R.RoleID
        WHERE U.Email = ? AND U.MotDePasse = ? AND U.Actif = 1
    """, (email, password))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"UserID": row[0], "Nom": row[1], "Role": row[2]}
    return None'''

import pyodbc
import pandas as pd

def get_connection():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost"  # ou juste localhost si pas d'instance nommée
        "DATABASE=GestionReservationsSalles;"
        "Trusted_Connection=yes;"        # authentification Windows intégrée
    )
    return conn

def authenticate_user(email, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT U.UserID, U.Nom + ' ' + U.Prenom AS NomComplet, R.NomRole
        FROM UTILISATEURS U
        JOIN ROLES R ON U.RoleID = R.RoleID
        WHERE U.Email = ? AND U.MotDePasse = ? AND U.Actif = 1
    """, (email, password))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"UserID": row[0], "Nom": row[1], "Role": row[2]}
    return None

'''# Fonction pour récupérer toute une table dans un DataFrame pandas
def lire_table_en_df(nom_table):
    conn = get_connection()
    query = f"SELECT * FROM {nom_table}"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Exemple d'utilisation
if __name__ == "__main__":
    df_reservations = lire_table_en_df("RESERVATIONS")
    print(df_reservations.head())'''

