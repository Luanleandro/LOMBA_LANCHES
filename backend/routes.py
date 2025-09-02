# from flask import Flask, request, jsonify
# from models import get_db_connection

# app = Flask(__name__)

# # Criar usuário
# @app.route("/users", methods=["POST"])
# def create_user():
#     data = request.json
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute(
#         "INSERT INTO users (name, email, password) VALUES (%s, %s, %s) RETURNING id;",
#         (data["name"], data["email"], data["password"])
#     )
#     user_id = cursor.fetchone()["id"]
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return jsonify({"id": user_id, "message": "User created successfully"}), 201

# # Listar usuários
# @app.route("/users", methods=["GET"])
# def list_users():
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT id, name, email FROM users;")
#     users = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     return jsonify(users)

# # Atualizar usuário
# @app.route("/users/<int:user_id>", methods=["PUT"])
# def update_user(user_id):
#     data = request.json
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute(
#         "UPDATE users SET name=%s, email=%s, password=%s WHERE id=%s",
#         (data["name"], data["email"], data["password"], user_id)
#     )
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return jsonify({"message": "User updated successfully"})

# # Deletar usuário
# @app.route("/users/<int:user_id>", methods=["DELETE"])
# def delete_user(user_id):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return jsonify({"message": "User deleted successfully"})

# import random
# import string
# from datetime import datetime, timedelta
# from flask import Flask, request, jsonify
# from models import get_db_connection

# app = Flask(__name__)

# # Função para gerar um código de 6 dígitos
# def generate_login_code():
#     return ''.join(random.choices(string.digits, k=6))

# # Rota para login ou registro por e-mail (login sem senha)
# @app.route("/login_or_register", methods=["POST"])
# def login_or_register():
#     data = request.json
#     email = data.get("email")
#     name = data.get("name") # O nome agora é opcional, então vamos pegá-lo se existir

#     if not email:
#         return jsonify({"message": "Email is required"}), 400

#     conn = get_db_connection()
#     cursor = conn.cursor()

#     try:
#         # 1. Verificar se o e-mail já existe
#         cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
#         existing_user = cursor.fetchone()

#         login_code = generate_login_code()
#         expires_at = datetime.utcnow() + timedelta(minutes=5)

#         if existing_user:
#             # Se o usuário existe, apenas atualiza o código de login
#             user_id = existing_user["id"]
#             cursor.execute(
#                 "UPDATE users SET login_code = %s, code_expires_at = %s WHERE id = %s",
#                 (login_code, expires_at, user_id)
#             )
#             message = "Login code sent to existing user"
#         else:
#             # 2. Se o usuário não existe, cria um novo registro
#             # O campo 'name' será inserido apenas se ele existir nos dados da requisição
#             if name:
#                 cursor.execute(
#                     "INSERT INTO users (email, name, login_code, code_expires_at) VALUES (%s, %s, %s, %s) RETURNING id;",
#                     (email, name, login_code, expires_at)
#                 )
#             else:
#                 cursor.execute(
#                     "INSERT INTO users (email, login_code, code_expires_at) VALUES (%s, %s, %s) RETURNING id;",
#                     (email, login_code, expires_at)
#                 )
#             user_id = cursor.fetchone()["id"]
#             message = "New user created. Login code sent."
        
#         conn.commit()

#         # Simular o envio do e-mail
#         print(f"ENVIAR E-MAIL PARA {email} com o código de login: {login_code}")
        
#         return jsonify({
#             "message": message,
#             "user_id": user_id
#         }), 200

#     except Exception as e:
#         conn.rollback()
#         return jsonify({"message": "An error occurred", "error": str(e)}), 500
    
#     finally:
#         cursor.close()
#         conn.close()

# # Rota para verificar o código e autenticar o usuário
# @app.route("/verify_code", methods=["POST"])
# def verify_code():
#     data = request.json
#     email = data.get("email")
#     code = data.get("code")

#     if not email or not code:
#         return jsonify({"message": "Email and code are required"}), 400

#     conn = get_db_connection()
#     cursor = conn.cursor()

#     try:
#         cursor.execute("SELECT id, login_code, code_expires_at FROM users WHERE email = %s", (email,))
#         user = cursor.fetchone()

#         if not user:
#             return jsonify({"message": "User not found"}), 404

#         if user["login_code"] == code and user["code_expires_at"] > datetime.utcnow():
#             return jsonify({"message": "Login successful!"}), 200
#         else:
#             return jsonify({"message": "Invalid or expired code"}), 401

#     except Exception as e:
#         return jsonify({"message": "An error occurred", "error": str(e)}), 500
    
#     finally:
#         cursor.close()
#         conn.close()

# # As outras rotas (list, update, delete) foram removidas para simplificar o fluxo
# # conforme o novo modelo de autenticação. Se você precisar delas, pode
# # readicioná-las ajustando para a ausência da senha.

from flask import Flask, request, jsonify
from models import get_db_connection

app = Flask(__name__)

# Rota para criar um novo usuário
@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    name = data.get("name")
    email = data.get("email")

    if not email:
        return jsonify({"message": "Email is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id;",
            (name, email)
        )
        user_id = cursor.fetchone()["id"]
        conn.commit()
        return jsonify({"id": user_id, "message": "User created successfully"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"message": "An error occurred", "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Rota para listar todos os usuários
@app.route("/users", methods=["GET"])
def list_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, name, email FROM users;")
        users = cursor.fetchall()
        return jsonify(users)
    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Rota para obter um usuário específico
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, name, email FROM users WHERE id = %s;", (user_id,))
        user = cursor.fetchone()
        if user:
            return jsonify(user)
        return jsonify({"message": "User not found"}), 404
    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Rota para atualizar um usuário
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json
    name = data.get("name")
    email = data.get("email")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE users SET name=%s, email=%s WHERE id=%s;",
            (name, email, user_id)
        )
        conn.commit()
        return jsonify({"message": "User updated successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"message": "An error occurred", "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Rota para deletar um usuário
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM users WHERE id=%s;", (user_id,))
        conn.commit()
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"message": "An error occurred", "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()