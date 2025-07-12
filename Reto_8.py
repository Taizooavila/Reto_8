class MenuItem:
    def __init__(self, nombre:str, precio:float):
        self.nombre = nombre
        self.precio = precio

class Bebidas(MenuItem):
    def __init__(self, nombre, precio, tamaño:int = 0):
        super().__init__(nombre, precio)
        if tamaño == 1:
            self.precio += 2000
            self.nombre += " Mediano"
        elif tamaño ==2:
            self.nombre += " Grande"
            self.precio += 3000
        #Aumenta el precio de la bebida dependiendo del tamaño

class Entradas(MenuItem):
    def __init__(self, nombre, precio, personas:int):
        super().__init__(nombre, precio)
        self.precio *= personas

class PlatoFuerte(MenuItem):
    def __init__(self, nombre, precio, sopa:bool = True):
        super().__init__(nombre, precio)
        if sopa:
            self.precio += 8000
            self.nombre += " con sopa"
        #Aumenta el precio del plato fuerte si se pide con sopa

class Postre(MenuItem):
    def __init__(self, nombre, precio, porcion:int):
        super().__init__(nombre, precio)
        self.precio *= porcion
        if porcion >= 10:
            self.precio *= 0.75
        #si hay 10 porciones del mismo postre, 25% de descuento

class Orden:
    def __init__(self):
        self.orden = []
        #crea una lista vacia
    def ordenar(self, item:"MenuItem"):
        self.orden.append(item)
        #Añade el item a la lista
    def precio_total(self):
        total = 0
        print("Orden:")
        for i in self.orden:
            total += i.precio
            print(f"{i.nombre}\t\t\t${i.precio}")
        print(f"Precio total:\t\t\t${total}")
        #Itera por la lista, imprime los productos con su precio y su suma
    def calcular_descuentos(self):
        a = 0
        b = 0
        for i in self.orden:
            if isinstance(i, Bebidas):
                a += 1
                if a == 2:
                    i.precio *= 0.5
                    print(f"Descuento 50% en: {i.nombre}")
                    #Descuento del 50% a la segunda bebida
            if isinstance(i, PlatoFuerte):
                b += 1
                if b == 10:
                    i.precio = 0
                    print(f"{i.nombre} es el décimo plato fuerte, por lo que la casa invita!")
                    #Un plato fuerte gratis si se ordenaron 10 o mas
    def __iter__(self):
        return OrdenIterable(self.orden)

class OrdenIterable:

    def __init__(self, orden):
        self.orden = orden
        self.indice = 0
    def __iter__(self):
        return self
    def __next__(self):
        if self.indice < len(self.orden):
            evento = self.orden[self.indice]
            self.indice += 1
            return evento
        else:
            raise StopIteration

if __name__ == "__main__":
    menu = dict(Jugo = 5000, Batido = 8000, Limonada = 7000,
                Empanada = 5000, Palitos_de_queso = 5000,
                Pollo = 18000, Costillas = 21000, Pasta = 17000,
                Cheesecake = 8000, Helado = 5000)
    productos = []
    for i in menu:
        productos.append(MenuItem(i, menu[i]))
        #Crea la lista de MenuItems que hay en el menu

    pedido = input("""
    Bienvenido.
    Para elegir su comida, ingrese los índices de los productos
    separados por espacios. Para elegir las demás opciones,
    digite el número separado de un punto.
    (Ejemplo: Limonada mediana -> 2.1):
    
    Bebidas:
        0. Jugo
        1. Malteada
        2. Limonada
        Tamaño:
            0. Pequeño
            1. Mediano
            2. Grande

    Entradas:
        3. Empanadas
        4. Palitos de queso
        Porciones:
            # Porciones
    
    Plato principal:
        5. Pollo
        6. Costillas
        7. Pasta
        Sopa:
            0. No
            1. Si
    
    Postre:
        8. Cheesecake
        9. Helado
        Porciones:
            # Porciones
    
    """)
        
    pedido = pedido.split()
    orden = Orden()
    for i in pedido:
        i = list(map(int, i.split(".")))
        if i[0] <= 2:
            orden.ordenar(Bebidas(productos[i[0]].nombre, productos[i[0]].precio, i[1]))
        elif i[0] <= 4:
            orden.ordenar(Entradas(productos[i[0]].nombre, productos[i[0]].precio, i[1]))
        elif i[0] <= 7:
            orden.ordenar(PlatoFuerte(productos[i[0]].nombre, productos[i[0]].precio, (True if i[1]==1 else False)))
        elif i[0] <= 9:
            orden.ordenar(Postre(productos[i[0]].nombre, productos[i[0]].precio, i[1]))
        #A partir del input recibido, crea las instancias de los productos ordenados

    orden.calcular_descuentos()
    orden.precio_total()