import matplotlib
matplotlib.use('TkAgg')  # Cambia TkAgg por otro backend si es necesario

from app.model.calle import Calle  # Asegúrate de que esta ruta sea correcta
import matplotlib.pyplot as plt
import networkx as nx

class Main:
    def __init__(self):
        self.calle = Calle()
        
    def run(self):
        plt.show()  # Muestra el grafo utilizando matplotlib

if __name__ == "__main__":
    app = Main()
    app.run()
