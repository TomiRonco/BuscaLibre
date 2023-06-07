import sqlite3


class Libreria:
    def __init__(self):
        self.conexion = Conexiones()
        self.conexion.abrirConexion()
        self.conexion.miCursor.execute("DROP TABLE IF EXISTS LIBROS")
        self.conexion.miCursor.execute('''CREATE TABLE LIBROS (
                                       ID INTEGER PRIMARY KEY,
                                       ISBN INTEGER,
                                       Titulo VARCHAR(30),
                                       Autor VARCHAR(30),
                                       Genero VARCHAR(30),
                                       Precio FLOAT NOT NULL,
                                       FechaUltimoPrecio VARCHAR(10),
                                       cantidadDisponibles INTEGER NOT NULL)
                                       ''')
        self.conexion.miConexion.commit()

    def agregar_libro(self, ID, ISBN, Titulo, Autor, Genero, Precio, FechaUltimoPrecio, cantidadDisponibles):
        try:
            self.conexion.miCursor.execute(
                "INSERT INTO LIBROS (ID, ISBN, Titulo, Autor, Genero, Precio, FechaUltimoPrecio, cantidadDisponibles) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (ID, ISBN, Titulo, Autor, Genero, Precio, FechaUltimoPrecio, cantidadDisponibles))
            self.conexion.miConexion.commit()
            print("Libro agregado exitosamente")
        except:
            print("Error al agregar un libro")

    def modificar_libro(self, ID, nuevo_Precio, nueva_Fecha):
        try:
            self.conexion.miCursor.execute(
                "UPDATE LIBROS SET precio = ? WHERE ID = ?", (nuevo_Precio, ID))
            self.conexion.miCursor.execute(
                "UPDATE LIBROS SET FechaUltimoPrecio = ? WHERE ID = ?", (nueva_Fecha, ID))
            self.conexion.miConexion.commit()
            print("Libro modificado correctamente")
        except:
            print("Error al modificar un libro")
    
    def borrar_libro(self):
        try:
            self.conexion.miCursor.execute("DELETE FROM LIBROS WHERE ID = ?", (ID,))
            self.conexion.miConexion.commit()
            print("Libro eliminado exitosamente.")
            
        except:
            print("Error al borrar el libro")
    
    def cantidad_libro(self):
        try:
            self.conexion.miCursor.execute("UPDATE LIBROS SET cantidadDisponibles = ? WHERE ID = ?", (nueva_cantidad, ID))
            self.conexion.miConexion.commit()
            print("Cantidad de libro actualizada exitosamente.")
            
        except:
            print("Error al actualizar cantidad del libro")

    def mostrar_libros(self):
        self.conexion.miCursor.execute("SELECT * FROM LIBROS")
        libros = self.conexion.miCursor.fetchall()
        print("<----- LISTADO DE LIBROS ----->")
        if libros:
            for libro in libros:
                print("ID:", libro[0],
                " | ISBN:", libro[1],
                " | Titulo:", libro[2],
                " | Autor:", libro[3],
                " | Genero:", libro[4],
                " | Precio:", libro[5],
                " | Fecha último precio:", libro[6],
                " | Cantidad disponible:", libro[7])
                print("-------------------------")
        else:
            print("No hay libros en la librería")

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
    print("<----- MENÚ DE OPCIONES DE LIBRERIA ----->")
    print("1-. Agregar libro.")
    print("2-. Modificar libro.")
    print("3-. Borrar libro.")
    print("4-. Modificar cantidad de un libro.")
    print("5-. Mostrar lista de libros.")
    print("0-. Salir del menú.")

    opcion = int(input("Por favor ingrese un número: "))

    if opcion == 1:
        ID = input("ID: ")
        ISBN = input("ISBN: ")
        Titulo = input("Titulo: ")
        Autor = input("Autor: ")
        Genero = input("Genero: ")
        Precio = float(input("Precio: $"))
        FechaUltimoPrecio = input("Fecha último precio (YYYY-MM-DD): ")
        cantidadDisponibles = int(input("Cantidad disponible: "))
        libreria.agregar_libro(ID, ISBN, Titulo, Autor, Genero, Precio, FechaUltimoPrecio, cantidadDisponibles)

    elif opcion == 2:
        ID = int(input("ID del libro a modificar: "))
        nuevo_Precio = float(input("Nuevo precio del libro: $"))
        nueva_Fecha = input("Ingrese la fecha del día de modificación: ")
        libreria.modificar_libro(ID, nuevo_Precio, nueva_Fecha)
        
    elif opcion == 3:
        ID = int(input("ID del libro a borrar: "))
        libreria.borrar_libro()

    elif opcion == 4:
        ID = int(input("ID del libro a modificar cantidad: "))
        nueva_cantidad = int(input("Ingrese la nueva cantidad del libro: "))
        libreria.cantidad_libro()
        
    elif opcion == 5:
        libreria.mostrar_libros()
        
    elif opcion == 0:
        libreria.cerrar_libreria()
        break
    
    """ VALIDACIONES DE ID Y PREGUNTA DE SI QUIERE MODIFICAR """