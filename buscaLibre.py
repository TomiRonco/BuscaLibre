import sqlite3


class Libreria:
    def __init__(self):
        self.conexion = Conexiones()
        self.conexion.abrirConexion()
        self.conexion.miCursor.execute("DROP TABLE IF EXISTS LIBROS")
        self.conexion.miCursor.execute('''CREATE TABLE LIBROS (
                                       ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                       ISBN INTEGER UNIQUE,
                                       Titulo VARCHAR(30),
                                       Autor VARCHAR(30),
                                       Genero VARCHAR(30),
                                       Precio FLOAT NOT NULL,
                                       FechaUltimoPrecio TEXT,
                                       cantidadDisponibles INTEGER NOT NULL)
                                       ''')
        self.conexion.miCursor.execute("DROP TABLE IF EXISTS VENTAS")
        self.conexion.miCursor.execute('''CREATE TABLE VENTAS (
                                       ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                       LibroID INTEGER,
                                       Cantidad INTERGER,
                                       FechaVenta TEXT)
                                       ''')
        self.conexion.miCursor.execute("DROP TABLE IF EXISTS HISTORICO_LIBROS")
        self.conexion.miCursor.execute('''CREATE TABLE HISTORICO_LIBROS (
                                       ID INTEGER,
                                       ISBN INTEGER,
                                       Titulo VARCHAR(30),
                                       Autor VARCHAR(30),
                                       Genero VARCHAR(30),
                                       Precio FLOAT NOT NULL,
                                       FechaUltimoPrecio TEXT,
                                       cantidadDisponibles INTEGER NOT NULL)
                                       ''')
        self.conexion.miConexion.commit()

    def agregar_libro(self, ISBN, Titulo, Autor, Genero, Precio, FechaUltimoPrecio, cantidadDisponibles):
        try:
            self.conexion.miCursor.execute(
                "INSERT INTO LIBROS ( ISBN, Titulo, Autor, Genero, Precio, FechaUltimoPrecio, cantidadDisponibles) VALUES (?, ?, ?, ?, ?, ?, ?)", (ISBN, Titulo, Autor, Genero, Precio, FechaUltimoPrecio, cantidadDisponibles))
            self.conexion.miConexion.commit()
            print("Libro agregado exitosamente")
        except:
            print("Error al agregar un libro")

    def modificar_libro(self, ID, nuevo_Precio, nueva_Fecha):
        try:
            confirmacion = input("¿Desea modificar este libro? (s/n): ")
            if confirmacion.lower() == 's':
                self.conexion.miCursor.execute(
                    "UPDATE LIBROS SET precio = ? WHERE ID = ?", (nuevo_Precio, ID))
                self.conexion.miCursor.execute(
                    "UPDATE LIBROS SET FechaUltimoPrecio = ? WHERE ID = ?", (nueva_Fecha, ID))
                self.conexion.miConexion.commit()
                print("Libro modificado correctamente")
            else:
                print("No se realizaron cambios en el libro")
        except:
            print("Error al modificar un libro")

    def borrar_libro(self):
        try:
            confirmacion = input("¿Desea eliminar este libro? (s/n): ")
            if confirmacion.lower() == 's':
                self.conexion.miCursor.execute(
                    "DELETE FROM LIBROS WHERE ID = ?", (ID,))
                self.conexion.miConexion.commit()
                print("Libro eliminado exitosamente.")
            else:
                print("No se ha eliminado el libro.")
                
        except:
            print("Error al borrar el libro")

    def cantidad_libro(self, nueva_cantidad, ID):
        try:
            self.conexion.miCursor.execute(
                "UPDATE LIBROS SET cantidadDisponibles = ? WHERE ID = ?", (nueva_cantidad, ID))
            self.conexion.miConexion.commit()
            print("Cantidad de libro actualizada exitosamente.")

        except:
            print("Error al actualizar cantidad del libro")

    def mostrar_libros_id(self):
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

    def mostrar_libros_autor(self):
        self.conexion.miCursor.execute("SELECT * FROM LIBROS ORDER BY Autor")
        libros = self.conexion.miCursor.fetchall()
        print("<----- LISTADO DE LIBROS ----->")
        if libros:
            for libro in libros:
                print("Autor:", libro[3],
                      " | ID:", libro[0],
                      " | ISBN:", libro[1],
                      " | Titulo:", libro[2],
                      " | Genero:", libro[4],
                      " | Precio:", libro[5],
                      " | Fecha último precio:", libro[6],
                      " | Cantidad disponible:", libro[7])
                print("-------------------------")
        else:
            print("No hay libros en la librería")

    def mostrar_libros_titulo(self):
        self.conexion.miCursor.execute("SELECT * FROM LIBROS ORDER BY Titulo")
        libros = self.conexion.miCursor.fetchall()
        print("<----- LISTADO DE LIBROS ----->")
        if libros:
            for libro in libros:
                print("Titulo:", libro[2],
                      " | ID:", libro[0],
                      " | ISBN:", libro[1],
                      " | Autor:", libro[3],
                      " | Genero:", libro[4],
                      " | Precio:", libro[5],
                      " | Fecha último precio:", libro[6],
                      " | Cantidad disponible:", libro[7])
                print("-------------------------")
        else:
            print("No hay libros en la librería")

    def validacion(self, ID):
        self.conexion.miCursor.execute(
            "SELECT * FROM LIBROS WHERE ID = ?", (ID,))
        libro = self.conexion.miCursor.fetchone()
        if libro is not None:
            return True
        else:
            return False
        
    def realizar_venta(self, LibroID, Cantidad, FechaVenta):
        try:
            libro = self.conexion.miCursor.execute(
                "SELECT cantidadDisponibles FROM LIBROS WHERE ID = ?", (LibroID,))
            libro = self.conexion.miCursor.fetchone()
            
            if libro and libro[0] >= Cantidad:
                self.conexion.miCursor.execute(
                    "INSERT INTO VENTAS (LibroID, Cantidad, FechaVenta) VALUES (?, ?, ?)", (LibroID, Cantidad, FechaVenta)
                    )
                self.conexion.miCursor.execute(
                    "UPDATE LIBROS SET cantidadDisponibles = cantidadDisponibles - ? WHERE ID = ?", (Cantidad, LibroID)
                    )
                self.conexion.miConexion.commit()
                print("Venta realizada correctamente")
            else:
                print("No hay suficientes libros disponibles.")
        except:
            print("Error al registrar venta")
            
    def mostrar_ventas(self):
        self.conexion.miCursor.execute(
            "SELECT * FROM VENTAS"
        )
        ventas = self.conexion.miCursor.fetchall()
        print("<----- LISTADO DE VENTAS ----->")
        if ventas:
            for venta in ventas:
                print("Libro ID: ", venta[0],
                      " | Cantidad: ", venta[2],
                      " | Fecha de venta: ", venta[3])
        else:
            print("No hay ventas registradas")

    def actualizar_porcentaje(self, porcentaje, fechaPorcentaje):
        self.conexion.miCursor.execute("INSERT INTO HISTORICO_LIBROS SELECT * FROM LIBROS")

        try:
            self.conexion.miCursor.execute("SELECT * FROM LIBROS")
            resultado = self.conexion.miCursor.fetchall()

            for actualizar in resultado:
                precio = actualizar[5]
                precio = precio + (precio * (porcentaje/100))
                id = actualizar[0]
                self.conexion.miCursor.execute("UPDATE LIBROS SET Precio = ?, FechaUltimoPrecio = ? WHERE ID = ?", (round(precio, 2), fechaPorcentaje, id))
            print("Libros actualizados exitosamente.")

        except:
            print("Error al actualizar libros")


    def mostrarSegunFecha(self, fecha):
        self.conexion.miCursor.execute("SELECT * FROM LIBROS WHERE FechaUltimoPrecio <= ? ",(fecha,))
        libros = self.conexion.miCursor.fetchall()
        print("<----- LISTADO DE LIBROS ----->")
        if libros:
            for libro in libros:
                print("Titulo:", libro[2],
                      " | ID:", libro[0],
                      " | ISBN:", libro[1],
                      " | Autor:", libro[3],
                      " | Genero:", libro[4],
                      " | Precio:", libro[5],
                      " | Fecha último precio:", libro[6],
                      " | Cantidad disponible:", libro[7])
                print("-------------------------")
        else:
            print("No hay libros con fecha anterior a la especificada")


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
    print("6-. Realizar venta.")
    print("7-. Actualizar precios.")
    print("8-. Mostrar Registros.")
    print("0-. Salir del menú.")

    opcion = int(input("Por favor ingrese un número: "))

    if opcion == 1:
        ISBN = input("ISBN: ")
        Titulo = input("Titulo: ")
        Autor = input("Autor: ")
        Genero = input("Genero: ")
        Precio = float(input("Precio: $"))
        FechaUltimoPrecio = input("Fecha último precio (YYYY-MM-DD): ")
        cantidadDisponibles = int(input("Cantidad disponible: "))
        libreria.agregar_libro(ISBN, Titulo, Autor, Genero,
                               Precio, FechaUltimoPrecio, cantidadDisponibles)

    if opcion == 2:
        ID = int(input("ID del libro a modificar: "))
        if libreria.validacion(ID):
            nuevo_Precio = float(input("Nuevo precio del libro: $"))
            nueva_Fecha = input("Ingrese la fecha del día de modificación: ")
            libreria.modificar_libro(ID, nuevo_Precio, nueva_Fecha)
        else:
            print("ID inexistente")

    elif opcion == 3:
        ID = int(input("ID del libro a borrar: "))
        if libreria.validacion(ID):
            libreria.borrar_libro()
        else:
            print("ID inexistente")

    elif opcion == 4:
        ID = int(input("ID del libro a modificar cantidad: "))
        if libreria.validacion(ID):
            nueva_cantidad = int(input("Ingrese la nueva cantidad del libro: "))
            libreria.cantidad_libro(nueva_cantidad, ID)
        else:
            print("ID inexistente")
        

    elif opcion == 5:
        print("Ordenar por 1-ID")
        print("Ordenar por 2-Autor")
        print("Ordenar por 3-Titulo")
        eleccion = int(input("Seleccione una opcion: "))
        if eleccion == 1:
            libreria.mostrar_libros_id()
        elif eleccion == 2:
            libreria.mostrar_libros_autor()
        elif eleccion == 3:
            libreria.mostrar_libros_titulo()
        else:
            print("Opcion seleccionada incorrecta")

    elif opcion == 6:
        LibroID = int(input("ID del libro a vender: "))
        Cantidad = int(input("Cantidad de libros a vender: "))
        FechaVenta = input("Ingrese la fecha de venta: ")
        libreria.realizar_venta(LibroID, Cantidad, FechaVenta)
        libreria.mostrar_ventas()
        
    elif opcion == 7:
        porcentaje = int(input("Ingrese el porcentaje que aumento el dolar: "))
        fechaPorcentaje = input("Ingrese la fecha de actulizacion del precio(YYYY-MM-DD): ")
        libreria.actualizar_porcentaje(porcentaje, fechaPorcentaje)

    elif opcion == 8:
        fecha = input("Ingrese la fecha: ")
        libreria.mostrarSegunFecha(fecha)
        
    elif opcion == 0:
        libreria.cerrar_libreria()
        break

    """ VALIDACIONES DE ID Y PREGUNTA DE SI QUIERE MODIFICAR """
