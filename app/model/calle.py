import matplotlib
matplotlib.use('TkAgg')  # Cambia TkAgg por otro backend si es necesario

import networkx as nx
import matplotlib.pyplot as plt
from app.model.carro import Carro
from app.model.centro_operacion import Centro_Operacion
import random

class Calle:
    def __init__(self) -> None:
        self.calle = nx.Graph()
        self.ubicaciones = []
        self.edificios = [
            'Tienda Don Jhon', 'Restaurante La Buena Mesa', 'Panadería El Trigo',
            'Supermercado El Ahorro', 'Librería El Saber', 'Farmacia La Salud',
            'Escuela Primaria', 'Instituto Secundario', 'Universidad Nacional',
            'Hospital General', 'Clínica Dental', 'Gimnasio Fitness Plus',
            'Parque Central', 'Museo de Historia', 'Teatro Municipal'
        ]
        self.crear_calle()

    def crear_calle(self):
        for i in range(16):
            self.crear_ubicacion()
            self.ubicaciones.append(self.edificios[i])
            self.calle.add_node(self.edificios[i])

        print(self.ubicaciones)

        for i in range(0, len(self.ubicaciones)-1):
            if (i+1) % 5 != 0: #si es el último
                self.crear_aristas(self.ubicaciones[i], self.ubicaciones[i+1])
            if (i % 5) != 0: #si es el primero
                self.crear_aristas(self.ubicaciones[i], self.ubicaciones[i-1])
            if (i - 5) > len(self.ubicaciones):
                self.crear_aristas(self.ubicaciones[i], self.ubicaciones[i-5])
            if (i + 5) < len(self.ubicaciones):
                self.crear_aristas(self.ubicaciones[i], self.ubicaciones[i+5])


        nx.draw(self.calle, with_labels=True, node_color='red', node_size=500)
        plt.show()

    def crear_ubicacion(self):
        centro = Centro_Operacion()
        centro.set_escoltas(random.randint(10,20))
        centro.set_vehiculos(random.randint(5,10))
        centro.set_dinero(random.randint(10000000,100000000)) #cien millones

        if centro.nombre not in self.ubicaciones:
            self.ubicaciones.append(centro.nombre)
            self.edificios.append(centro.nombre)
            self.calle.add_node(centro.nombre)
            return True

    def crear_aristas(self, edificio1, edificio2):
        self.calle.add_edge(edificio1, edificio2)

