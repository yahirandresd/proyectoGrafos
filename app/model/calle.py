import networkx as nx
from app.model.centro_operacion import Centro_Operacion
from app.model.cliente import Cliente
import random

class Calle:
    def __init__(self) -> None:
        self.calle = nx.Graph()
        self.edificios = [
            'Tienda Don Jhon', 'Restaurante La Buena Mesa', 'Panadería El Trigo',
            'Supermercado El Ahorro', 'Librería El Saber', 'Farmacia La Salud',
            'Escuela Primaria', 'Instituto Secundario', 'Universidad Nacional',
            'Hospital General', 'Clínica Dental', 'Gimnasio Fitness Plus',
            'Parque Central', 'Museo de Historia', 'Teatro Municipal',
            'Tienda El Rincón', 'Restaurante La Esquina', 'Panadería El Trigo',
            'Supermercado El Ahorro', 'Librería El Saber', 'Farmacia La Salud',
            'Escuela Primaria San Juan', 'Instituto Secundario Los Pinos',
            'Universidad Nacional del Valle', 'Hospital General San Rafael',
            'Clínica Dental Sonrisas', 'Gimnasio Fitness Plus', 'Parque Central',
            'Museo de Historia Ciudad Vieja', 'Teatro Municipal El Faro'
        ]
        self.ubicaciones = []
        self.centros = []
        self.clientes = []
        self.crear_calle()

    def crear_calle(self):
        for i in range(25):
            self.crear_ubicacion()
            self.calle.add_node(self.ubicaciones[i])

        print(len(self.ubicaciones))
        
        for i in range(0, len(self.ubicaciones)-1):
            if (i+1) % 5 != 0: #si es el último
                self.crear_aristas(self.ubicaciones[i], self.ubicaciones[i+1])
            if (i % 5) != 0: #si es el primero
                self.crear_aristas(self.ubicaciones[i], self.ubicaciones[i-1])
            if (i - 5) >= len(self.ubicaciones):
                self.crear_aristas(self.ubicaciones[i], self.ubicaciones[i-5])
            if (i + 5) < len(self.ubicaciones):
                self.crear_aristas(self.ubicaciones[i], self.ubicaciones[i+5])

        node_colors = ['red' if nodo in self.centros else ('green' if nodo in self.clientes else 'blue') for nodo in self.calle.nodes]

        nx.draw(self.calle, with_labels=True, node_color=node_colors, node_size=500)

    def crear_ubicacion(self):
        centro = Centro_Operacion()
        centro.set_escoltas(random.randint(10,20))
        centro.set_vehiculos(random.randint(5,10))
        centro.set_dinero(random.randint(10000000,100000000)) #cien millones

        cliente = Cliente()

        if centro.nombre not in self.ubicaciones:
            self.ubicaciones.append(centro.nombre)
            self.centros.append(centro.nombre)
        elif cliente.nombre not in self.ubicaciones:
            self.ubicaciones.append(cliente.nombre)
            self.clientes.append(cliente.nombre)
        else:
            edificio_nuevo = random.choice(self.edificios)
            while edificio_nuevo in self.ubicaciones:
                edificio_nuevo = random.choice(self.edificios)
            self.ubicaciones.append(edificio_nuevo)
        
    def crear_aristas(self, edificio1, edificio2):
        self.calle.add_edge(edificio1, edificio2)
