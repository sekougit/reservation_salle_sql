import pyodbc

def get_connection():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost\\SQLEXPRESS;"  # 🔁 change si besoin
        "DATABASE=GestionReservationsSalles;"
        "UID=sa;"
        "PWD=motdepasse;"
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
