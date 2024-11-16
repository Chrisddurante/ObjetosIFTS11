# documento.py
class Documento:
    def __init__(self, id_documento, contenido):
        self.id_documento = id_documento
        self.contenido = contenido

    def obtener_contenido(self):
        return self.contenido

    def modificar_contenido(self, nuevo_contenido):
        self.contenido = nuevo_contenido


# coleccion.py
class Coleccion:
    def __init__(self, nombre):
        self.nombre = nombre
        self.ids = 0
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

    def importar_csv(self, ruta_csv):
        import csv
        with open(ruta_csv, mode='r') as archivo_csv:
            lector_csv = csv.DictReader(archivo_csv)
            for fila in lector_csv:
                doc_id = fila['id']  # Suponiendo que el CSV tiene una columna 'id'
                contenido = {k: v for k, v in fila.items() if k != 'id'}
                documento = Documento(doc_id, contenido)
                self.agregar_documento(documento)


# database.py
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


# main.py
from database import Database

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
                ruta_csv = input("Ingrese la ruta del archivo CSV: ")
                coleccion.importar_csv(ruta_csv)
                print(f"Documentos importados desde '{ruta_csv}' a la colección '{nombre_coleccion}'.")
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
            coleccion = db.get_collection
