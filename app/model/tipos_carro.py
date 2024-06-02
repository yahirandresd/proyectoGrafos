class Grande:
    def __init__(self, contenedor):
        self.velocidad = 0
        self.capacidad = contenedor
        self.escoltas = 2
        self.escudo = 20
        self.ataque = 15

class Pequeño:
    def __init__(self, contenedor):
        self.velocidad = 1
        self.capacidad = contenedor
        self.escoltas = 1
        self.escudo = 5
        self.ataque = 10

class Escolta:
    def __init__(self):
        self.escudo = 5
        self.ataque = 5
