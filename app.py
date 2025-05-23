from flask import Flask, request, jsonify
import jwt
import logging
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 
app.config['SECRET_KEY'] = 'apilab'

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Datos personales ficticios
user_data = {
    "1": {
        "nombre": "Pablo Pérez",
        "correo": "pablo@example.com",
        "ciudad": "Bucaramanga"
    },
    "2": {
        "nombre": "Luisa Amaya",
        "correo": "lmaya@example.com",
        "ciudad": "Bucaramanga"
    },
    "3": {
        "nombre": "aaaa Pérez",
        "correo": "juan@example.com",
        "ciudad": "Bucaramanga"
    },
    "4": {
        "nombre": "Juan Pérez",
        "correo": "juan@example.com",
        "ciudad": "Bucaramanga"
    }
}

@app.route('/info', methods=['GET'])
def get_info():
    logging.info("➡️ Inicio de la ruta /info")

    auth_header = request.headers.get('Authorization')
    if not auth_header:
        logging.warning("🔐 Token no proporcionado")
        logging.info("⬅️ Fin de la ruta /info")
        return jsonify({"message": "Token requerido"}), 403

    try:
        token = auth_header.split()[1]
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        cedula = data.get('cedula')

        logging.info(f"👤 Cédula decodificada: {cedula}")
        user_info = user_data.get(cedula)

        if user_info:
            logging.info("✅ Datos encontrados")
            logging.info("⬅️ Fin de la ruta /info")
            return jsonify(user_info)
        else:
            logging.warning("❌ No se encontró información para la cédula")
            logging.info("⬅️ Fin de la ruta /info")
            return jsonify({"message": "Usuario no encontrado"}), 404

    except jwt.ExpiredSignatureError:
        logging.error("❌ Token expirado")
        logging.info("⬅️ Fin de la ruta /info")
        return jsonify({"message": "Token expirado"}), 403
    except jwt.InvalidTokenError:
        logging.error("❌ Token inválido")
        logging.info("⬅️ Fin de la ruta /info")
        return jsonify({"message": "Token inválido"}), 403
    except Exception as e:
        logging.error(f"❌ Error inesperado: {str(e)}")
        logging.info("⬅️ Fin de la ruta /info")
        return jsonify({"message": "Error al procesar el token"}), 500

if __name__ == '__main__':
    app.run()
