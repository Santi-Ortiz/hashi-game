import tkinter as tk

class Interfaz:
    def __init__(self, tablero, celda_tam = 50) :
        self.tablero = tablero # Tablero de la partida
        self.celda_tam = celda_tam # Tamaño de las celdas   
        self.isla_seleccionada = None # Isla seleccionada por el usuario

        # Se inicializa la ventana principal (root) de la interfaz (UI)
        self.root = tk.Tk()

        # Creación de un Canvas para dibujar tablero, islas y puentes
        self.canvas = tk.Canvas(self.root, width=self.tablero.n * self.celda_tam, height=self.tablero.n * self.celda_tam)
        self.canvas.pack()

        # Se dibuja el tablero
        self.dibujar_tablero()

        # Se asocian los eventos de click del mouse
        self.canvas.bind("<Button-1>", self.click)


    def dibujar_tablero(self):

        # Dibujar el tablero incluyendo celdas e islas
        for x in range(self.tablero.n):
            for y in range(self.tablero.n):
                # Dibujo de las celdas
                x1, y1 = y * self.celda_tam, x * self.celda_tam
                x2, y2 = x1 + self.celda_tam, y1 + self.celda_tam

                # Contorno de las celdas
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black")

    def inicializar(self):
        self.root.mainloop()

# ventana = tk.Tk()
# ventana.mainloop()
# ventana.title("Hashi")
#tablero = Tablero(5)

#interfaz = Interfaz(tablero)
#interfaz.inicializar()