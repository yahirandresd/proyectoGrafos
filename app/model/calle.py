import networkx as nx
import matplotlib.pyplot as plt
from app.model.carro import Carro
from app.model.centro_operacion import Centro_Operacion
import random

class Calle:
    def __init__(self) -> None:
        self.calle = nx.Graph()
        self.centros = []
        self.crear_calle()

    def crear_calle(self):
        for i in range(16):
            self.crear_centro()

        self.calle.add_node(self.centros[0].nombre)
        self.calle.add_node(self.centros[1].nombre)
        self.calle.add_edge(self.centros[0].nombre, self.centros[1].nombre)

        nx.draw(self.calle, with_labels=True)
        plt.show()

    def crear_centro(self):
        centro = Centro_Operacion()
        centro.set_escoltas(random.randint(10,20))
        centro.set_vehiculos(random.randint(5,10))
        centro.set_dinero(random.randint(10000000,100000000)) #cien millones

        self.centros.append(centro)
