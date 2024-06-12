class Grande:
    def __init__(self, contenedor):
        self.velocidad = 1
        self.peso = contenedor

        if self.peso == 1:
            self.capacidad = 20000000
        if self.peso == 2:
            self.capacidad = 50000000
        if self.peso == 3:
            self.capacidad = 100000000

        self.escoltas = 2
        self.escudo = 20
        self.ataque = 15

    def actualizar_posicion(self, nueva_posicion):
        self.posicion_actual = nueva_posicion


class Pequeño:
    def __init__(self, contenedor):
        self.velocidad = 2
        self.peso = contenedor

        if self.peso == 1:
            self.capacidad = 20000000
        if self.peso == 2:
            self.capacidad = 50000000
        if self.peso == 3:
            self.capacidad = 100000000

        self.escoltas = 1
        self.escudo = 5
        self.ataque = 10

    def actualizar_posicion(self, nueva_posicion):
        self.posicion_actual = nueva_posicion


class Escolta:
    def __init__(self):
        self.escudo = 5
        self.ataque = 5

    def actualizar_posicion(self, nueva_posicion):
        self.posicion_actual = nueva_posicion


class Ladron:
    def __init__(self):
        self.escudo = 0
        self.ataque = 0

    def actualizar_posicion(self, nueva_posicion):
        self.posicion_actual = nueva_posicion

    def get_escudo(self):
        return self.escudo

    def set_escudo(self, escudo):
        self.escudo = escudo

    def get_ataque(self):
        return self.ataque

    def set_ataque(self, ataque):
        self.ataque = ataque
