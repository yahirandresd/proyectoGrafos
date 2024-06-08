import random

class Centro_Operacion:
    def __init__(self, nombre=None):
        self.capacidad_dinero = 0
        self.capacidad_vehiculos = 0
        self.capacidad_escoltas = 0
        self.nombre = nombre if nombre else self.asignar_nombre_aleatorio()

    def get_dinero(self):
        return self.capacidad_dinero
    
    def set_dinero(self, capacidad):
        self.capacidad_dinero = capacidad

    def get_vehiculos(self):
        return self.capacidad_vehiculos
    
    def set_vehiculos(self, capacidad):
        self.capacidad_vehiculos = capacidad

    def get_escoltas(self):
        return self.capacidad_escoltas
    
    def set_escoltas(self, capacidad):
        self.capacidad_escoltas = capacidad

    def asignar_nombre_aleatorio(self):
        nombres = ["Centro A", "Centro B", "Centro C", "Centro D", "Centro E"]
        return random.choice(nombres)

