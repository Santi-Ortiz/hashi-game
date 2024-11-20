import sys
sys.setrecursionlimit(10000)

class Jugador:
    def __init__(self, nombre, es_sintetico):
        self.nombre = nombre
        self.es_sintetico = es_sintetico
        self.memo = set()

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

        def conectar_isla_mayor_conexiones():
            isla_mayor_conexiones = max(tablero.islas,
                                        key=lambda isla: isla.conexiones_necesarias - isla.conexiones_actuales)

            if isla_mayor_conexiones.conexiones_actuales < isla_mayor_conexiones.conexiones_necesarias:
                vecinos_validos = [
                    otra_isla for otra_isla in tablero.islas
                    if isla_mayor_conexiones != otra_isla and tablero.validar_conexion(isla_mayor_conexiones, otra_isla)
                ]

                conexiones_por_vecino = isla_mayor_conexiones.conexiones_necesarias // len(vecinos_validos)

                for vecino in vecinos_validos:
                    while (isla_mayor_conexiones.conexiones_actuales < isla_mayor_conexiones.conexiones_necesarias and
                           vecino.conexiones_actuales < vecino.conexiones_necesarias and
                           tablero.conexiones.get(tuple(
                               sorted([(isla_mayor_conexiones.x, isla_mayor_conexiones.y), (vecino.x, vecino.y)])),
                                                  0) < 2):
                        self.agregar_puente(tablero, isla_mayor_conexiones, vecino)
                        if tablero.verificar_ganador():
                            return True
            return False

        def completar_islas_obvias():
            for isla in tablero.islas:
                if isla.conexiones_actuales < isla.conexiones_necesarias:
                    vecinos_validos = [
                        otra_isla for otra_isla in tablero.islas
                        if isla != otra_isla and tablero.validar_conexion(isla, otra_isla)
                    ]
                    if len(vecinos_validos) == 1:  # Solo un vecino posible
                        vecino = vecinos_validos[0]
                        while isla.conexiones_actuales < isla.conexiones_necesarias:
                            self.agregar_puente(tablero, isla, vecino)
                            if tablero.verificar_ganador():
                                return True
            return False

        def distribuir_conexiones():
            for isla in tablero.islas:
                if isla.conexiones_actuales < isla.conexiones_necesarias:
                    vecinos_validos = [
                        otra_isla for otra_isla in tablero.islas
                        if isla != otra_isla and tablero.validar_conexion(isla, otra_isla)
                    ]
                    for vecino in vecinos_validos:
                        if vecino.conexiones_actuales < vecino.conexiones_necesarias:
                            self.agregar_puente(tablero, isla, vecino)
                            if tablero.verificar_ganador():
                                return True
            return False

        def estan_todas_conectadas():
            visitadas = set()

            def dfs(isla):
                if isla in visitadas:
                    return
                visitadas.add(isla)
                for otra_isla in tablero.islas:
                    if isla != otra_isla and tablero.validar_conexion(isla, otra_isla):
                        dfs(otra_isla)

            dfs(tablero.islas[0])
            return len(visitadas) == len(tablero.islas)

        def backtrack(depth, max_depth):
            if depth > max_depth:
                return False

            state = tuple((isla.x, isla.y, isla.conexiones_actuales) for isla in tablero.islas)
            if state in self.memo:
                return False

            for isla1 in tablero.islas:
                if isla1.conexiones_actuales < isla1.conexiones_necesarias:
                    for isla2 in tablero.islas:
                        if isla1 != isla2 and isla2.conexiones_actuales < isla2.conexiones_necesarias and tablero.validar_conexion(
                                isla1, isla2):
                            self.agregar_puente(tablero, isla1, isla2)

                            if tablero.verificar_ganador() and estan_todas_conectadas():
                                return True
                            if backtrack(depth + 1, max_depth):
                                return True
                            self.quitar_puente(tablero, isla1, isla2)

            self.memo.add(state)
            return False

        conectar_isla_mayor_conexiones()

        if completar_islas_obvias():
            print(f"¡{self.nombre} ha completado el tablero!")
            return

        if distribuir_conexiones():
            print(f"¡{self.nombre} ha completado el tablero!")
            return

        max_depth = min(1000, len(tablero.islas) * 10)
        if backtrack(0, max_depth):
            print(f"¡{self.nombre} ha completado el tablero!")
        else:
            print(f"{self.nombre} no encontró una solución para el tablero.")

        for isla in tablero.islas:
            if isla.conexiones_actuales != isla.conexiones_necesarias:
                print(
                    f"{self.nombre} no completó todas las conexiones necesarias para la isla en ({isla.x}, {isla.y}).")
                return

        print(f"¡{self.nombre} ha completado todas las conexiones necesarias para el tablero!")