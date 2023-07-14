from flask import Flask, request, jsonify
from datetime import datetime

class Operacion:
    def __init__(self, numero_destino, valor):
        self.numero_destino = numero_destino
        self.fecha = datetime.now()
        self.valor = valor

class Cuenta:
    def __init__(self, numero, nombre, saldo, contactos):
        self.numero = numero
        self.nombre = nombre
        self.saldo = saldo
        self.contactos = contactos
        self.historial = []

    def pagar(self, destino, valor):
        if self.saldo >= valor and destino in self.contactos:
            self.saldo -= valor
            self.historial.append(Operacion(destino, -valor))
            return True
        return False

app = Flask(__name__)

BD = {
    "21345": Cuenta("21345", "Arnaldo", 200, ["123", "456"]),
    "123": Cuenta("123", "Luisa", 400, ["456"]),
    "456": Cuenta("456", "Andrea", 300, ["21345"]),
}


@app.route('/billetera/contactos')
def contactos():
    minumero = request.args.get('minumero')
    cuenta = BD.get(minumero)
    if cuenta:
        return jsonify({contacto: BD[contacto].nombre for contacto in cuenta.contactos})
    return jsonify({'error': 'Cuenta no encontrada'}), 404


@app.route('/billetera/pagar', methods=['GET', 'POST'])
def pagar():
    minumero = request.args.get('minumero')
    numerodestino = request.args.get('numerodestino')
    valor = int(request.args.get('valor'))
    cuenta = BD.get(minumero)
    if cuenta:
        if numerodestino not in cuenta.contactos:
            return jsonify({'error': 'El contacto no existe'}), 400
        if cuenta.pagar(numerodestino, valor):
            destino = BD.get(numerodestino)
            if destino:
                destino.saldo += valor
                destino.historial.append(Operacion(minumero, valor))
            return jsonify({'message': 'Realizado en {}.'.format(datetime.now().strftime('%d/%m/%Y'))})
        else:
            return jsonify({'error': 'Saldo insuficiente'}), 400
    return jsonify({'error': 'Cuenta no encontrada'}), 404


@app.route('/billetera/historial')
def historial():
    minumero = request.args.get('minumero')
    cuenta = BD.get(minumero)
    if cuenta:
        saldo = cuenta.saldo
        operaciones = [{'fecha': op.fecha.strftime('%d/%m/%Y'), 
                        'numero_destino': op.numero_destino, 
                        'valor': op.valor} for op in cuenta.historial]
        return jsonify({'Saldo de {}'.format(cuenta.nombre): saldo, 
                        'Operaciones de {}'.format(cuenta.nombre): operaciones})
    return jsonify({'error': 'Cuenta no encontrada'}), 404


if __name__ == '__main__':
    app.run(debug=True)
