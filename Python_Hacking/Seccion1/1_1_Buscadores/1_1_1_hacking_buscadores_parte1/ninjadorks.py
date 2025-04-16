
from googlesearch import GoogleSearch
from results_parser import ResultsParser
from file_downloader import FileDownloader
from ai_agent import GPT4ALL_Generator, OpenAI_Generator, AIAgent

from dotenv import load_dotenv, set_key
import os
import sys
import argparse

def env_config():
    """confugura del archivo .env"""
    api_key = input("Ingrese la clave API KEY de Google: ")
    engine_id = input("Ingrese el ID del buscador de Google: ")
    set_key(".env", "API_KEY_GOOGLE", api_key)
    set_key(".env", "SEARCH_ENGINE_ID", engine_id)
    
def openai_config():
    """Configura la API KEY de OpenAI en el fichero .env"""
    api_key = input("Ingrese el API KEY de OpenAI")
    set_key(".env", "OPENAI_API_KEY", api_key)

def main(query, configure_env, start_page, pages, lang, output_json, output_html, download, gen_dork):
    # Comprobamos existenciadel archivo .env
    env_exist = os.path.exists('.env')
    
    if not env_exist and configure_env:
        env_config()
        print("Archivo .env configurado correctamente")
        sys.exit(1)

    # Cargar las variables en el entorno
    load_dotenv()

    # Leemos las claves API
    API_KEY_GOOGLE = os.getenv('API_KEY_GOOGLE')
    SEARCH_ENGINE_ID = os.getenv('SEARCH_ENGINE_ID')

    if gen_dork:
        # Preguntamos si el usuario quiere utilizar un modelo local u OpenAI
        respuesta = ""
        while respuesta.lower() not in ("y", "yes", "no", "n"):
            respuesta = input("Quieres utilizar DeepSeek (Yes/no): ")
        
        if respuesta.lower() in ("y", "yes"):
            # Comprobamos si esta definida la API KEY de OpenAI en el fichero .env
            if not "OPENAI_API_KEY" in os.environ:
                openai_config()
                load_dotenv()
            # Generamos el Dork
            deepseek_generator = OpenAI_Generator()
            ai_agent = AIAgent(deepseek_generator)
        else:
            print("Utilizando gpt4all y ejecutando la generacion en local. Puede tardar varios minutos...")
            gpt4all_generator = GPT4ALL_Generator()
            ai_agent = AIAgent(gpt4all_generator)
        
        respuesta = ai_agent.generate_gdork(gen_dork)
        print(f'\nResultado:\n{respuesta}')
        sys.exit(1)

    # Configuración de la consulta y parámetros de búsqueda
    if not query:
        print("Ingrese una consulta con el argumento -q. Utiliza el comando -h para obtener ayuda")
        sys.exit(1)

    gsearch = GoogleSearch(API_KEY_GOOGLE, SEARCH_ENGINE_ID)
    resultados = gsearch.search(query=query, start_page=start_page, pages=pages, lang=lang)

    rparser = ResultsParser(resultados)

    # Mostrar los resultados en linea de comandos
    rparser.mostrar_pantalla()

    if output_html:
        rparser.exportar_html(output_html)
    if output_json:
        rparser.export_josn(output_json)

    if download:
        # Separar las extensiones de los archivos en una lista
        fyle_type = download.split(",")
        # Nos quedamos unicamente con las URLs de los resultados obtenidos
        urls = [resultado['link'] for resultado in resultados]
        fdownloader = FileDownloader("Descargas")
        fdownloader.filtrar_descargar_archivos(urls, fyle_type)

if __name__ == '__main__':
    # Configuración de los argumentos del programa
    parser = argparse.ArgumentParser(description='Esta herramienta busca en Google los resultados de una consulta dada.')
    parser.add_argument("-q", "--query", type=str, 
                        help="Especifica el dork que desea buscar,\nEjemplo -q 'filetype:sql \"SQL dump\" (pass|password|passwd|pwd)'")
    parser.add_argument("-c", "--configure", action="store_true", 
                        help="Inicia el proceso de configuracion del archivo .env. \nUtiliza esta opcion sin otros argumentos para configurar las claves API")
    parser.add_argument("--start-page", type=int, default=1, 
                        help="Define la pagina de inicio del buscador para obtener los resultados")
    parser.add_argument( "--pages", type=int, default=1, 
                        help="Define el numero de paginas a buscar")
    parser.add_argument("--lang", type=str, default="lang_es", 
                        help="Define el idioma del buscador. Por defecto Español")
    parser.add_argument("--json", type=str, 
                        help="Exporta los resultados a un archivo JSON en el fichero especificado")
    parser.add_argument("--html", type=str, 
                        help="Exporta los resultados a un archivo HTML en el fichero especificado")
    parser.add_argument("--download", type=str, default="all",  
                        help="Especifica las extensiones de los archivos que quieras descagar separadas por ','. \n --download 'pdf,doc,docx'")
    parser.add_argument("-gd", "--generate-dork", type=str, 
                        help="Genera un dork a partir de una descripcion proporcionada por el usuario.\nEj: --generate-dork 'Listado de usuarios y passwords en ficheros de texto")
    args = parser.parse_args()

    main(query=args.query,
         configure_env=args.configure,
         start_page=args.start_page,
         pages=args.pages,
         lang=args.lang,
         output_html=args.html,
         output_json=args.json,
         download=args.download,
         gen_dork=args.generate_dork
         )
