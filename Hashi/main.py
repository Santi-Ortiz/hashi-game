from Tablero import Tablero
from Jugador import Jugador
from Interfaz import Interfaz
import tkinter as tk
from tkinter import simpledialog, messagebox

def main():
    root = tk.Tk()
    root.withdraw()
    
    # Pregunta si el usuario quiere un jugador humano o sintético
    tipo_jugador = simpledialog.askstring("Tipo de Jugador", "¿Desea jugar como Humano o Sintético? (h/s)").lower()

    if tipo_jugador not in ("h", "s"):
        messagebox.showinfo("Saliendo","Opción no válida. Cerrando el juego.")
        print("Opción no válida. Cerrando el juego.")
        return

    ruta_archivo = 'tablero1.txt'

    # Si el jugador es humano se comienza a jugar
    if tipo_jugador == "h":
        # Se instancian los objetos para inicializar el juego en este caso tablero, jugador e interfaz
        es_sintetico = False
        nombre = simpledialog.askstring("Nombre", "Ingrese su nombre:")
        jugador = Jugador(nombre, es_sintetico)
        tablero = Tablero(ruta_archivo)
        interfaz = Interfaz(tablero, jugador)
        interfaz.iniciar_interfaz()
    elif tipo_jugador == "s": # En cambio, si el jugador es sintético juega automáticamente
        # Se debe hacer la lógica para el jugador sintético
        print("Jugador sintético seleccionado.")

if __name__ == "__main__":
    main()