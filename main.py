# Importar las bibliotecas necesarias
import mesa
import networkx as nx
import matplotlib.pyplot as plt

# Crear una clase de agente
class GraphAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        # Definir el comportamiento del agente en cada paso
        pass

# Crear una clase de modelo
class GraphModel(mesa.Model):
    def __init__(self, N):
        self.num_agents = N
        self.schedule = mesa.time.RandomActivation(self)

        # Crear una red de grafos utilizando NetworkX
        self.graph = nx.erdos_renyi_graph(n=N, p=0.1)

        # Crear agentes y añadirlos al modelo
        for i in range(self.num_agents):
            agent = GraphAgent(i, self)
            self.schedule.add(agent)

    def step(self):
        self.schedule.step()

# Inicializar y ejecutar el modelo
num_agents = 10
model = GraphModel(num_agents)

for i in range(10):
    model.step()

# Dibujar el grafo utilizando Matplotlib
pos = nx.spring_layout(model.graph)
nx.draw(model.graph, pos, with_labels=True)
plt.show()
