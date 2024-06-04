import matplotlib
matplotlib.use('TkAgg')  # Cambia TkAgg por otro backend si es necesario

import tkinter as tk
from tkinter import ttk
import networkx as nx
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
from app.model.calle import Calle  # Asegúrate de que esta ruta sea correcta


class Main:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Planificador de Rutas")
        self.calle = Calle()

        # Crear interfaz de selección de nodos
        self.start_label = tk.Label(self.root, text="Nodo de Inicio")
        self.start_label.pack()
        self.start_node = ttk.Combobox(self.root, values=self.calle.edificios)
        self.start_node.pack()

        self.end_label = tk.Label(self.root, text="Nodo de Destino")
        self.end_label.pack()
        self.end_node = ttk.Combobox(self.root, values=self.calle.edificios)
        self.end_node.pack()

        self.button = tk.Button(self.root, text="Empezar Ruta", command=self.start_route)
        self.button.pack()

        # Crear el gráfico
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack()

        self.draw_graph()

    def draw_graph(self):
        self.ax.clear()
        self.figure.set_size_inches(20, 8)  # Establece el tamaño de la figura
        self.pos = nx.spring_layout(self.calle.calle)
        nx.draw(self.calle.calle, self.pos, with_labels=True, node_color=self.calle.node_colors, node_size=500,
                ax=self.ax)
        self.canvas.draw()
        # Ajusta el tamaño del recuadro del lienzo de Tkinter para que se expanda y llene el espacio disponible
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def start_route(self):
        start = self.start_node.get()
        end = self.end_node.get()
        if start and end:
            try:
                self.path = nx.shortest_path(self.calle.calle, source=start, target=end)
                self.animate_path()
            except nx.NetworkXNoPath:
                print("No existe una ruta entre los nodos seleccionados.")
        else:
            print("Seleccione nodos válidos.")

    def animate_path(self):
        self.show_path(self.path)
        self.anim = FuncAnimation(self.figure, self.update_animation, frames=len(self.path), interval=500, repeat=False)
        self.canvas.draw()

    def show_path(self, path):
        self.ax.clear()
        nx.draw(self.calle.calle, self.pos, with_labels=True, node_color=self.calle.node_colors, node_size=500, ax=self.ax)
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(self.calle.calle, self.pos, edgelist=path_edges, edge_color='green', width=2.0, ax=self.ax)
        self.canvas.draw()

    def update_animation(self, i):
        if i < len(self.path):
            self.ax.clear()
            nx.draw(self.calle.calle, self.pos, with_labels=True, node_color=self.calle.node_colors, node_size=500, ax=self.ax)
            path_edges = list(zip(self.path, self.path[1:]))
            nx.draw_networkx_edges(self.calle.calle, self.pos, edgelist=path_edges, edge_color='green', width=2.0, ax=self.ax)
            current_node = self.path[i]
            current_pos = self.pos[current_node]
            self.ax.plot(current_pos[0], current_pos[1], 'ro', markersize=12)  # Circle representing the moving point
            self.canvas.draw()

    def run(self):
        self.root.geometry("1280x720")
        self.root.mainloop()  # Inicia el bucle principal de Tkinter


if __name__ == "__main__":
    app = Main()
    app.run()
