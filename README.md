
# Cambios requeridos
El proyecto de billetera digital implementado actualmente permite a los usuarios realizar transacciones, consultar contactos y ver el historial de transacciones. Sin embargo, se ha propuesto una nueva característica que limita el monto total de las transferencias a un máximo de 200 soles por día.

Existen dos posibles enfoques para implementar esta característica:

## Enfoque 1: Usar el historial de operaciones para rastrear las transferencias diarias

Este enfoque implicaría recorrer el historial de transacciones de la cuenta cada vez que se realiza una transferencia. Se calcularía la suma de todas las transferencias que tienen la misma fecha que la transferencia actual. Si la suma, incluyendo la transferencia actual, supera los 200 soles, la transferencia se rechazaría.

La clase Operacion debería incluir la fecha y hora de la transacción.
La clase Cuenta requeriría un nuevo método para calcular la suma de las transferencias para una fecha dada.
El método pagar en la clase Cuenta necesitaría ser modificado para usar este nuevo método y rechazar las transferencias que superen el límite.

## Enfoque 2: Usar un campo adicional en la clase Cuenta para rastrear las transferencias diarias

Este enfoque implica la adición de un nuevo campo a la clase Cuenta que rastrearía la suma de las transferencias realizadas en el día actual. Cuando se realiza una transferencia, se suma el valor de la transferencia a este campo. Si el valor del campo, incluyendo la transferencia actual, supera los 200 soles, la transferencia se rechazaría.

# Nuevos casos de prueba
Independientemente del enfoque, deberían agregarse casos de prueba para asegurar que el límite de transferencia diario se implemente correctamente. Estos podrían incluir:

Realizar transferencias que sumen menos de 200 soles en un día. Estas transferencias deben ser exitosas.
Realizar una transferencia que haga que el total de las transferencias del día supere los 200 soles. Esta transferencia debe ser rechazada. Aquí pueden intervenir nuevas variables como la zona horaria del usuario, ya que el "reset" del límite podria ser más cómodo en horarios específicos para ciertos usuarios. 


# Riesgo de "romper" la funcionalidad existente
Implementar esta nueva característica implica un riesgo moderado. Las modificaciones a la clase Cuenta y a sus métodos, en particular el método pagar, podrían introducir bugs que afecten a la capacidad de los usuarios para realizar transferencias. Por ejemplo, se debe manejar errores referentes a la límite recientemente implementado, si estos tienen un retraso al actualizarce, el usuario podría hacer varias transferencias antes que el límite que tiene que haga vigente en su cuenta. Así como estos errores, pueden surgir más, principalmente relacionados con el manejo del historial de pagos del día.




