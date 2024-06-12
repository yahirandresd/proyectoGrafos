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
import time
from app.model.calle import Calle  # Asegúrate de que esta ruta sea correcta
from app.model.carro import Carro


class Main:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Planificador de Rutas")
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(1, weight=1)

        self.calle = Calle()

        # la lista de rutas que van a tener los carros

        self.ordenes = []

        self.tiempo_transcurrido = 0

        self.button_frame = tk.Frame(self.root, width=1)
        self.button_frame.grid(row=0, column=0, pady=10, sticky="ew")

        self.order_button = tk.Button(self.button_frame, text="Hacer Orden", command=self.show_order_form)
        self.order_button.grid(row=0, column=1, padx=5, pady=5)

        self.center_stats_button = tk.Button(self.button_frame, text="Empezar rutas", command=self.start_route)
        self.center_stats_button.grid(row=0, column=3, padx=5, pady=5)

        self.car_scale = 0.2

        self.carro_stats = tk.Text(self.button_frame, state='disabled', height=10, width=54)
        self.carro_stats.grid(row=1, column=0, padx=10, pady=10, columnspan=1, sticky="nsew")

        self.centro_stats = tk.Text(self.button_frame, state='disabled', height=10, width=54)
        self.centro_stats.grid(row=1, column=1, padx=10, pady=10, columnspan=3, sticky="nsew")

        self.ordenes_stats = tk.Text(self.button_frame, state='disabled', wrap='word', height=10, width=54)
        self.ordenes_stats.grid(row=1, column=4, padx=10, pady=10, columnspan=1, sticky="nsew")

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().grid(row=2, column=0, columnspan=10, sticky="nsew")

        self.draw_graph()

        image_folder = os.path.join(os.path.dirname(__file__), 'images')

        self.car_images = {
            'grande': mpimg.imread(os.path.join(image_folder, 'cGran.png')),
            'pequeño': mpimg.imread(os.path.join(image_folder, 'cPeque.png')),
        }

        self.show_center_stats()

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
        self.start_node = ttk.Combobox(self.order_window, values=[cliente.nombre for cliente in self.calle.clientes],
                                       state="readonly")
        self.start_node.grid(row=0, column=1, padx=5)

        self.end_label = tk.Label(self.order_window, text="Nodo de Destino")
        self.end_label.grid(row=1, column=0, padx=5)
        self.end_node = ttk.Combobox(self.order_window, values=[centro.nombre for centro in self.calle.centros],
                                     state="readonly")
        self.end_node.grid(row=1, column=1, padx=5)

        self.amount_label = tk.Label(self.order_window, text="Cantidad (10 a 100)")
        self.amount_label.grid(row=2, column=0, padx=5)
        self.amount_spinbox = tk.Spinbox(self.order_window, from_=0, to=100, validate="all",
                                         validatecommand=(self.root.register(self.validate_spinbox), '%P'))
        self.amount_spinbox.grid(row=2, column=1, padx=5)

        self.tiempo_label = tk.Label(self.order_window, text="Tiempo de entrega (segundos):")
        self.tiempo_label.grid(row=3, column=0, padx=5)
        self.tiempo_entry = ttk.Entry(self.order_window)
        self.tiempo_entry.grid(row=3, column=1, padx=5)

        self.button = ttk.Button(self.order_window, text="Enlistar orden", command=self.validar_orden)
        self.button.grid(row=4, column=0, columnspan=2, pady=10)

    def validar_orden(self):
        if int(self.amount_spinbox.get()) < 50:
            self.carro = Carro('pequeño')
        else:
            self.carro = Carro('grande')

        orden = [self.start_node.get(), self.end_node.get(), int(self.amount_spinbox.get()),
                 int(self.tiempo_entry.get()), self.carro]
        tiempo_calculado = self.simular_viaje(orden[0], orden[1])
        orden[3] = tiempo_calculado

        cantidad = orden[2] * 10 ** 6

        if self.validar_capacidad(cantidad, orden):
            if tiempo_calculado < int(self.tiempo_entry.get()):
                self.ordenes.append(orden)
                self.show_center_stats()
                self.show_ordenes()
            else:
                continuar = tk.Toplevel(self.root)
                continuar.title("Atención")
                mensaje = tk.Label(continuar,
                                   text=f"El tiempo de viaje estimado es {tiempo_calculado:.2f} segundos. ¿Desea hacer la orden de igual manera?")
                mensaje.pack()
                boton_si = ttk.Button(continuar, text="Sí",
                                      command=lambda: [self.ordenes.append(orden), self.show_ordenes(),
                                                       continuar.destroy(), self.show_center_stats()])
                boton_si.pack(side="left", padx=5)
                boton_no = ttk.Button(continuar, text="No",
                                      command=lambda: [messagebox.showinfo('', 'La orden no se ha realizado'),
                                                       self.show_ordenes(), continuar.destroy()])
                boton_no.pack(side="left", padx=5)
                continuar.focus_set()
                continuar.grab_set()
                self.root.wait_window(continuar)

            self.order_window.destroy()

    def validar_capacidad(self, cantidad, orden):
        for centro in self.calle.centros:
            if centro.nombre == orden[1]:
                if centro.capacidad_dinero < cantidad or centro.capacidad_escoltas < self.carro.get_carro().escoltas or centro.capacidad_vehiculos < 1:
                    messagebox.showinfo('Capacidad del centro copada', 'Por favor, seleccione otro centro.')
                    return False
                else:
                    centro.capacidad_dinero -= cantidad
                    centro.capacidad_escoltas -= self.carro.get_carro().escoltas
                    centro.capacidad_vehiculos -= 1
                    return True

    def simular_viaje(self, nodo1, nodo2):
        distancia = nx.shortest_path_length(self.calle.calle, source=nodo1, target=nodo2)

        tiempo_viaje = distancia / self.carro.get_carro().velocidad

        return tiempo_viaje

    def show_center_stats(self):
        self.centro_stats.config(state='normal')
        self.centro_stats.delete('1.0', tk.END)

        for item in self.calle.centros:
            stats = f"{item.nombre}:\n"
            stats += f"Capacidad de dinero: {item.capacidad_dinero}\n"
            stats += f"Capacidad de escoltas: {item.capacidad_escoltas}\n"
            stats += f"Capacidad de vehículos: {item.capacidad_vehiculos}\n"
            stats += "\n"

            self.centro_stats.insert(tk.END, stats)

        self.centro_stats.config(state='disabled')

    def show_ordenes(self):
        self.ordenes_stats.config(state='normal')
        self.ordenes_stats.delete('1.0', tk.END)  # Limpiar el widget antes de insertar nuevos datos

        for i in range(len(self.ordenes)):
            stats = f"{i + 1}.\n"
            stats += f"Nodo inicio: {self.ordenes[i][0]}\n"
            stats += f"Nodo fin: {self.ordenes[i][1]}\n"
            stats += f"Cantidad de dinero: {self.ordenes[i][2] * 10 ** 6}\n"
            stats += f"Tiempo estimado: {self.ordenes[i][3]:.2f} segundos\n"
            stats += f"Tipo de carro: {self.ordenes[i][4].tipo}\n"
            stats += "\n"

            self.ordenes_stats.insert(tk.END, stats)

        self.ordenes_stats.config(state='disabled')

    def draw_graph(self):
        self.ax.clear()
        self.figure.set_size_inches(20, 8)
        self.pos = nx.spring_layout(self.calle.calle)
        nx.draw(self.calle.calle, self.pos, with_labels=True, node_color=self.calle.node_colors, node_size=500,
                edge_color=self.calle.edge_colors, ax=self.ax)
        nx.draw_networkx_edge_labels(self.calle.calle, self.pos, edge_labels=self.calle.edge_labels)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=2, column=0, columnspan=2, sticky="nsew")

    def start_route(self):
        for item in self.ordenes:
            start = item[0]
            end = item[1]

            carro = item[4]

            self.ruta = item[4]

            self.update_car_stats(carro)

            inicio_tiempo = time.time()
            if start and end:
                try:
                    self.path = nx.shortest_path(self.calle.calle, source=start, target=end)
                    if self.revisar_pesos(carro):
                        self.interpolated_positions = self.interpolate_positions(self.path)
                        carro.posicion_actual = self.interpolated_positions[0]
                        self.animate_path(carro)
                    else:
                        messagebox.showinfo('Atención',
                                            "El puente no puede soportar el peso del vehículo. Buscando ruta alternativa...")
                        alternative_path = self.find_alternative_route(start, end, carro)
                        if alternative_path:
                            self.path = alternative_path
                            self.interpolated_positions = self.interpolate_positions(self.path)
                            carro.posicion_actual = self.interpolated_positions[0]
                            self.animate_path(carro)
                        else:
                            messagebox.showinfo('Error', "No se encontró una ruta alternativa.")
                except nx.NetworkXNoPath:
                    messagebox.showinfo('Error', "No existe una ruta entre los nodos seleccionados.")
            else:
                messagebox.showinfo('Error', "Seleccione nodos válidos.")

            self.tiempo_transcurrido = time.time() - inicio_tiempo  # Calcular el tiempo transcurrido

            # Crear la ventana emergente para preguntar al usuario si desea continuar
            continuar = tk.Toplevel(self.root)
            continuar.title("Continuar?")
            mensaje = tk.Label(continuar, text="¿Desea continuar con la siguiente orden?")
            mensaje.pack()
            boton_si = ttk.Button(continuar, text="Sí", command=continuar.destroy)
            boton_si.pack(side="left", padx=5)
            boton_no = ttk.Button(continuar, text="No",
                                  command=lambda: [messagebox.showinfo('Información', 'Simulación finalizada.'),
                                                   continuar.destroy()])
            boton_no.pack(side="left", padx=5)
            continuar.focus_set()
            continuar.grab_set()
            self.root.wait_window(continuar)

    def revisar_pesos(self, carro):
        for i in range(len(self.path) - 1):
            start = self.path[i]
            end = self.path[i + 1]
            edge_data = self.calle.calle.get_edge_data(start, end)
            if edge_data and 'peso' in edge_data:
                peso_maximo = edge_data['peso']
                if carro.get_carro().peso > peso_maximo:
                    return False
        return True

    def find_alternative_route(self, start, end, carro):
        G = self.calle.calle.copy()

        edges_to_remove = [(u, v) for u, v, data in G.edges(data=True) if
                           data.get('peso', float('inf')) < carro.get_carro().peso]
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

    def animate_path(self, carro):
        velocidad = carro.get_carro().velocidad
        frames = len(self.interpolated_positions) // velocidad
        self.anim = FuncAnimation(self.figure, self.update_animation, frames=frames, interval=50, repeat=False)
        self.canvas.draw()

    def show_path(self, path):
        self.ax.clear()
        nx.draw(self.calle.calle, self.pos, with_labels=True, node_color=self.calle.node_colors, node_size=500,
                ax=self.ax)
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(self.calle.calle, self.pos, edgelist=path_edges, edge_color='green', width=2.0,
                               ax=self.ax)
        self.canvas.draw()

    def update_animation(self, i):
        self.ax.clear()

        # Dibuja el grafo con los colores originales de las aristas
        nx.draw(self.calle.calle, self.pos, with_labels=True, node_color=self.calle.node_colors, node_size=500,
                edge_color=self.calle.edge_colors, ax=self.ax)
        nx.draw_networkx_edge_labels(self.calle.calle, self.pos, edge_labels=self.calle.edge_labels, ax=self.ax)

        # Obtén las aristas del camino y colóralas en verde
        path_edges = list(zip(self.path, self.path[1:]))
        nx.draw_networkx_edges(self.calle.calle, self.pos, edgelist=path_edges, edge_color='green', width=2.0,
                               ax=self.ax)

        self.ax.set_xlim(-1, 1)  # Establece límites de eje x
        self.ax.set_ylim(-1, 1)

        if i < len(self.interpolated_positions):
            pos_index = i * self.ruta.get_carro().velocidad
            if pos_index < len(self.interpolated_positions):
                self.ruta.get_carro().actualizar_posicion(self.interpolated_positions[pos_index])
                current_pos = self.ruta.get_carro().posicion_actual
                carro_tipo = self.ruta.tipo

                if carro_tipo in self.car_images:
                    image = self.car_images[carro_tipo]
                    self.ax.imshow(image, extent=[current_pos[0] - 0.5 * self.car_scale,
                                                  current_pos[0] + 0.5 * self.car_scale,
                                                  current_pos[1] - 0.5 * self.car_scale,
                                                  current_pos[1] + 0.5 * self.car_scale])
                else:
                    messagebox.showwarning('Q HUBO GONORREA', "Imagen no encontrada para el tipo de carro:", carro_tipo)
        self.canvas.draw()

    def update_car_stats(self, carro):
        stats = f"Tipo de carro: {carro.tipo}\n"
        stats += f"Peso: {carro.get_carro().peso}\n"
        stats += f"Velocidad: {carro.get_carro().velocidad}\n"
        stats += f"Escudo: {carro.get_carro().escudo}\n"
        stats += f"Ataque: {carro.get_carro().ataque}\n"
        stats += f"Dinero cargado: {carro.get_carro().capacidad}\n"

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