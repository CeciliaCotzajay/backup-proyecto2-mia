from flask import Flask, jsonify, request
from flask_cors import CORS
from analizador import analizador
from reportess3 import reportess3
import singleton
import time

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Respuesta de ejemplo
respuesta = {
    'estado': 'OK',
    'mensaje': '[Success] => Servidor backend ejecutandose exitosamente, flask',
}

# Ruta para obtener la lista de productos≠
@app.route('/', methods=['GET'])
def obtener_productos():
    return jsonify(respuesta)

@app.route('/cargaReportes', methods=['POST'])
def obtener_reportes():
    reps3 = reportess3()
    singleton.objL.respuesta['estado'] = "200"
    if(singleton.objL.list_pathsReports):
        singleton.objL.respuesta['estado'] = "205"
        singleton.objL.respuesta["report"] = {}
        for i1, i2 in zip(singleton.objL.list_pathsReports, singleton.objL.list_nameReports):
            singleton.objL.respuesta["report"][i2] = i1
        reps3.subir_Imagen()
    return jsonify(singleton.objL.respuesta)

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
        singleton.objL.respuesta['estado'] = "200"
        singleton.objL.respuesta['mensaje'] = ""
        singleton.objL.respuesta['mensaje']+= message + "\n"
        an.analizar(message)
        if(ocurrencia < 0):
            singleton.objL.respuesta['mensaje']+= f"[Success] => comando {words[0]} ejecutado exitosamente"+"\n"
    else:
        singleton.objL.respuesta['estado'] = "200"
        singleton.objL.respuesta['mensaje'] = ""
        singleton.objL.respuesta['mensaje']+= "No se encontraron palabras en el mensaje."
    # Esperamos 1 segundo, para simular proceso de ejecución
    #time.sleep(1)
    return jsonify(singleton.objL.respuesta)

@app.route('/resp', methods=['POST'])
def get_first_word2():
    data = request.get_json()
    message0 = data.get('command', '')
    message = message0.lower()
    print(message)
    # Dividir el mensaje en palabras
    words = message.split()
    an = analizador()
    if words:
        singleton.objL.respuesta['estado'] = "200"
        singleton.objL.respuesta['mensaje'] = ""
        singleton.objL.respuesta['mensaje']+= message + "\n"
        an.analizar(message)
    else:
        singleton.objL.respuesta['estado'] = "200"
        singleton.objL.respuesta['mensaje'] = ""
        singleton.objL.respuesta['mensaje']+= "No se encontraron palabras en el mensaje.\n"
    # Esperamos 1 segundo, para simular proceso de ejecución
    #time.sleep(1)
    return jsonify(singleton.objL.respuesta)


if __name__ == '__main__':
    app.run(debug=True)