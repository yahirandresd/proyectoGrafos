import matplotlib
matplotlib.use('TkAgg')  # Cambia TkAgg por otro backend si es necesario

import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
from app.model.calle_nueva import Calle  # Asegúrate de que esta ruta sea correcta


class Main:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Planificador de Rutas")
        self.calle = Calle()

        # Crear un Frame para la entrada de nodos y el Spinbox
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(pady=10)

        # Crear interfaz de selección de nodos
        self.start_label = tk.Label(self.input_frame, text="Nodo de Inicio")
        self.start_label.grid(row=0, column=0, padx=5)
        self.start_node = ttk.Combobox(self.input_frame, values=self.calle.ubicaciones, state="readonly")
        self.start_node.grid(row=0, column=1, padx=5)

        self.end_label = tk.Label(self.input_frame, text="Nodo de Destino")
        self.end_label.grid(row=1, column=0, padx=5)
        self.end_node = ttk.Combobox(self.input_frame, values=self.calle.ubicaciones, state="readonly")
        self.end_node.grid(row=1, column=1, padx=5)

        self.button = tk.Button(self.input_frame, text="Empezar Ruta", command=self.start_route)
        self.button.grid(row=2, column=0, columnspan=2, pady=10)

        # Agregar el Spinbox para ingresar la cantidad
        self.amount_label = tk.Label(self.input_frame, text="Cantidad (10 a 100)")
        self.amount_label.grid(row=0, column=2, padx=5)
        self.amount_spinbox = tk.Spinbox(self.input_frame, from_=0, to=100, validate="all", validatecommand=(self.root.register(self.validate_spinbox), '%P'))
        self.amount_spinbox.grid(row=0, column=3, padx=5)

        # Crear el gráfico
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.draw_graph()

    def validate_spinbox(self, value):
        # Ensure the value is numeric and within the specified range
        if value.isdigit():
            num = int(value)
            if 0 <= num <= 100:
                return True
        return False

    def draw_graph(self):
        self.ax.clear()
        self.figure.set_size_inches(20, 8)  # Establece el tamaño de la figura
        self.pos = nx.spring_layout(self.calle.calle)
        nx.draw(self.calle.calle, self.pos, with_labels=True, node_color=self.calle.node_colors, node_size=500, edge_color = self.calle.edge_colors, ax=self.ax)
        nx.draw_networkx_edge_labels(self.calle.calle, self.pos, edge_labels=self.calle.edge_labels)
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
        self.root.geometry("1420x920")  # Establece el tamaño de la ventana principal (ancho x alto)
        self.root.mainloop()  # Inicia el bucle principal de Tkinter


if __name__ == "__main__":
    app = Main()
    app.run()
