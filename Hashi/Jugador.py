import random

class Jugador:
    def __init__(self, nombre, es_sintetico):
        
        self.nombre = nombre
        self.es_sintetico = es_sintetico

    def agregar_puente(self, tablero, isla1, isla2):
        try:
            tablero.agregar_puente(isla1, isla2)
            print(f"{self.nombre} agregó un puente entre las islas ({isla1.x}, {isla1.y}) y ({isla2.x}, {isla2.y})\n")
        except ValueError as e:
            print(f"Movimiento inválido: {e}\n")

    def quitar_puente(self, tablero, isla1, isla2):
        try:
            tablero.quitar_puente(isla1, isla2)
            print(f"{self.nombre} quitó un puente entre las islas ({isla1.x}, {isla1.y}) y ({isla2.x}, {isla2.y})\n")
        except ValueError as e:
            print(f"Movimiento inválido: {e}\n")

    def jugar_auto(self, tablero):
        if not self.es_sintetico:
            return
        # Lógica para jugar automáticamente con jugador sintético


        
