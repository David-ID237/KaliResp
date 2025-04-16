import argparse
import os
import re
from transformers import GPT2Tokenizer

class SmartSearch:
    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.files = self._read_files()

    def _read_files(self):
        """Lee el contenido de los ficheros que se encuentran en el directorio"""
        files = {}
        # Listar los ficheros del directorio
        for archivo in os.listdir(self.dir_path):
            file_path = os.path.join(self.dir_path, archivo)
            try:
                with open(file_path, "r", encoding='UTF-8') as f:
                    files[archivo] = f.read()
            except Exception as e:
                print(f"Error al leer el archivo {file_path}: {e}")
        return files

    def regex_search(self, regex):
        """Busca informacion utilizando una expresion regulares"""
        coincidencias = {}
        # Recorremos el contenido de todos los ficheros del directorio
        for file, text in self.files.items():
            respuesta = ""
            while respuesta not in ("y", "yes", "no", "n"):
                respuesta = input(f"El fichero {file} tiene una longitud de {len(text)} caracteres, quieres procesarlo? (y/n): ")
            if respuesta in ("n", "no"):
                continue
            matches = re.findall(regex, text, re.IGNORECASE)
            if not matches == []:
                coincidencias[file] = matches
        return coincidencias

    def ai_search(self, prompt, model_name='deepseek-ai/deepseek-r1', max_tokens=100):
        """Realiza una busqueda en ficheros utilizando el modelo DeepSeek"""
        coincidencias = {}
        for file, text in self.files.items():
            respuesta = ''
            pass

    def _calcular_coste(selfself, text, prompt, model_name, max_tokens):
        """Calcula el coste para un modelo"""


if __name__ == "__main__":
    # Configuramos los argumentos del programa
    parser = argparse.ArgumentParser(description='Esta herramienta busca en un directorio de archivos de texto los resultados de una expresion regular dada.')
    parser.add_argument("dir_path", type=str, help="Define el directorio donde se encuentran los archivos de texto a buscar")
    parser.add_argument("-r", "--regex", type=str,help="Define la expresion regular que desea buscar")
    # Parseamos los argumentos
    args = parser.parse_args()

    if args.regex:
        searcher = SmartSearch(args.dir_path)
        resultados = searcher.regex_search(args.regex)
        print()
        for archivo, coincidencias in resultados.items():
            print(f"Resultados en el archivo {archivo}:")
            for coincidencia in coincidencias:
                print(f"- {coincidencia}")