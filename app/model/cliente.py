import random

class Cliente:
    def __init__(self, nombre=None):
        self.nombre = nombre if nombre else self.asignar_nombre()
        self.dinero_recogido = random.randint(10000000, 100000000) #entre 10 y 100 millones

    def asignar_nombre(self):
        nombres = [
            'BBVA', 'Éxito', 'Falabella', 'Bancolombia', 'D1'
            ]
        return random.choice(nombres)
        
