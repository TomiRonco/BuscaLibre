import sqlite3

class Libreria:

    #De cada libro se quiere saber ID, ISBN, Título, Autor, Género, Precio, FechaUltimoPrecio y CantDisponible.
    #ISBN declararlo como Único e irrepetible. ID es una clave primaria y autoincremental

    def __init__(self):
        self.conexion = Conexiones()
        self.conexion.abrirConexion()
        self.conexion.miCursor.execute("DROP TABLE IF EXISTS LIBROS")
        self.conexion.miCursor.execute("CREATE TABLE LIBROS (id_libro INTEGER PRIMARY KEY,ISBN INTEGER ,titulo VARCHAR(30), autor VARCHAR(30),genero VARCHAR(40) ,precio FLOAT NOT NULL, cantidadDisponibles INTEGER NOT NULL,FechaUltimoPrecio VARCHAR(10), UNIQUE(ISBN,id_libro))")
        self.conexion.miConexion.commit()
    
    def agregar_libro(self, titulo, autor, precio, cantidadDisponibles, id_libro, ISBN, genero, FechaUltimoPrecio):
        try:
            self.conexion.miCursor.execute("INSERT INTO LIBROS (titulo, autor, precio, cantidadDisponibles, id_libro, ISBN, genero, FechaUltimoPrecio) VALUES (?, ?, ?, ?, ? , ? , ? , ?)", (titulo, autor, precio, cantidadDisponibles, id_libro, ISBN, genero, FechaUltimoPrecio))
            self.conexion.miConexion.commit()
            print("Libro agregado exitosamente")
        except:
            print("Error al agregar un libro")
    
    def modificar_libro(self, id_libro , precio_nuevo):
        try:
            self.conexion.miCursor.execute("UPDATE LIBROS SET precio = ? WHERE id_libro = ? ", (precio_nuevo, id_libro))
            self.conexion.miConexion.commit()
            print("Libro modificado correctamente")
        except:
            print("Error al modificar un libro")
    
    def cerrar_libreria(self):
        self.conexion.cerrarConexion()

class Conexiones:
    def abrirConexion(self):
        self.miConexion = sqlite3.connect("Libreria.db")
        self.miCursor = self.miConexion.cursor()
        
    def cerrarConexion(self):
        self.miConexion.close()  


libreria = Libreria()

while True:
    print("Menu de opciones Libreria")
    print("1- Agregar libro")
    print("2- Modificar libro")
    print("3- Borrar un libro")
    print("4- Cargar disponibilidad")
    print("5- Listado de libros")
    print("6- Ventas")
    print("7- Actualizar precios")
    print("8- Mostrar todos los registros anteriores a una fecha en específico de la tabla libros.")
    print("0- Salir del menú")
   
    
    opcion = int(input("Por favor ingrese un número: "))
    
    if opcion == 1:
        titulo = input("Por favor ingrese el título del libro: ")
        autor = input("Por favor ingrese el autor del libro: ")
        precio = float(input("Por favor ingrese el precio del libro: "))
        cantidadDisponibles = int(input("Por favor ingrese la cantidad de unidades disponibles: "))
        id_libro = input("Por favor ingrese el ID del libro: ")
        ISBN = input("Por favor ingrese el ISBN del libro: ")
        genero = input("Por favor ingrese el género del libro: ")
        FechaUltimoPrecio = input("Por favor ingrese la ultima fecha que se actualizó el precio del libro: ")
        libreria.agregar_libro(titulo, autor, precio, cantidadDisponibles, id_libro, ISBN, genero, FechaUltimoPrecio)
    elif opcion == 2:
        id_libro = input("Por favor ingrese el ID del libro a modificar: ")
        precio_nuevo = float(input("Por favor ingrese el nuevo precio del libro: "))
        libreria.modificar_libro(id_libro, precio_nuevo)
    elif opcion == 0:
        libreria.cerrar_libreria()
        break