import pyodbc

def get_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=GestionReservationsSalles;"
        "Trusted_Connection=yes;"
    )

# Ajoute ici des fonctions réutilisables si besoin (ex: fetch_salles(), fetch_types_evenements())
