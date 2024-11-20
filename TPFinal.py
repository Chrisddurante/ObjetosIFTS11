class Documento:
    def __init__(self, id_documento, contenido):
        self.id_documento = id_documento
        self.contenido = contenido

    def obtener_contenido(self):
        return self.contenido

    def modificar_contenido(self, nuevo_contenido):
        self.contenido = nuevo_contenido

class Coleccion:
    def __init__(self, nombre):
        self.nombre = nombre
        self.documentos = {}

    def agregar_documento(self, documento):
        self.documentos[documento.id_documento] = documento

    def eliminar_documento(self, id_documento):
        if id_documento in self.documentos:
            del self.documentos[id_documento]

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
                    doc_id = str(i)  #Este doc no tiene ID, con esto se asigna uno
                    contenido = {k: v for k, v in fila.items()}
                    documento = Documento(doc_id, contenido)
                    self.agregar_documento(documento)
            print(f"Se importaron los documentos desde '{ruta_csv}'.")
        except FileNotFoundError:
            print(f"Error: el archivo {ruta_csv} no existe.")
        except Exception as e:
            print(f"Error al importar CSV: {e}")

class Database:
    def __init__(self, nombre_base):
        self.nombre_base = nombre_base
        self.colecciones = {}

    def create_collection(self, nombre_coleccion):
        if nombre_coleccion not in self.colecciones:
            self.colecciones[nombre_coleccion] = Coleccion(nombre_coleccion)

    def get_collection(self, nombre_coleccion):
        return self.colecciones.get(nombre_coleccion, None)

    def list_collections(self):
        return list(self.colecciones.keys())

def mostrar_menu():
    print("\n--- Base de Datos Documental ---")
    print("1. Crear colección")
    print("2. Importar CSV a colección")
    print("3. Consultar documento en colección")
    print("4. Eliminar documento de colección")
    print("5. Listar todos los documentos en colección")
    print("6. Salir")
    return input("Seleccione una opción: ")

def main():
    db = Database("MiBaseDeDatos")
    while True:
        opcion = mostrar_menu()
        if opcion == "1":
            nombre_coleccion = input("Ingrese el nombre de la colección: ")
            db.create_collection(nombre_coleccion)
            print(f"Colección '{nombre_coleccion}' creada.")
        elif opcion == "2":
            nombre_coleccion = input("Ingrese el nombre de la colección: ")
            coleccion = db.get_collection(nombre_coleccion)
            if coleccion:
                coleccion.importar_csv()
            else:
                print(f"Colección '{nombre_coleccion}' no encontrada.")
        elif opcion == "3":
            nombre_coleccion = input("Ingrese el nombre de la colección: ")
            doc_id = input("Ingrese el ID del documento: ")
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
        elif opcion == "4":
            nombre_coleccion = input("Ingrese el nombre de la colección: ")
            doc_id = input("Ingrese el ID del documento a eliminar: ")
            coleccion = db.get_collection(nombre_coleccion)
            if coleccion:
                coleccion.eliminar_documento(doc_id)
                print(f"Documento con ID '{doc_id}' eliminado de la colección '{nombre_coleccion}'.")
            else:
                print(f"Colección '{nombre_coleccion}' no encontrada.")
        elif opcion == "5":
            nombre_coleccion = input("Ingrese el nombre de la colección: ")
            coleccion = db.get_collection(nombre_coleccion)
            if coleccion:
                documentos = coleccion.listar_documentos()
                print(f"Documentos en la colección '{nombre_coleccion}':")
                for documento in documentos:
                    print(documento.obtener_contenido())
            else:
                print(f"Colección '{nombre_coleccion}' no encontrada.")
        elif opcion == "6":
            print("Saliendo del programa...")
            break

if __name__ == "__main__":
    main()
