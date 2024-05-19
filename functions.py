import os
import glob
import json
import pickle
from tqdm import tqdm

import re
from pypdf import PdfReader
from langchain_openai import ChatOpenAI
from kor.extraction import create_extraction_chain



def bill_cleaner(path):
    """
    Función que devuelve el texto procesado de una factura.

    Input:
        - path(str): Ruta de la factura.pdf

    Output:
        - texto_limpio (str)

    """

    factura = PdfReader(path)

    texto_factura = ""
    for pagina in factura.pages:
        texto_factura += pagina.extract_text()

    # Elimino saltos de linea
    texto_limpio = re.sub(r"\s+", " ", texto_factura).strip()

    # Elimino puntos
    texto_limpio = re.sub(r"\.+", "", texto_limpio)

    # Elimino espacios multiples
    texto_limpio = re.sub(r"\s+", " ", texto_limpio)

    return texto_limpio


def inicializar():

    data_path = input("Introduce la ruta donde se encuentran las facturas de las que deseas extraer información: ")

    model = input("Selecciona OPENAI(1) o LLaMa(2): ")

    if model == "1":
        nombre = input("Introduce el nombre asociado a la API key de OPENAI que aparece en tu archivo .ENV: ")
        api_key = os.getenv(nombre)
    if model == "2":
        nombre = input("Introduce el nombre asociado a la API key de GROQ que aparece en tu archivo .ENV: ")
        api_key = os.getenv(nombre)

    return data_path, model, api_key


def information_extractor(path, model, api_key):
    """
    Función que extrae la información requerida de una factura de luz guardandola en formato JSON.

    Input:
        - path(str): Ruta donde se alojan las factura en formato PDF
        - api_key(str): La api key de OPENAI o GROQ

    Output:
        - archivo JSON con la información requerida de la factura.

    """

    # Defino el LLM:
    if model == "1":
        llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0,
            openai_api_key=api_key)

    if model == "2":
        llm = ChatGroq(model="llama3-70b-8192",
                       groq_api_key=api_key)

        # Cargo el esquema:
    with open("utils/schema.pkl", "rb") as f:
        schema = pickle.load(f)

    # Cargo cadena
    chain = create_extraction_chain(llm, schema, encoder_or_encoder_class="json")

    # Busco las facturas en PDF en la ruta proporcionada:

    facturas = glob.glob(os.path.join(path, "*.pdf"))

    # Obtengo la información requerida de cada factura:

    if not os.path.exists("extracted_information"):
        os.makedirs("extracted_information")

    barra_progreso = tqdm(total=len(facturas), desc="Progreso", unit="archivo")

    for path_factura in facturas:
        file_name = path_factura.split("\\")[1].split(".")[0] + ".json"
        information_path = "extracted_information\\"

        ###################################### Limpieza texto ######################################

        texto_factura = bill_cleaner(path_factura)

        ###################################### Extracción de información requerida ######################################

        informacion_factura = chain.invoke(input=texto_factura)["text"]["data"]["informacion_factura"][0]

        ###################################### Guardo en formato JSON la informacion ######################################
        with open(information_path + file_name, "w") as json_file:
            json.dump(informacion_factura, json_file, indent=4)

        barra_progreso.update(1)

    barra_progreso.close()