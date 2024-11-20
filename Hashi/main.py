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
        es_sintetico = False
        nombre = simpledialog.askstring("Nombre", "Ingrese su nombre:")
        jugador = Jugador(nombre, es_sintetico)
        tablero = Tablero(ruta_archivo)
        interfaz = Interfaz(tablero, jugador)
        interfaz.iniciar_interfaz()

    elif tipo_jugador == "s":
        es_sintetico = True
        nombre = "Jugador Sintético"
        jugador = Jugador(nombre, es_sintetico)
        tablero = Tablero(ruta_archivo)
        interfaz = Interfaz(tablero, jugador)

        # Jugar automáticamente
        while not tablero.verificar_ganador():
            jugador.jugar_auto(tablero)
            interfaz.dibujar_grilla()
            if not tablero.verificar_ganador():
                break

        if tablero.verificar_ganador():
            messagebox.showinfo("¡Victoria!", f"Felicidades, ¡has ganado el juego!")
        else:
            messagebox.showinfo("Fin del juego", "No se encontró una solución.")
if __name__ == "__main__":
    main()