class Contenedor:
    def __init__(self, tipo):
        if tipo == 1:
            self.tipo = 'pequeño'
            self.capacidad = 20
        elif tipo == 2:
            self.tipo = 'mediano'
            self.capacidad = 50
        elif tipo == 3:
            self.tipo = 'grande'
            self.capacidad = 100