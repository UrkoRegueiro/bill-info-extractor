# Extractor de información de facturas eléctricas

## Tecnologías usadas

**Lenguaje:** Python.

**Librerias:** regex, pandas, pypdf, kor, langchain, openai

------------

<h2>
  
Para visualizar la versión detallada del presente proyecto véase [bill-info-extractor](https://github.com/UrkoRegueiro/bill-info-extractor/blob/master/info_extraction.ipynb)

<h2>
  
------------

## 1. **Introducción**

El presente proyecto tratará de extraer información relevante de faturas de luz. Para ello se presentan diferentes modelos de facturas en formato PDF que, mediante el método empleado de extracción de información, esta se guardará en archivos con formato JSON.

El método empleado para la extracción de información ha sido la utilización de un LLM junto con la librería Kor. Esta librería nos permite crear un esquema(véase Apéndice 1.) para especificar que información debe ser extraida, generando un prompt que mandará a nuestro LLM. Los archivos PDF se han leido con la librería Pypdf y el texto se ha limpiado bajo criterio personal, pudiendo mejorarse.

Este método puede implementarse utilizando LLM's open source como LLaMa 3, haciendo un finetuning(véase Apéndice 2.) con los datos de entrenamiento y aplicando el mismo procedimiento. No se ha realizado en este caso por carecer de procesamiento suficiente, por lo que se ha optado por el modelo 'gpt-3.5-turbo' de OPENAI.

Se han comparado los resultados obtenidos entre el modelo 'gpt-3.5-turbo' y el modelo LLaMa 3-70b(a traves de GROQ), obteniendo prácticamente identicos resultados.
