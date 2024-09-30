class Isla:
    def __init__(self, x, y, conexiones_necesarias):
        self.x = x
        self.y = y
        self.conexiones_necesarias = conexiones_necesarias
        self.conexiones_actuales = 0

    def agregar_conexion(self):
        if self.conexiones_actuales < self.conexiones_necesarias:
            self.conexiones_actuales += 1
        else:
            raise ValueError("Número máximo de conexiones alcanzado")
        
    def quitar_conexion(self):
        if self.conexiones_actuales > 0:
            self.conexiones_actuales -= 1
        else:
            raise ValueError("No hay conexiones para quitar")

    def esta_completa(self):
        return self.conexiones_actuales == self.conexiones_necesarias