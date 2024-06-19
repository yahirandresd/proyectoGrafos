class Contenedor:
    def __init__(self, tipo):
        if tipo == 1:
            self.tipo = 'pequeño'
            self.capacidad = 20
            self.peso = tipo
        elif tipo == 2:
            self.tipo = 'mediano'
            self.capacidad = 50
            self.peso = tipo
        elif tipo == 3:
            self.tipo = 'grande'
            self.capacidad = 100
            self.peso = tipo
