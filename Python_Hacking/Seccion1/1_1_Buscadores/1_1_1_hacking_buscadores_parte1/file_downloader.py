import os
import requests

class FileDownloader:
    def __init__(self, directorio_destino):
        self.directorio = directorio_destino
        self.crear_directorio()

    def crear_directorio(self):
        if not os.path.exists(self.directorio):
            os.makedirs(self.directorio)

    def descargar_archivo(self, url):
        nombre_archivo = url.split('/')[-1]
        try:
            respuesta = requests.get(url)
            #nombre_archivo = url.split('/')[-1]
            ruta_completa = os.path.join(self.directorio, nombre_archivo)
            # Guardamos el archivo en disco
            with open(ruta_completa, "wb") as archivo:
                archivo.write(respuesta.content)
            print(f"Archivo {nombre_archivo} descargado correctamente: {ruta_completa}")
        except Exception as e:
            print(f"Error al descargar el archivo {nombre_archivo}: {e}")

    def filtrar_descargar_archivos(self, urls, tipos_archivos=["all"]):
        if tipos_archivos == ["all"]:
            for url in urls:
                self.descargar_archivo(url)
        else:
            for url in urls:
                if any(url.endswith(f".{tipo}") for tipo in tipos_archivos):
                    self.descargar_archivo(url)