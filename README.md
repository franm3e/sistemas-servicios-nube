# Proyecto Final: Caso de uso
## Desarrollo de una aplicación usando los servicios de AWS

* Máster Universitario en Ingeniería Informática
* Asignatura: SISTEMAS Y SERVICIOS EN LA NUBE
* Curso: PRIMERO
* UNIVERSIDAD DE CASTILLA-LA MANCHA
* :es:

Autores (Grupo 7):
- Rubio Barato, Cristian
- Ortega Gómez, Víctor
- Martínez Esteso, Francisco

---

# Índice

1. [Introducción](#Introducción)  
2. [Arquitectura](#Arquitectura)  
3. [Demo](#Demo)

## Introducción
Este proyecto se basa en el reconocimiento de personas famosas a través del uso de la API Amazon Rekognition.

El funcionamiento y la estructura de este proyecto consiste en tener un par de servidores HTTP junto a un balanceador de carga para evitar la sobrecarga. Estos servidores permitirán que, a través de ellos, se suban imágenes o vídeos de famosos a un bucket de Amazon S3 para que sean analizados por Amazon Rekognition.

Una vez se suba la imagen o vídeo al bucket, se lanzará un evento de creación de objeto el cuál será tratado por una función lambda que se deberá encargar de hacer uso de la API de Amazon
Rekognition para identificar al famoso que aparezca en dicha imagen o vídeo, tras esto, se devolverá el resultado al usuario.
Esta función lambda también deberá de encargarse de guardar en la base de datos de Amazon DynamoDB el nombre del archivo subido y la fecha o timestamp en la que la subida del fichero fue realizada, así como las celebridades que han sido detectadas.

## Arquitectura
<img width="925" alt="image" src="https://github.com/user-attachments/assets/b8bb5049-451f-4e14-a5a3-1d485866679a" />

Los servicios de AWS utilizados y que forman la estructura del caso de uso son:
- Amazon EC2: es un servicio que permite crear y gestionar instancias de servidores virtuales en la nube de manera escalable y flexible.
- Balanceador de carga: se trata de un componente que distribuye automáticamente el tráfico entrante entre varios servidores o instancias para garantizar un rendimiento óptimo y evitar la sobrecarga.
- Amazon S3: es un servicio de almacenamiento de objetos en buckets. Se puede usar para almacenar y recuperar cualquier cantidad de datos en cualquier momento.
- AWS Lambda: es un servicio de computación sin servidor que permite ejecutar código sin la necesidad de aprovisionar o gestionar servidores. Con este servicio puedes ejecutar código en respuesta a eventos, como cambios en los datos en el Amazon S3 bucket.
- Amazon Rekognition: se trata de un servicio basado en tecnología de Deep learning que no requiere conocimientos previos para su uso. Este servicio proporciona una API simple y fácil de usar que permite analizar imágenes o videos almacenados en un Amazon S3 bucket.
- Amazon DynamoDB: se trata de un servicio de base de datos NoSQL completamente administrado, diseñado para manejar cargas de trabajo de aplicaciones de alta demanda con baja latencia. Ofrece esquemas flexibles y un rápido rendimiento predecible y escalable.

## Demo
<img width="1750" alt="image" src="https://github.com/user-attachments/assets/40732997-6cda-40c7-ab46-67012e270bd0" />
