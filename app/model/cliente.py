import random
from app.model.contenedor import Contenedor

class Cliente:
    def __init__(self, nombre=None):
        self.nombre = nombre if nombre else self.asignar_nombre()
        self.contenedores = [Contenedor(random.randint(1,3)), Contenedor(random.randint(1,3))]
        self.capacidad_dinero = random.randint(100000000,200000000)

    def asignar_nombre(self):
        nombres = [
            'BBVA', 'Éxito', 'Falabella', 'Bancolombia', 'D1'
        ]
        return random.choice(nombres)
    
    def eliminar_contenedor(self, contenedor):
        for i, c in enumerate(self.contenedores):
            if c.tipo == contenedor:
                self.contenedores.pop(i)
                break
