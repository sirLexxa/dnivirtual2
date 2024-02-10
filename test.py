from flask import Flask, request, jsonify
import DNIVIRTUAL

app = Flask(__name__)

@app.route('/procesar_dni', methods=['GET'])
def procesar_dni():
    dni = request.args.get('dni')
    resultado = DNIVIRTUAL.dnivir(dni)
    
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="4000")
