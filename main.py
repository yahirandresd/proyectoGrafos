import matplotlib
matplotlib.use('TkAgg')

import tkinter as tk
from tkinter import ttk
import networkx as nx
import os
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
from app.model.calle_nueva import Calle  # Asegúrate de que esta ruta sea correcta
from app.model.carro import Carro

class Main:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Planificador de Rutas")
        self.calle = Calle()

        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(pady=10)
        self.car_scale = 0.2

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

        self.amount_label = tk.Label(self.input_frame, text="Cantidad (10 a 100)")
        self.amount_label.grid(row=0, column=2, padx=5)
        self.amount_spinbox = tk.Spinbox(self.input_frame, from_=0, to=100, validate="all", validatecommand=(self.root.register(self.validate_spinbox), '%P'))
        self.amount_spinbox.grid(row=0, column=3, padx=5)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.carro = Carro('grande')
        self.draw_graph()

        image_folder = os.path.join(os.path.dirname(__file__), 'images')

        self.car_images = {
            'grande': mpimg.imread(os.path.join(image_folder, 'cGran.png')),
            'pequeño': mpimg.imread(os.path.join(image_folder, 'cPeque.png')),
            # 'escolta': mpimg.imread(os.path.join(image_folder, 'imagen_escolta.png')),
            # 'ladron': mpimg.imread(os.path.join(image_folder, 'imagen_ladron.png'))
        }

    def validate_spinbox(self, value):
        if value.isdigit():
            num = int(value)
            if 0 <= num <= 100:
                return True
        return False

    def draw_graph(self):
        self.ax.clear()
        self.figure.set_size_inches(20, 8)
        self.pos = nx.spring_layout(self.calle.calle)
        nx.draw(self.calle.calle, self.pos, with_labels=True, node_color=self.calle.node_colors, node_size=500, edge_color=self.calle.edge_colors, ax=self.ax)
        nx.draw_networkx_edge_labels(self.calle.calle, self.pos, edge_labels=self.calle.edge_labels)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def start_route(self):
        start = self.start_node.get()
        end = self.end_node.get()
        if start and end:
            try:
                self.path = nx.shortest_path(self.calle.calle, source=start, target=end)
                self.interpolated_positions = self.interpolate_positions(self.path)
                self.carro.get_carro().posicion_actual = self.interpolated_positions[0]
                self.animate_path()
            except nx.NetworkXNoPath:
                print("No existe una ruta entre los nodos seleccionados.")
        else:
            print("Seleccione nodos válidos.")

    def interpolate_positions(self, path):
        interpolated_positions = []
        for i in range(len(path) - 1):
            start_pos = self.pos[path[i]]
            end_pos = self.pos[path[i + 1]]
            steps = 20
            for j in range(steps):
                interp_pos = start_pos + (end_pos - start_pos) * j / steps
                interpolated_positions.append(interp_pos)
        return interpolated_positions

    def animate_path(self):
        velocidad = self.carro.get_carro().velocidad
        frames = len(self.interpolated_positions) // velocidad
        self.anim = FuncAnimation(self.figure, self.update_animation, frames=frames, interval=50, repeat=False)
        self.canvas.draw()

    def show_path(self, path):
        self.ax.clear()
        nx.draw(self.calle.calle, self.pos, with_labels=True, node_color=self.calle.node_colors, node_size=500, ax=self.ax)
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(self.calle.calle, self.pos, edgelist=path_edges, edge_color='green', width=2.0, ax=self.ax)
        self.canvas.draw()

    def update_animation(self, i):
        self.ax.clear()
        nx.draw(self.calle.calle, self.pos, with_labels=True, node_color=self.calle.node_colors, node_size=500, ax=self.ax)
        path_edges = list(zip(self.path, self.path[1:]))
        nx.draw_networkx_edges(self.calle.calle, self.pos, edgelist=path_edges, edge_color='green', width=2.0, ax=self.ax)

        self.ax.set_xlim(-1, 1)  # Establece límites de eje x
        self.ax.set_ylim(-1, 1)

        if i < len(self.interpolated_positions):
            pos_index = i * self.carro.get_carro().velocidad
            if pos_index < len(self.interpolated_positions):
                self.carro.get_carro().actualizar_posicion(self.interpolated_positions[pos_index])
                current_pos = self.carro.get_carro().posicion_actual
                carro_tipo = self.carro.tipo

                if carro_tipo in self.car_images:
                    image = self.car_images[carro_tipo]
                    self.ax.imshow(image, extent=[current_pos[0] - 0.5 * self.car_scale,
                                                  current_pos[0] + 0.5 * self.car_scale,
                                                  current_pos[1] - 0.5 * self.car_scale,
                                                  current_pos[1] + 0.5 * self.car_scale])
                else:
                    print("Imagen no encontrada para el tipo de carro:", carro_tipo)

        self.canvas.draw()

    def run(self):
        self.root.geometry("1420x920")
        self.root.mainloop()

if __name__ == "__main__":
    app = Main()
    app.run()
