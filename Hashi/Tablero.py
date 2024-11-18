from Isla import Isla
from collections import deque

class Tablero:
    def __init__(self, ruta_archivo):
        self.ruta_archivo = ruta_archivo
        self.tablero, self.islas = self.leer_archivo_y_crear_tablero()
        self.tablero_expandido = self.expandir_tablero()
        self.conexiones = {}

    def leer_archivo_y_crear_tablero(self):
        with open(self.ruta_archivo, 'r') as archivo:
            primera_linea = archivo.readline().strip()
            filas, columnas = map(int, primera_linea.split(','))

            tablero = []
            islas = []

            for i in range(filas):
                linea = archivo.readline().strip()
                fila = [int(celda) for celda in linea]
                tablero.append(fila)
                for j, celda in enumerate(fila):
                    if celda > 0:
                        islas.append(Isla(i, j, celda))

            return tablero, islas

    def expandir_tablero(self):
        filas_originales = len(self.tablero)
        columnas_originales = len(self.tablero[0])
        filas_expandidas = filas_originales * 2 - 1
        columnas_expandidas = columnas_originales * 2 - 1

        tablero_expandido = [[' ' for _ in range(columnas_expandidas)] for _ in range(filas_expandidas)]

        for i in range(filas_originales):
            for j in range(columnas_originales):
                tablero_expandido[i * 2][j * 2] = self.tablero[i][j]

        return tablero_expandido

    def obtener_isla(self, x, y):
        for isla in self.islas:
            if isla.x == x and isla.y == y:
                return isla
        return None

    def validar_conexion(self, isla1, isla2):
        if isla1.x == isla2.x:
            for j in range(min(isla1.y, isla2.y) * 2 + 1, max(isla1.y, isla2.y) * 2, 2):
                if self.tablero_expandido[isla1.x * 2][j] not in (' ', '-', '='):
                    return False
        elif isla1.y == isla2.y:
            for i in range(min(isla1.x, isla2.x) * 2 + 1, max(isla1.x, isla2.x) * 2, 2):
                if self.tablero_expandido[i][isla1.y * 2] not in (' ', '|', '||'):
                    return False
        else:
            return False

        return True

    def agregar_puente(self, isla1, isla2):
        par_islas = tuple(sorted([(isla1.x, isla1.y), (isla2.x, isla2.y)]))
        conexiones_actuales = self.conexiones.get(par_islas, 0)

        if conexiones_actuales >= 2:
            self.eliminar_puente(isla1, isla2)
            return

        if not self.validar_conexion(isla1, isla2):
            raise ValueError("No se puede conectar las islas debido a una obstrucción o alineación incorrecta.")

        if isla1.conexiones_actuales >= isla1.conexiones_necesarias or isla2.conexiones_actuales >= isla2.conexiones_necesarias:
            self.eliminar_puente(isla1, isla2)
            return

        if conexiones_actuales < 2:
            self.conexiones[par_islas] = self.conexiones.get(par_islas, 0) + 1
            isla1.agregar_conexion()
            isla2.agregar_conexion()

            if isla1.x == isla2.x:
                for j in range(min(isla1.y, isla2.y) * 2 + 1, max(isla1.y, isla2.y) * 2, 2):
                    if self.tablero_expandido[isla1.x * 2][j] == ' ':
                        self.tablero_expandido[isla1.x * 2][j] = '-'
                    elif self.tablero_expandido[isla1.x * 2][j] == '-':
                        self.tablero_expandido[isla1.x * 2][j] = '='
            elif isla1.y == isla2.y:
                for i in range(min(isla1.x, isla2.x) * 2 + 1, max(isla1.x, isla2.x) * 2, 2):
                    if self.tablero_expandido[i][isla1.y * 2] == ' ':
                        self.tablero_expandido[i][isla1.y * 2] = '|'
                    elif self.tablero_expandido[i][isla1.y * 2] == '|':
                        self.tablero_expandido[i][isla1.y * 2] = '||'

    def eliminar_puente(self, isla1, isla2):
        par_islas = tuple(sorted([(isla1.x, isla1.y), (isla2.x, isla2.y)]))
        conexiones_actuales = self.conexiones.get(par_islas, 0)

        if conexiones_actuales > 0:
            del self.conexiones[par_islas]

            for _ in range(conexiones_actuales):
                isla1.eliminar_conexion()
                isla2.eliminar_conexion()

            if isla1.x == isla2.x:
                for j in range(min(isla1.y, isla2.y) * 2 + 1, max(isla1.y, isla2.y) * 2, 2):
                    self.tablero_expandido[isla1.x * 2][j] = ' '
                    if self.tablero[isla1.x][j // 2] == '-':
                        self.tablero[isla1.x][j // 2] = 0
            elif isla1.y == isla2.y:
                for i in range(min(isla1.x, isla2.x) * 2 + 1, max(isla1.x, isla2.x) * 2, 2):
                    self.tablero_expandido[i][isla1.y * 2] = ' '
                    if self.tablero[i // 2][isla1.y] == '|':
                        self.tablero[i // 2][isla1.y] = 0

    def verificar_conectividad(self):
        if not self.islas:
            return False

        visitadas = set()
        cola = deque([self.islas[0]])

        while cola:
            isla = cola.popleft()
            if isla in visitadas:
                continue
            visitadas.add(isla)

            for (x1, y1), (x2, y2) in self.conexiones:
                if (isla.x, isla.y) == (x1, y1):
                    isla_vecina = self.obtener_isla(x2, y2)
                elif (isla.x, isla.y) == (x2, y2):
                    isla_vecina = self.obtener_isla(x1, y1)
                else:
                    continue

                if isla_vecina and isla_vecina not in visitadas:
                    cola.append(isla_vecina)

        return len(visitadas) == len(self.islas)

    def verificar_ganador(self):
        if not all(isla.esta_completa() for isla in self.islas):
            return False
        if not self.verificar_conectividad():
            return False
        return True

    def son_vecinos(self, isla1, isla2):
        if isla1.x == isla2.x:
            for j in range(min(isla1.y, isla2.y) + 1, max(isla1.y, isla2.y)):
                if self.tablero[isla1.x][j] != 0:
                    return False
            return True
        elif isla1.y == isla2.y:
            for i in range(min(isla1.x, isla2.x) + 1, max(isla1.x, isla2.x)):
                if self.tablero[i][isla1.y] != 0:
                    return False
            return True
        return False