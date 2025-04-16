from gpt4all import GPT4All
from openai import OpenAI
from dotenv import load_dotenv
import re
import os

class GPT4ALL_Generator:
    def __init__(self, model_name='orca-mini-3b-gguf2-q4_0.gguf'):
        self.model = GPT4All(model_name)
        
    def generate(self, prompt):
        return self.model.generate(prompt)

class OpenAI_Generator:
    def __init__(self, model_name='deepseek-ai/deepseek-r1'):
        load_dotenv()
        self.model_name = model_name
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(
            base_url = "https://integrate.api.nvidia.com/v1",
            api_key = api_key
            )
    
    def generate(self, prompt):
        chat_completion = self.client.chat.completions.create(
          model = self.model_name,
          messages=[{"role":"user","content": prompt}],
          temperature=0.6,
          top_p=0.7,
          max_tokens=4096
        )

        respuesta = chat_completion.choices[0].message.content
        
        respuesta_limpia = re.sub(r'<think>.*?</think>', '', respuesta, flags=re.DOTALL)

        return respuesta_limpia

        
class AIAgent:
    def __init__(self, generator):
        self.generator = generator

    def generate_gdork(self, description):
        # Construimos el prompt
        prompt = self._build_prompt(description)
        try:
            output = self.generator.generate(prompt)
            return output
        except Exception as e:
            print(f"Error al generar el Google Dork: {e}")
            return None

    def _build_prompt(self, description):
        return f"""
        Genera un Google Dork específico basado en la descripción del usuario. Un Google Dork utiliza operadores avanzados en motores de búsqueda para encontrar información específica que es difícil de encontrar mediante una búsqueda normal. Tu tarea es convertir la descripción del usuario en un Google Dork preciso. 
        A continuación, se presentan algunos ejemplos de cómo deberías formular los Google Dorks basándote en diferentes descripciones:
        
        Descripción: Documentos PDF relacionados con la seguridad informática publicados en el último año.
        Google Dork: filetype:pdf "seguridad informática" after:2023-01-01
        
        Descripción: Presentaciones de Powerpoint sobre cambio climático disponibles en sitios .edu.
        Google Dork: site:.edu filetype:ppt "cambio climático"
        
        Descripción: Listas de correos electrónicos en archivos de texto dentro de dominios gubernamentales.
        Google Dork: site:.gov filetype:txt "email" | "correo electrónico"
        
        Ahora, basado en la siguiente descripción proporcionada por el usuario, genera el Google Dork correspondiente:
        
        Descripción: {description}
        
        Limitate a escribir el dork, solo requiero el dork, no necesito que expliques nada.
        """

if __name__ == "__main__":
    description = "Listado de usuarios y contraseñas en el contenido de ficheros de texto. utiliza variaciones de la palabra password(passwd, pwd...)"

    #ai_agent = AIAgent()
    #print(ai_agent.generate_gdork(description))
    
    load_dotenv()
    
    openai_generator = OpenAI_Generator()

    ai_agent = AIAgent(openai_generator)
    
    res = ai_agent.generate_gdork(description)
    
    print(res)
    