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
        self.edge_colors = []
        self.edge_labels = []
        self.crear_calle()
    
    def crear_calle(self):
        self.crear_edificios()
        
        self.crear_centro('Centro A')
        self.crear_cliente('Falabella')
        self.crear_centro('Centro B')
        self.crear_cliente('Bancolombia')
        self.crear_centro('Centro C')
        self.crear_cliente('D1')
        self.crear_centro('Centro D')
        self.crear_cliente('Éxito')
        self.crear_centro('Centro E')
        self.crear_cliente('BBVA')

        self.crear_aristas(self.ubicaciones[0], self.ubicaciones[18], 1)
        self.calle.add_edge(self.ubicaciones[0], self.ubicaciones[19])
        self.crear_aristas(self.ubicaciones[19], self.ubicaciones[1], 2)
        self.calle.add_edge(self.ubicaciones[19], self.ubicaciones[6])
        self.calle.add_edge(self.ubicaciones[18], self.ubicaciones[6])
        self.calle.add_edge(self.ubicaciones[18], self.ubicaciones[17])
        self.calle.add_edge(self.ubicaciones[1], self.ubicaciones[16])
        self.calle.add_edge(self.ubicaciones[1], self.ubicaciones[2])
        self.calle.add_edge(self.ubicaciones[16], self.ubicaciones[6])
        self.crear_aristas(self.ubicaciones[16], self.ubicaciones[3], 0)
        self.calle.add_edge(self.ubicaciones[2], self.ubicaciones[3])
        self.calle.add_edge(self.ubicaciones[2], self.ubicaciones[15])
        self.calle.add_edge(self.ubicaciones[15], self.ubicaciones[4])
        self.calle.add_edge(self.ubicaciones[3], self.ubicaciones[4])
        self.calle.add_edge(self.ubicaciones[4], self.ubicaciones[14])
        self.calle.add_edge(self.ubicaciones[14], self.ubicaciones[7])
        self.calle.add_edge(self.ubicaciones[14], self.ubicaciones[5])
        self.crear_aristas(self.ubicaciones[5], self.ubicaciones[3], 1)
        self.calle.add_edge(self.ubicaciones[7], self.ubicaciones[11])
        self.calle.add_edge(self.ubicaciones[11], self.ubicaciones[5])
        self.calle.add_edge(self.ubicaciones[11], self.ubicaciones[12])
        self.crear_aristas(self.ubicaciones[12], self.ubicaciones[13], 1)
        self.calle.add_edge(self.ubicaciones[13], self.ubicaciones[16])
        self.calle.add_edge(self.ubicaciones[13], self.ubicaciones[5])
        self.calle.add_edge(self.ubicaciones[8], self.ubicaciones[13])
        self.calle.add_edge(self.ubicaciones[8], self.ubicaciones[17])
        self.calle.add_edge(self.ubicaciones[8], self.ubicaciones[6])
        self.calle.add_edge(self.ubicaciones[17], self.ubicaciones[10])
        self.calle.add_edge(self.ubicaciones[10], self.ubicaciones[9])
        self.calle.add_edge(self.ubicaciones[9], self.ubicaciones[12])
        self.calle.add_edge(self.ubicaciones[9], self.ubicaciones[8])

        self.node_colors = [
            'red' if nodo in [centro.nombre for centro in self.centros] else 
            ('green' if nodo in [cliente.nombre for cliente in self.clientes] else 'blue')
            for nodo in self.calle.nodes
        ]
        
        self.edge_colors = [
            'yellow' if isinstance(self.calle.get_edge_data(edge[0], edge[1]).get('peso'), int) else 'black' 
            for edge in self.calle.edges
        ]

        self.edge_labels = nx.get_edge_attributes(self.calle, 'peso')

    def crear_edificios(self):
        for item in self.edificios:
            self.crear_nodo(item)

    def crear_cliente(self, nombre):
        cliente = Cliente(nombre)

        self.clientes.append(cliente)
        self.crear_nodo(cliente.nombre)


    def crear_centro(self, nombre):
        centro = Centro_Operacion(nombre)
            
        centro.set_escoltas(random.randint(10,20))
        centro.set_vehiculos(random.randint(5,10))
        centro.set_dinero(random.randint(10000000,100000000))

        self.centros.append(centro)
        self.crear_nodo(centro.nombre)

    def crear_aristas(self, edificio1, edificio2, peso):
        self.calle.add_edge(edificio1, edificio2, peso = peso)

    def crear_nodo(self, edificio):
        self.calle.add_node(edificio)
        self.ubicaciones.append(edificio)

