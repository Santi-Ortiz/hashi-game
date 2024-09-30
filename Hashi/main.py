from Tablero import Tablero
from Interfaz import Interfaz
from Jugador import Jugador

def main():
    ruta_archivo = 'tablero1.txt'
    tablero = Tablero(ruta_archivo)
    interfaz = Interfaz(tablero)
    jugador = Jugador("Humano")

    interfaz.jugar(jugador)

if __name__ == "__main__":
    main()