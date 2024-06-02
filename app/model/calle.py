import networkx as nx
import matplotlib.pyplot as plt

Calle = nx.Graph()

Calle.add_node('Centro de operación A')
Calle.add_node(2)
Calle.add_node(3)
Calle.add_edge('Centro de operación A', 2)
Calle.add_edge(1, 3)
Calle.add_edge(2, 3)

nx.draw(Calle, with_labels=True)
plt.show()
