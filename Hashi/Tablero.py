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

    def mostrar_tablero(self):
        for fila in self.tablero_expandido:
            fila_str = ""
            for celda in fila:
                if celda == '||':
                    fila_str += celda
                else:
                    fila_str += f"{celda} "
            print(fila_str)

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

        if isla1.x == isla2.x: 
            for j in range(min(isla1.y, isla2.y) + 1, max(isla1.y, isla2.y)):
                if self.tablero[isla1.x][j] != 0:
                    return False
        elif isla1.y == isla2.y:  
            for i in range(min(isla1.x, isla2.x) + 1, max(isla1.x, isla2.x)):
                if self.tablero[i][isla1.y] != 0:
                    return False

        return True
    
    def agregar_puente(self, isla1, isla2):
        if not self.validar_conexion(isla1, isla2):
            raise ValueError("No se puede conectar las islas debido a una obstrucción o alineación incorrecta.")
        
        par_islas = tuple(sorted([(isla1.x, isla1.y), (isla2.x, isla2.y)]))
        
        if self.conexiones.get(par_islas, 0) >= 2:
            raise ValueError("No se pueden agregar más de dos conexiones entre dos islas.")
        
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

    def quitar_puente(self, isla1, isla2):
        if not self.validar_conexion(isla1, isla2):
            raise ValueError("No hay puente entre las islas para quitar.")
        
        par_islas = tuple(sorted([(isla1.x, isla1.y), (isla2.x, isla2.y)]))
        
        if self.conexiones.get(par_islas, 0) == 0:
            raise ValueError("No hay conexiones actuales entre las islas para quitar.")
        
        self.conexiones[par_islas] -= 1
        
        isla1.quitar_conexion()
        isla2.quitar_conexion()
        
        if isla1.x == isla2.x: 
            for j in range(min(isla1.y, isla2.y) * 2 + 1, max(isla1.y, isla2.y) * 2, 2):
                if self.tablero_expandido[isla1.x * 2][j] == '=':
                    self.tablero_expandido[isla1.x * 2][j] = '-'
                elif self.tablero_expandido[isla1.x * 2][j] == '-':
                    self.tablero_expandido[isla1.x * 2][j] = ' '
        elif isla1.y == isla2.y: 
            for i in range(min(isla1.x, isla2.x) * 2 + 1, max(isla1.x, isla2.x) * 2, 2):
                if self.tablero_expandido[i][isla1.y * 2] == '||':
                    self.tablero_expandido[i][isla1.y * 2] = '|'
                elif self.tablero_expandido[i][isla1.y * 2] == '|':
                    self.tablero_expandido[i][isla1.y * 2] = ' '

    def verificar_ganador(self):
        return all(isla.esta_completa() for isla in self.islas)