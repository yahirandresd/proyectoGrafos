from app.model.tipos_carro import Escolta, Pequeño, Grande, Ladron


class Carro:
    def __init__(self, tipo):
        self.tipo = tipo
        self.carro = None

        if self.tipo == 'grande':
            self.carro = Grande(3)
        elif self.tipo == 'pequeño':
            self.carro = Pequeño(2)
        elif self.tipo == 'escolta':
            self.carro = Escolta()
        elif self.tipo == 'ladron':  # Agregamos esta condición para Ladron
            self.carro = Ladron()
        else:
            raise ValueError(f"Tipo de carro desconocido: {tipo}")

    def get_carro(self):
        return self.carro

    def set_carro(self, carro):
        self.carro = carro
