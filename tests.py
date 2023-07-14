import unittest
from app import app, BD

class TestApp(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        
    # CASOS EXITOSOS:

    # Prueba si se pueden obtener correctamente los contactos de un número específico
    def test_obtener_contactos(self):
        response = self.app.get('/billetera/contactos?minumero=21345')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'123': 'Luisa', '456': 'Andrea'})

    # Prueba si se puede obtener correctamente el historial de transacciones de un número específico
    def test_obtener_historial(self):
        response = self.app.get('/billetera/historial?minumero=21345')
        self.assertEqual(response.status_code, 200)

    # Prueba si se puede realizar correctamente un pago desde un contacto a otro
    def test_pago_exitoso_otro_contacto(self):
        response = self.app.post('/billetera/pagar?minumero=123&numerodestino=456&valor=50')
        self.assertEqual(response.status_code, 200)

    # Prueba si se puede realizar un pago desde un número específico a un contacto
    def test_pago_exitoso(self):
        response = self.app.post('/billetera/pagar?minumero=21345&numerodestino=123&valor=50')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Realizado", response.get_json()['message'])


    # CASOS FALLIDOS

    # Prueba si el sistema maneja cuando se intenta realizar un pago pero no hay saldo en la cuenta
    def test_pago_saldo_insuficiente(self):
        response = self.app.post('/billetera/pagar?minumero=21345&numerodestino=123&valor=500')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Saldo insuficiente", response.get_json()["error"])

    # Prueba si el sistema maneja correctamente la situación en la que se intenta realizar un pago a un contacto que no existe
    def test_pago_no_contacto(self):
        response = self.app.post('/billetera/pagar?minumero=21345&numerodestino=789&valor=100')
        self.assertEqual(response.status_code, 400)
        self.assertIn("El contacto no existe", response.get_json()["error"])

    # Prueba si el sistema maneja cuando se intenta obtener los contactos de un número que no existe
    def test_obtener_contactos_no_existentes(self):
        response = self.app.get('/billetera/contactos?minumero=789')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
