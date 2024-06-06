import networkx as nx
from app.model.centro_operacion import Centro_Operacion
from app.model.cliente import Cliente
import random

class Calle:
    def __init__(self) -> None:
        self.calle = nx.Graph()
        self.centros = []
        self.clientes = []
        self.edificios = ['Tienda Don Jhon', 'Restaurante La Buena Mesa', 'Panadería El Trigo',
            'Supermercado El Ahorro', 'Librería El Saber', 'Farmacia La Salud',
            'Escuela Primaria', 'Universidad Nacional', 'Gimnasio Fitness Plus', 'Clínica Dental Sonrisas']
        self.ubicaciones = []
        self.node_colors = []
        self.crear_calle()
    
    def crear_calle(self):
        for i in range(5):
            self.crear_centro()
            if (2*i+1) < len(self.edificios):
                self.crear_nodo(self.edificios[2*i])
                self.ubicaciones.append(self.edificios[(2*i)])
                self.ubicaciones.append(self.edificios[2*i+1])
                self.crear_nodo(self.edificios[2*i+1])
            self.crear_cliente()

        print(self.ubicaciones)

        for i in range(0, len(self.ubicaciones)-1):
            if (i+1) % 5 != 0: #si es el último
                self.crear_aristas(self.ubicaciones[i], self.ubicaciones[i+1])
            if (i % 5) != 0: #si es el primero
                self.crear_aristas(self.ubicaciones[i], self.ubicaciones[i-1])
            if (i - 5) >= len(self.ubicaciones):
                self.crear_aristas(self.ubicaciones[i], self.ubicaciones[i-5])
            if (i + 5) < len(self.ubicaciones):
                self.crear_aristas(self.ubicaciones[i], self.ubicaciones[i+5])

        self.node_colors = [
            'red' if nodo in [centro.nombre for centro in self.centros] else 
            ('green' if nodo in [cliente.nombre for cliente in self.clientes] else 'blue')
            for nodo in self.calle.nodes
        ]
        nx.draw(self.calle)

    def crear_cliente(self):
        cliente = Cliente()

        while cliente.nombre in [c.nombre for c in self.clientes]:
            cliente = Cliente()

        self.clientes.append(cliente)
        self.ubicaciones.append(cliente.nombre)
        self.crear_nodo(cliente.nombre)


    def crear_centro(self):
        centro = Centro_Operacion()

        while centro.nombre in [c.nombre for c in self.centros]:
            centro = Centro_Operacion()
            
        centro.set_escoltas(random.randint(10,20))
        centro.set_vehiculos(random.randint(5,10))
        centro.set_dinero(random.randint(10000000,100000000))

        self.centros.append(centro)
        self.ubicaciones.append(centro.nombre)
        self.crear_nodo(centro.nombre)

    def crear_aristas(self, edificio1, edificio2):
        self.calle.add_edge(edificio1, edificio2)

    def crear_nodo(self, edificio):
        self.calle.add_node(edificio)

