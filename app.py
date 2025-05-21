from flask import Flask, request, jsonify
import jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta'

# Datos personales ficticios
user_data = {
    "123456789": {
        "nombre": "Juan Pérez",
        "correo": "juan@example.com",
        "ciudad": "Bucaramanga"
    }
}

@app.route('/info', methods=['GET'])
def get_info():
    auth = request.headers.get('Authorization')
    if not auth:
        return jsonify({"message": "Token requerido"}), 403
    
    try:
        token = auth.split()[1]
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        cedula = data['cedula']
        return jsonify(user_data.get(cedula, {}))
    except Exception as e:
        return jsonify({"message": "Token inválido o expirado"}), 403

if __name__ == '__main__':
    app.run()
