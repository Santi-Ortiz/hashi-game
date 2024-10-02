import tkinter as tk
from tkinter import messagebox

class Interfaz:
    def __init__(self, tablero, jugador):
        self.tablero = tablero
        self.jugador = jugador
        self.cell_size = 50  # Tamaño de cada celda en píxeles
        self.selected_isla = None  # Isla seleccionada para conectar puentes

        # Calcula el tamaño del canvas basado en el tamaño del tablero
        self.n = len(self.tablero.tablero)
        canvas_width = self.n * self.cell_size
        canvas_height = self.n * self.cell_size

        # Crea la ventana principal
        self.root = tk.Tk()
        self.root.title(f"Hashiwokakero - Jugador: {jugador.nombre}")

        # Crea un Canvas para dibujar la grilla y los elementos
        self.canvas = tk.Canvas(self.root, width=canvas_width, height=canvas_height, bg="white")
        self.canvas.pack()

        # Dibuja la grilla inicial
        self.dibujar_grilla()

        # Asocia el evento de clic del mouse
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def dibujar_grilla(self):
        self.canvas.delete("all") 

        for x in range(self.n):
            for y in range(self.n):
                # Posición en píxeles para cada celda
                x1, y1 = y * self.cell_size, x * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size

                # Contorno de la celda
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="gray")

                # Si la celda contiene una isla, dibujarla con el número requerido
                isla = self.tablero.obtener_isla(x, y)
                if isla:
                    if isla == self.selected_isla:
                        self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="#4682B4", outline="#C4B454", width=2)
                    else:
                        self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="#87CEEB", outline="#C4B454", width=2)
                    self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=isla.conexiones_necesarias, font=("Arial", 16))

        # Dibuja puentes entre las islas
        for (i1, j1), (i2, j2) in self.tablero.conexiones:
            self._dibujar_puente(i1, j1, i2, j2, self.tablero.conexiones[((i1, j1), (i2, j2))])

    def _dibujar_puente(self, x1, y1, x2, y2, cantidad):
        # Posición de los centros de las islas
        cx1, cy1 = y1 * self.cell_size + self.cell_size // 2, x1 * self.cell_size + self.cell_size // 2
        cx2, cy2 = y2 * self.cell_size + self.cell_size // 2, x2 * self.cell_size + self.cell_size // 2

        # Dibuja puentes entre las islas
        if x1 == x2:  # Puente horizontal
            offset = 5 if cantidad == 2 else 0
            self.canvas.create_line(cx1, cy1 - offset, cx2, cy2 - offset, fill="black", width=2)
            if cantidad == 2:
                self.canvas.create_line(cx1, cy1 + offset, cx2, cy2 + offset, fill="black", width=2)
        elif y1 == y2:  # Puente vertical
            offset = 5 if cantidad == 2 else 0
            self.canvas.create_line(cx1 - offset, cy1, cx2 - offset, cy2, fill="black", width=2)
            if cantidad == 2:
                self.canvas.create_line(cx1 + offset, cy1, cx2 + offset, cy2, fill="black", width=2)

    def on_canvas_click(self, event):
        # Determina las coordenadas de la celda en la grilla que se ha hecho click
        row = event.y // self.cell_size
        col = event.x // self.cell_size

        # Obtiene la isla en la posición clicada
        isla = self.tablero.obtener_isla(row, col)

        if isla:
            # Si ya hay una isla seleccionada, intenta conectar las dos islas
            if self.selected_isla:
                if isla != self.selected_isla:
                    try:
                        # Intenta agregar el puente
                        self.tablero.agregar_puente(self.selected_isla, isla)

                        # Si el puente se agregó correctamente, reinicia la selección
                        self.selected_isla = None
                    except ValueError as e:
                        # Muestra el mensaje de error pero no actualizar la grilla
                        messagebox.showerror("Error de Conexión", f"No se puede conectar las islas: {e}")
                        # Mantiene la isla seleccionada para otro intento
                        self.selected_isla = None
                        return
            else:
                # Selecciona la primera isla
                self.selected_isla = isla
                print(f"Isla seleccionada: {self.selected_isla}")
        else:
            # Si no se hizo click en una isla, deseleccionar la isla actual
            self.selected_isla = None

        # Redibuja la grilla solo si el movimiento es válido
        self.dibujar_grilla()

        # Verifica si se ha ganado el juego
        if self.tablero.verificar_ganador():
            messagebox.showinfo("¡Victoria!", f"Felicidades {self.jugador.nombre}, ¡has ganado el juego!")
            self.root.quit()


    def iniciar_interfaz(self):
        self.root.mainloop()
