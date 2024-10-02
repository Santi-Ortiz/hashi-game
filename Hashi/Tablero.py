from Isla import Isla

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
        filas = len(self.tablero)  # Número de filas en el tablero original
        columnas = len(self.tablero[0])  # Número de columnas en el tablero original

        if isla1.x == isla2.x:  # Conexión horizontal
            for j in range(min(isla1.y, isla2.y) * 2 + 1, max(isla1.y, isla2.y) * 2, 2):
                if self.tablero_expandido[isla1.x * 2][j] not in (' ', '-', '='):
                    return False

            for i in range(filas * 2 - 1):
                if self.tablero_expandido[i][(min(isla1.y, isla2.y) + max(isla1.y, isla2.y)) // 2 * 2] in ('|', '||'):
                    return False

        elif isla1.y == isla2.y:  # Conexión vertical
            for i in range(min(isla1.x, isla2.x) * 2 + 1, max(isla1.x, isla2.x) * 2, 2):
                if self.tablero_expandido[i][isla1.y * 2] not in (' ', '|', '||'):
                    return False

            for j in range(columnas * 2 - 1):
                if self.tablero_expandido[(min(isla1.x, isla2.x) + max(isla1.x, isla2.x)) // 2 * 2][j] in ('-', '='):
                    return False

        else:
            return False

        # Verificar que no haya islas en el camino en el tablero original
        if isla1.x == isla2.x:  # Conexión horizontal en el tablero original
            for j in range(min(isla1.y, isla2.y) + 1, max(isla1.y, isla2.y)):
                if self.tablero[isla1.x][j] != 0:
                    return False
        elif isla1.y == isla2.y:  # Conexión vertical en el tablero original
            for i in range(min(isla1.x, isla2.x) + 1, max(isla1.x, isla2.x)):
                if self.tablero[i][isla1.y] != 0:
                    return False

        return True
    
    def agregar_puente(self, isla1, isla2):
        """
        Agrega un puente entre dos islas si es una conexión válida.
        """
        # Primero, validar la conexión
        if not self.validar_conexion(isla1, isla2):
            raise ValueError("No se puede conectar las islas debido a una obstrucción o alineación incorrecta.")
        
        # Crear el par ordenado de islas para representar la conexión
        par_islas = tuple(sorted([(isla1.x, isla1.y), (isla2.x, isla2.y)]))
        
        # Verificar si ya hay dos puentes conectando estas dos islas
        if self.conexiones.get(par_islas, 0) >= 2:
            raise ValueError("No se pueden agregar más de dos conexiones entre dos islas.")

        # Verificar si alguna de las islas excede el número de conexiones permitidas
        if isla1.conexiones_actuales >= isla1.conexiones_necesarias or isla2.conexiones_actuales >= isla2.conexiones_necesarias:
            raise ValueError("Una de las islas ya alcanzó su número máximo de conexiones.")

        # Si la validación pasa, agregar el puente
        self.conexiones[par_islas] = self.conexiones.get(par_islas, 0) + 1
        
        # Actualizar el número de conexiones de cada isla
        isla1.agregar_conexion()
        isla2.agregar_conexion()
        
        # Dibujar el puente en la grilla expandida
        if isla1.x == isla2.x:  # Conexión horizontal
            for j in range(min(isla1.y, isla2.y) * 2 + 1, max(isla1.y, isla2.y) * 2, 2):
                if self.tablero_expandido[isla1.x * 2][j] == ' ':
                    self.tablero_expandido[isla1.x * 2][j] = '-'
                elif self.tablero_expandido[isla1.x * 2][j] == '-':
                    self.tablero_expandido[isla1.x * 2][j] = '='
        elif isla1.y == isla2.y:  # Conexión vertical
            for i in range(min(isla1.x, isla2.x) * 2 + 1, max(isla1.x, isla2.x) * 2, 2):
                if self.tablero_expandido[i][isla1.y * 2] == ' ':
                    self.tablero_expandido[i][isla1.y * 2] = '|'
                elif self.tablero_expandido[i][isla1.y * 2] == '|':
                    self.tablero_expandido[i][isla1.y * 2] = '||'


    def verificar_ganador(self):
        return all(isla.esta_completa() for isla in self.islas)