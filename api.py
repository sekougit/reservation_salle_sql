from flask import abort

@app.route('/api/reservations/<int:reservation_id>/annuler', methods=['POST'])
def annuler_reservation(reservation_id):
    data = request.json
    manager_id = data.get("ManagerID")

    # Vérifier que l'utilisateur est manager ou admin
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT R.NomRole
        FROM UTILISATEURS U
        JOIN ROLES R ON U.RoleID = R.RoleID
        WHERE U.UserID = ? AND U.Actif = 1
    """, manager_id)
    row = cursor.fetchone()
    if not row or row[0].lower() not in ['manager', 'admin']:
        conn.close()
        return jsonify({"error": "Accès refusé, rôle non autorisé"}), 403

    # Mettre à jour la réservation pour annuler si elle est en attente ou validée
    cursor.execute("""
        UPDATE RESERVATIONS
        SET Statut = 'Annulée',
            Commentaires = 'Annulée par manager/admin',
            DateValidation = GETDATE(),
            ValidePar = ?
        WHERE ReservationID = ? AND Statut IN ('En attente', 'Validée')
    """, manager_id, reservation_id)
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"error": "Réservation introuvable ou déjà annulée"}), 404

    # Log de l'action
    cursor.execute("""
        INSERT INTO LOGS_RESERVATIONS (ReservationID, UserID, Action, Details)
        VALUES (?, ?, 'Annulation', 'Réservation annulée par manager/admin')
    """, reservation_id, manager_id)

    conn.commit()
    conn.close()
    return jsonify({"message": "Réservation annulée avec succès"}), 200
