class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre

    def agregar_puente(self, tablero, isla1, isla2):
        try:
            tablero.agregar_puente(isla1, isla2)
            print(f"Agregó un puente entre las islas ({isla1.x}, {isla1.y}) y ({isla2.x}, {isla2.y})\n")
        except ValueError as e:
            print(f"Movimiento inválido: {e}\n")

    def quitar_puente(self, tablero, isla1, isla2):
        try:
            tablero.quitar_puente(isla1, isla2)
            print(f"Quitó un puente entre las islas ({isla1.x}, {isla1.y}) y ({isla2.x}, {isla2.y})\n")
        except ValueError as e:
            print(f"Movimiento inválido: {e}\n")