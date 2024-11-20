class Documento:
    def __init__(self, id_documento, contenido):
        self.id_documento = id_documento
        self.contenido = contenido

    def obtener_contenido(self):
        return self.contenido

    def modificar_contenido(self, nuevo_contenido):
        self.contenido = nuevo_contenido

    def __str__(self):
        return f"ID: {self.id_documento}, Contenido: {self.contenido}"


class Coleccion:
    def __init__(self, nombre):
        self.nombre = nombre
        self.documentos = {}

    def agregar_documento(self, documento):
        self.documentos[documento.id_documento] = documento

    def eliminar_documento(self, id_documento):
        if id_documento in self.documentos:
            del self.documentos[id_documento]
        else:
            raise ValueError(f"Documento con ID {id_documento} no encontrado.")

    def buscar_documento(self, id_documento):
        return self.documentos.get(id_documento, None)

    def listar_documentos(self):
        return list(self.documentos.values())

    def importar_csv(self):
        import csv
        ruta_csv = "datos_personales (2).CSV"
        try:
            with open(ruta_csv, mode='r', encoding='utf-8') as archivo_csv:
                lector_csv = csv.DictReader(archivo_csv)
                for i, fila in enumerate(lector_csv):
                    doc_id = i
                    contenido = {k: v for k, v in fila.items()}
                    documento = Documento(doc_id, contenido)
                    self.agregar_documento(documento)
            print(f"Se importaron los documentos desde '{ruta_csv}'.")
        except FileNotFoundError:
            print(f"Error: el archivo {ruta_csv} no existe.")
        except Exception as e:
            print(f"Error al importar CSV: {e}")

    def agregar_desde_lineas(self, lineas):
        for i, linea in enumerate(lineas):
            contenido = {f"campo_{j}": valor for j, valor in enumerate(linea.split(","))}
            doc_id = i
            documento = Documento(doc_id, contenido)
            self.agregar_documento(documento)


class Database:
    def __init__(self, nombre_base):
        self.nombre_base = nombre_base
        self.colecciones = {}

    def create_collection(self, nombre_coleccion):
        if nombre_coleccion not in self.colecciones:
            self.colecciones[nombre_coleccion] = Coleccion(nombre_coleccion)
        else:
            raise ValueError(f"La colección '{nombre_coleccion}' ya existe.")

    def get_collection(self, nombre_coleccion):
        return self.colecciones.get(nombre_coleccion, None)

    def list_collections(self):
        return list(self.colecciones.keys())


def convert(linea):
    
    campos = linea.split(",")
    contenido = {f"campo_{i}": campo for i, campo in enumerate(campos)}
    return contenido


def str2Doc(linea, id_documento):
    
    contenido = convert(linea)
    return Documento(id_documento, contenido)


def mostrar_menu():
    print("\n--- Base de Datos Documental ---")
    print("1. Crear colección")
    print("2. Importar CSV a colección")
    print("3. Consultar documento en colección")
    print("4. Eliminar documento de colección")
    print("5. Listar todos los documentos en colección")
    print("6. Agregar documentos desde líneas")
    print("7. Salir")
    return input("Seleccione una opción: ")


def main():
    db = Database("MiBaseDeDatos")
    while True:
        try:
            opcion = mostrar_menu()

            if opcion == "1":
                nombre_coleccion = input("Ingrese el nombre de la colección: ")
                try:
                    db.create_collection(nombre_coleccion)
                    print(f"Colección '{nombre_coleccion}' creada.")
                except ValueError as e:
                    print(f"Error: {e}")

            elif opcion == "2":
                nombre_coleccion = input("Ingrese el nombre de la colección: ")
                coleccion = db.get_collection(nombre_coleccion)
                if coleccion:
                    coleccion.importar_csv()
                else:
                    print(f"Colección '{nombre_coleccion}' no encontrada.")

            elif opcion == "3":
                nombre_coleccion = input("Ingrese el nombre de la colección: ")
                try:
                    doc_id = int(input("Ingrese el ID del documento (número): "))
                    coleccion = db.get_collection(nombre_coleccion)
                    if coleccion:
                        documento = coleccion.buscar_documento(doc_id)
                        if documento:
                            print("Documento encontrado:")
                            print(documento.obtener_contenido())
                        else:
                            print("Documento no encontrado.")
                    else:
                        print(f"Colección '{nombre_coleccion}' no encontrada.")
                except ValueError:
                    print("Error: El ID del documento debe ser un número entero.")

            elif opcion == "4":
                nombre_coleccion = input("Ingrese el nombre de la colección: ")
                try:
                    doc_id = int(input("Ingrese el ID del documento a eliminar (número): "))
                    coleccion = db.get_collection(nombre_coleccion)
                    if coleccion:
                        coleccion.eliminar_documento(doc_id)
                        print(f"Documento con ID '{doc_id}' eliminado de la colección '{nombre_coleccion}'.")
                    else:
                        print(f"Colección '{nombre_coleccion}' no encontrada.")
                except ValueError:
                    print("Error: El ID del documento debe ser un número entero.")
                except ValueError as e:
                    print(f"Error: {e}")

            elif opcion == "5":
                nombre_coleccion = input("Ingrese el nombre de la colección: ")
                coleccion = db.get_collection(nombre_coleccion)
                if coleccion:
                    documentos = coleccion.listar_documentos()
                    print(f"Documentos en la colección '{nombre_coleccion}':")
                    for documento in documentos:
                        print(documento)
                else:
                    print(f"Colección '{nombre_coleccion}' no encontrada.")

            elif opcion == "6":
                nombre_coleccion = input("Ingrese el nombre de la colección: ")
                coleccion = db.get_collection(nombre_coleccion)
                if coleccion:
                    lineas = input("Ingrese las líneas separadas por ';': ").split(";")
                    coleccion.agregar_desde_lineas(lineas)
                    print("Documentos agregados desde líneas.")
                else:
                    print(f"Colección '{nombre_coleccion}' no encontrada.")

            elif opcion == "7":
                print("Saliendo del programa...")
                break
        except ValueError as e:
            print(f"Error inesperado: {e}")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
