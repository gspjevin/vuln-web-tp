from flask import Flask, request
import sqlite3
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return "heelo tout le monde"

#injection SQL détectée par CodeQL
@app.route('/user')
def get_user():
    username = request.args.get('username', '')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    #concaténation directe au lieu d'utiliser des paramètres
    query = f"SELECT * FROM users WHERE username = '{username}'"
    try:
        cursor.execute(query)
        return f"Recherche de l'utilisateur {username} effectuée."
    except Exception as e:
        return "Erreur dans la base de données."

#faille 2 exécution de commande
@app.route('/ping')
def ping():
    ip = request.args.get('ip', '127.0.0.1')
    # Mauvaise pratique : passage direct d'une entrée utilisateur au système
    os.system(f"ping -c 1 {ip}")
    return f"Commande de ping lancée vers {ip}"

if __name__ == '__main__':
    app.run(debug=True)
