from tipos_carro import Escolta, Pequeño, Grande

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

carro = Carro('grande')
print(carro.carro.__dict__)
