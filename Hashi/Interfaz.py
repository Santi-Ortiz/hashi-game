class Interfaz:
    def __init__(self, tablero):
        self.tablero = tablero

    def mostrar_tablero(self):
        self.tablero.mostrar_tablero()

    def pedir_coordenadas(self):
        try:
            x1, y1 = map(int, input("\nIngrese las coordenadas de la primera isla (x1 y1): ").split())
            x2, y2 = map(int, input("Ingrese las coordenadas de la segunda isla (x2 y2): ").split())
            return (x1, y1), (x2, y2)
        except ValueError:
            print("\nCoordenadas inválidas. Intente de nuevo.\n")
            return self.pedir_coordenadas()

    def pedir_accion(self):
        accion = input("\n¿Desea agregar o quitar un puente? (a/q): ").strip().lower()
        if accion not in ["a", "q"]:
            print("Acción inválida. Intente de nuevo.\n")
            return self.pedir_accion()
        return accion

    def jugar(self, jugador):
        while True:
            self.mostrar_tablero()
            accion = self.pedir_accion()
            (x1, y1), (x2, y2) = self.pedir_coordenadas()
            isla1 = self.tablero.obtener_isla(x1, y1)
            isla2 = self.tablero.obtener_isla(x2, y2)
            if isla1 and isla2:
                try:
                    if accion == "a":
                        jugador.agregar_puente(self.tablero, isla1, isla2)
                    elif accion == "q":
                        jugador.quitar_puente(self.tablero, isla1, isla2)
                    if self.tablero.verificar_ganador():
                        self.mostrar_tablero()
                        print(f"\n¡Felicidades {jugador.nombre}, has ganado!\n")
                        break
                except ValueError as e:
                    print(f"Movimiento inválido: {e}\n")
            else:
                print("Una o ambas coordenadas no corresponden a una isla. Intente de nuevo.\n")
