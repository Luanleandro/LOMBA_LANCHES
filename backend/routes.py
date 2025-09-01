from flask import Flask, request, jsonify
from models import get_db_connection

app = Flask(__name__)

# Criar usuário
@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, email, password) VALUES (%s, %s, %s) RETURNING id;",
        (data["name"], data["email"], data["password"])
    )
    user_id = cursor.fetchone()["id"]
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"id": user_id, "message": "User created successfully"}), 201

# Listar usuários
@app.route("/users", methods=["GET"])
def list_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email FROM users;")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users)

# Atualizar usuário
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET name=%s, email=%s, password=%s WHERE id=%s",
        (data["name"], data["email"], data["password"], user_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "User updated successfully"})

# Deletar usuário
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "User deleted successfully"})
