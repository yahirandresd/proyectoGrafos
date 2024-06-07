class Grande:
    def __init__(self, contenedor):
        self.velocidad = 0
        if contenedor == 3:
            self.capacidad = 100000000
        elif contenedor == 2:
            self.capacidad = 50000000
        else:
            self.capacidad = 20000000
        self.escoltas = 2
        self.escudo = 20
        self.ataque = 15

class Pequeño:
    def __init__(self, contenedor):
        self.velocidad = 1
        if contenedor == 3:
            self.capacidad = 100000000
        elif contenedor == 2:
            self.capacidad = 50000000
        else:
            self.capacidad = 20000000
        self.escoltas = 1
        self.escudo = 5
        self.ataque = 10

class Escolta:
    def __init__(self, velocidad):
        self.escudo = 5
        self.ataque = 5
        self.velocidad = velocidad

class Ladron:
    def __init__(self):
        self.escudo = 0
        self.ataque = 0

    def get_escudo(self):
        return self.escudo
    
    def set_escudo(self, escudo):
        self.escudo = escudo

    def get_ataque(self):
        return self.ataque
    
    def set_ataque(self, ataque):
        self.ataque = ataque
