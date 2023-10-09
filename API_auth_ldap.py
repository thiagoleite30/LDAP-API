from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from auth_ldap.auth_ldap import authenticate_ldap
from decouple import config

app = Flask(__name__)

# Configure CORS para permitir solicitações da origem do seu frontend
origens_dominios = config("ORIGINS")
cors = CORS(app, resources={r"/autenticar": {"origins": origens_dominios}})

print(f'\nDOMINIOS PERMITIDOS: {origens_dominios}')

@app.route("/autenticar", methods=["POST"])
@cross_origin(origin=origens_dominios)
def autenticar():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if authenticate_ldap(username, password):
        return jsonify({"message": "Autenticação bem-sucedida"}), 200
    else:
        return jsonify({"message": "Falha na autenticação"}), 401

if __name__ == "__main__":
    context = (config('CRT'), config('PRIVATE_KEY'))
    app.run(debug=False, port=443, ssl_context=context, host='0.0.0.0')
