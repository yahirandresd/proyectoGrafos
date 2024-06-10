import matplotlib
matplotlib.use('TkAgg')

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import networkx as nx
import os
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
from app.model.calle import Calle  # Asegúrate de que esta ruta sea correcta
from app.model.carro import Carro

class Main:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Planificador de Rutas")
        self.root.geometry("1200x800")  # Configura el tamaño inicial de la ventana
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.calle = Calle()

        self.button_frame = tk.Frame(self.root, width=1)
        self.button_frame.grid(row=0, column=0, pady=10, sticky="ew")

        self.order_button = tk.Button(self.button_frame, text="Hacer Orden", command=self.show_order_form)
        self.order_button.grid(row=0, column=0, padx=5, pady=5)

        self.car_stats_button = tk.Button(self.button_frame, text="Estadísticas del Carro", command=self.update_car_stats)
        self.car_stats_button.grid(row=0, column=1, padx=5, pady=5)

        self.center_stats_button = tk.Button(self.button_frame, text="Estadísticas de Centros", command=self.show_center_stats)
        self.center_stats_button.grid(row=0, column=2, padx=5, pady=5)

        self.car_scale = 0.2

        self.carro_stats = tk.Text(self.root, state='disabled')
        self.carro_stats.grid(row=1, column=0, padx=10, pady=10, columnspan=1, sticky="nsew")

        self.centro_stats = tk.Text(self.root, state='disabled')
        self.centro_stats.grid(row=1, column=1, padx=10, pady=10, columnspan=1, sticky="nsew")

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().grid(row=2, column=0, sticky="nsew")

        self.carro = Carro('pequeño')
        self.draw_graph()

        image_folder = os.path.join(os.path.dirname(__file__), 'images')

        self.car_images = {
            'grande': mpimg.imread(os.path.join(image_folder, 'cGran.png')),
            'pequeño': mpimg.imread(os.path.join(image_folder, 'cPeque.png')),
        }

    def validate_spinbox(self, value):
        if value.isdigit():
            num = int(value)
            if 0 <= num <= 100:
                return True
        return False
    
    def show_order_form(self):
        self.order_window = tk.Toplevel(self.root)
        self.order_window.title("Formulario de Orden")

        self.start_label = tk.Label(self.order_window, text="Nodo de Inicio")
        self.start_label.grid(row=0, column=0, padx=5)
        self.start_node = ttk.Combobox(self.order_window, values=self.calle.ubicaciones, state="readonly")
        self.start_node.grid(row=0, column=1, padx=5)

        self.end_label = tk.Label(self.order_window, text="Nodo de Destino")
        self.end_label.grid(row=1, column=0, padx=5)
        self.end_node = ttk.Combobox(self.order_window, values=self.calle.ubicaciones, state="readonly")
        self.end_node.grid(row=1, column=1, padx=5)

        self.amount_label = tk.Label(self.order_window, text="Cantidad (10 a 100)")
        self.amount_label.grid(row=2, column=0, padx=5)
        self.amount_spinbox = tk.Spinbox(self.order_window, from_=0, to=100, validate="all", validatecommand=(self.root.register(self.validate_spinbox), '%P'))
        self.amount_spinbox.grid(row=2, column=1, padx=5)

        self.button = tk.Button(self.order_window, text="Empezar Ruta", command=self.start_route)
        self.button.grid(row=3, column=0, columnspan=2, pady=10)

    def show_center_stats(self):
        for item in self.calle.centros:
            print(item.nombre)
            stats = f"{item.nombre}:\n"
            stats += f"Capacidad de dinero: {item.capacidad_dinero}\n"
            stats += f"Capacidad de escoltas: {item.capacidad_escoltas}\n"
            stats += f"Capacidad de vehículos: {item.capacidad_vehiculos}\n"
            stats += "\n"

            self.centro_stats.config(state='normal')
            self.centro_stats.insert(tk.END, stats)

        self.centro_stats.config(state='disabled')


    def draw_graph(self):
        self.ax.clear()
        self.figure.set_size_inches(20, 8)
        self.pos = nx.spring_layout(self.calle.calle)
        nx.draw(self.calle.calle, self.pos, with_labels=True, node_color=self.calle.node_colors, node_size=500, edge_color=self.calle.edge_colors, ax=self.ax)
        nx.draw_networkx_edge_labels(self.calle.calle, self.pos, edge_labels=self.calle.edge_labels)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=2, column=0, columnspan=2, sticky="nsew")

    def start_route(self):
        start = self.start_node.get()
        end = self.end_node.get()
        if start and end:
            try:
                self.path = nx.shortest_path(self.calle.calle, source=start, target=end)
                if self.revisar_pesos():
                    self.interpolated_positions = self.interpolate_positions(self.path)
                    self.carro.get_carro().posicion_actual = self.interpolated_positions[0]
                    self.animate_path()
                else:
                    messagebox.showinfo('Atención', "El puente no puede soportar el peso del vehículo. Buscando ruta alternativa...")
                    alternative_path = self.find_alternative_route(start, end)
                    if alternative_path:
                        self.path = alternative_path
                        self.interpolated_positions = self.interpolate_positions(self.path)
                        self.carro.get_carro().posicion_actual = self.interpolated_positions[0]
                        self.animate_path()
                    else:
                        messagebox.showinfo('Error', "No se encontró una ruta alternativa.")
            except nx.NetworkXNoPath:
                messagebox.showinfo('Error', "No existe una ruta entre los nodos seleccionados.")
        else:
            messagebox.showinfo('Error', "Seleccione nodos válidos.")

    def revisar_pesos(self):
        for i in range(len(self.path) - 1):
            start = self.path[i]
            end = self.path[i + 1]
            edge_data = self.calle.calle.get_edge_data(start, end)
            if edge_data and 'peso' in edge_data:
                peso_maximo = edge_data['peso']
                if self.carro.get_carro().peso > peso_maximo:
                    return False
        return True
    
    def find_alternative_route(self, start, end):
        G = self.calle.calle.copy()
        
        edges_to_remove = [(u, v) for u, v, data in G.edges(data=True) if data.get('peso', float('inf')) < self.carro.get_carro().peso]
        G.remove_edges_from(edges_to_remove)
        
        try:
            return nx.shortest_path(G, source=start, target=end)
        except nx.NetworkXNoPath:
            return None

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
        
        # Dibuja el grafo con los colores originales de las aristas
        nx.draw(self.calle.calle, self.pos, with_labels=True, node_color=self.calle.node_colors, node_size=500, edge_color=self.calle.edge_colors, ax=self.ax)
        nx.draw_networkx_edge_labels(self.calle.calle, self.pos, edge_labels = self.calle.edge_labels, ax=self.ax)

        # Obtén las aristas del camino y colóralas en verde
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

    def update_car_stats(self):
        stats = f"Tipo de carro: {self.carro.tipo}\n"
        stats += f"Peso: {self.carro.get_carro().peso}\n"
        stats += f"Velocidad: {self.carro.get_carro().velocidad}\n"
        stats += f"Escudo: {self.carro.get_carro().escudo}\n"
        stats += f"Ataque: {self.carro.get_carro().ataque}\n"
        stats += f"Capacidad: {self.carro.get_carro().capacidad}\n"
        
        self.carro_stats.config(state='normal')
        self.carro_stats.delete('1.0', tk.END)
        self.carro_stats.insert(tk.END, stats)
        self.carro_stats.config(state='disabled')

    def run(self):
        self.root.geometry("1420x920")
        self.root.mainloop()

if __name__ == "__main__":
    app = Main()
    app.run()
