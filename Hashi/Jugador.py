import sys
sys.setrecursionlimit(20000)  # Increase the recursion limit

MAX_DEPTH = 10000

class Jugador:
    def __init__(self, nombre, es_sintetico):
        self.nombre = nombre
        self.es_sintetico = es_sintetico
        self.memo = set()  # Memoization set to store failed states

    def agregar_puente(self, tablero, isla1, isla2):
        try:
            tablero.agregar_puente(isla1, isla2)
            print(f"{self.nombre} agregó un puente entre las islas ({isla1.x}, {isla1.y}) y ({isla2.x}, {isla2.y})\n")
        except ValueError as e:
            print(f"Movimiento inválido: {e}\n")

    def quitar_puente(self, tablero, isla1, isla2):
        try:
            tablero.eliminar_puente(isla1, isla2)
            print(f"{self.nombre} quitó un puente entre las islas ({isla1.x}, {isla1.y}) y ({isla2.x}, {isla2.y})\n")
        except ValueError as e:
            print(f"Movimiento inválido: {e}\n")

    def jugar_auto(self, tablero):
        if not self.es_sintetico:
            return

        def calcular_grados_de_libertad(isla):
            return sum(1 for otra_isla in tablero.islas if isla != otra_isla and tablero.validar_conexion(isla, otra_isla))

        def calcular_criticidad(isla):
            return isla.conexiones_necesarias - isla.conexiones_actuales

        def encontrar_islas_criticas():
            """Encuentra islas que sólo pueden completarse con una configuración específica."""
            return [isla for isla in tablero.islas if calcular_grados_de_libertad(isla) == 1]

        def backtrack(depth):
            if depth > MAX_DEPTH:  # Depth limit to prevent infinite recursion
                return False

            state = tuple((isla.x, isla.y, isla.conexiones_actuales) for isla in tablero.islas)
            if state in self.memo:
                return False

            # Ordenar islas según criticidad, grados de libertad y conexiones actuales
            islas_ordenadas = sorted(
                tablero.islas,
                key=lambda isla: (calcular_criticidad(isla), calcular_grados_de_libertad(isla)),
                reverse=True
            )

            for isla1 in islas_ordenadas:
                if isla1.conexiones_actuales < isla1.conexiones_necesarias:
                    for isla2 in islas_ordenadas:
                        if isla1 != isla2 and isla2.conexiones_actuales < isla2.conexiones_necesarias and tablero.validar_conexion(
                                isla1, isla2):
                            try:
                                self.agregar_puente(tablero, isla1, isla2)
                                if tablero.verificar_ganador():
                                    return True
                                if backtrack(depth + 1):
                                    return True
                                self.quitar_puente(tablero, isla1, isla2)
                            except ValueError:
                                continue

            self.memo.add(state)
            return False

        # Heurística inicial: completar islas críticas primero
        islas_criticas = encontrar_islas_criticas()
        for isla in islas_criticas:
            for otra_isla in tablero.islas:
                if isla != otra_isla and tablero.validar_conexion(isla, otra_isla):
                    self.agregar_puente(tablero, isla, otra_isla)
                    if tablero.verificar_ganador():
                        return

        # Si las críticas no bastan, se usa backtracking
        if backtrack(0):
            print(f"¡Has ganado el juego!")
        else:
            print("No se encontró una solución.")
