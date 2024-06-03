from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import NetworkGrid
from mesa.visualization.modules import NetworkModule
from mesa.visualization.ModularVisualization import ModularServer
from app.model.calle import Calle  # Asegúrate de que esta ruta sea correcta
import networkx as nx

class GraphAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.calle = Calle()

    def step(self):
        pass

class GraphModel(Model):
    def __init__(self):
        self.num_agents = 10
        self.G = nx.erdos_renyi_graph(n=self.num_agents, p=0.2)
        self.grid = NetworkGrid(self.G)
        self.schedule = RandomActivation(self)
        self.calle = Calle()  # Crear instancia de Calle dentro del modelo

        for i, node in enumerate(self.G.nodes):
            agent = GraphAgent(i, self)
            self.grid.place_agent(agent, node)
            self.schedule.add(agent)

    def step(self):
        self.schedule.step()

def network_portrayal(G):
    portrayal = {}
    portrayal["nodes"] = [{"id": n} for n in G.nodes]
    portrayal["edges"] = [{"source": u, "target": v} for u, v in G.edges]
    return portrayal

network = NetworkModule(network_portrayal, 500, 500)

model_params = {}
server = ModularServer(GraphModel, [network], "Graph Model", model_params)
server.port = 8521
server.launch()
