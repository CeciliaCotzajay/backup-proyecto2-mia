from flask import Flask, jsonify, request
from flask_cors import CORS
from analizador import analizador
import singleton
import time

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Respuesta de ejemplo
respuesta = {
    'estado': 'OK',
    'mensaje': '[Success] => Disco creado correctamente',
}

# Ruta para obtener la lista de productos≠
@app.route('/', methods=['GET'])
def obtener_productos():
    return jsonify(respuesta)

@app.route('/execute', methods=['POST'])
def get_first_word():
    data = request.get_json()
    message0 = data.get('command', '')
    message = message0.lower()
    print(message)
    # Dividir el mensaje en palabras
    words = message.split()
    ocurrencia = words[0].count('#')
    an = analizador()
    if words:
        singleton.objL.respuesta['mensaje'] = ""
        singleton.objL.respuesta['mensaje']+= message + "\n"
        an.analizar(message)
        if(ocurrencia < 0):
            singleton.objL.respuesta['mensaje']+= f"[Success] => comando {words[0]} ejecutado exitosamente"+"\n"
    else:
        singleton.objL.respuesta['mensaje'] = ""
        singleton.objL.respuesta['mensaje']+= "No se encontraron palabras en el mensaje."
    # Esperamos 1 segundo, para simular proceso de ejecución
    #time.sleep(1)
    return jsonify(singleton.objL.respuesta)

if __name__ == '__main__':
    app.run(debug=True)