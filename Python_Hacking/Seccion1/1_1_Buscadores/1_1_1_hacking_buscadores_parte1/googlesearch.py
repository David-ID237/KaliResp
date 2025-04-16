import requests

class GoogleSearch:
    def __init__(self, apy_key, engine_id):
        """
        Inicializa una nueva instancia de GoogleSearch
        Permite realizar peticiones automaticas a la API de Google

        Args:
            api_key (str): Clave API de Google
            engine_id(str): Identificador del motor personalizado de Google
        """
        self.apy_key = apy_key
        self.engine_id = engine_id

    def search(self, query, start_page=1, pages=1, lang="lang_es"):
        """Realiza la busqueda automatizada en google utilizando su API"""
        final_results = []
        results_per_page = 10 # Google muestra por defecto 10 resultados por pagina
        for page in range(pages):
            # Calculamos el resultado de comienzo en cada pagina
            start_index = (start_page - 1) * results_per_page + 1 + (page * results_per_page)
            # Construcción de la URL para la API de Google Custom Search
            url = f"https://www.googleapis.com/customsearch/v1?key={self.apy_key}&cx={self.engine_id}&q={query}&start={start_index}&lr={lang}"
            response = requests.get(url)
            # Comprobamos si la respuesta es correcta
            if response.status_code == 200:
                data = response.json()
                # Recuperar la lista de resultados de la respuesta
                results = data.get("items")  # Uso de get para evitar KeyError si 'items' no existe
                cresults = self.custom_results(results)
                final_results.extend(cresults)
            else:
                print(f"Error obtenido al consultar la pagina {page}: HTTP {response.status_code}")
                break
        return final_results

    def custom_results(self, results):
        """Filtra los resultados de la query"""
        custom_results = []
        for r in results:
            cresult = {}
            cresult["title"] = r.get("title")
            cresult["description"] = r.get("snippet")
            cresult["link"] = r.get("link")
            custom_results.append(cresult)
        return custom_results