# Funciones Lambda para Amazon Rekognition y DynamoDB

## `lambda_function.py`
Este archivo contiene la lógica principal que se ejecutará en la función Lambda. Se lanzará con un evento de subida de fichero al bucket y se encarga de análizarlos con Amazon Rekognition y realizar las operaciones necesarias sobre DynamoDB.

## `insertDataDB.py`
Este archivo contiene únicamente la parte del código del manejo de DynamoDB que se útiliza en `lambda_function.py`. Simplemente se encuentra en el repositorio a modo de plantilla para ser utilizado.

