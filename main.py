# Importo paquetes necesarios:
from dotenv import load_dotenv

# Importo las funciones:
from functions import inicializar, information_extractor

load_dotenv()

# Inicializo variables:
data_path, model, api_key = inicializar()

# Comienzo extracción:
information_extractor(data_path, model, api_key)

