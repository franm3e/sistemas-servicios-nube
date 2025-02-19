import boto3
import logging
import datetime
 
logger = logging.getLogger()
logger.setLevel(logging.INFO)
 
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('s3events')  # Nombre de tu tabla
 
def lambda_handler(event, context):
    try:
        for record in event['Records']:
            logger.info(f"Evento recibido: {event}")
            record = event['Records'][0]  # Obtiene el primer registro del evento
            bucket_name = record['s3']['bucket']['name']  # Extrae el nombre del bucket donde se encuentra el archivo
            logger.info(f"Bucket detectado: {bucket_name}")
            
            s3_client = boto3.client('s3')
            # Listar los objetos dentro del bucket detectado
            objects = s3_client.list_objects_v2(Bucket=bucket_name)
            # Comprobar si el bucket contiene archivos, si no, se retorna un error
            if 'Contents' not in objects:
                logger.error("El bucket está vacío.")  
                return {
                    'statusCode': 400, 
                    'body': "El bucket no contiene archivos." 
                }
            # Ordenar los objetos por la fecha de modificación (de más reciente a más antigua)
            sorted_objects = sorted(objects['Contents'], key=lambda obj: obj['LastModified'], reverse=True)
            # Obtener el objeto más reciente
            latest_object = sorted_objects[0]
            file_name = latest_object['Key']  # Nombre del archivo más reciente
            # Log del archivo más reciente detectado
            logger.info(f"Archivo más reciente detectado: {file_name}")
    
            # Extrae el nombre del archivo del evento
            imageName = record['s3']['object']['key']
            # Obtiene el timestamp actual en formato ISO 8601
            timestamp = datetime.datetime.utcnow().isoformat()

            # Crear un cliente de Rekognition para analizar el archivo con el servicio de reconocimiento de imágenes
            rekognition_client = boto3.client('rekognition')
            # Llamar al servicio de Rekognition para analizar la imagen en busca de celebridades
            response = rekognition_client.recognize_celebrities(
                Image={
                    'S3Object': {
                        'Bucket': bucket_name, 
                        'Name': file_name
                    }
                }
            )
            # Log de la respuesta obtenida desde Rekognition
            logger.info(f"Respuesta de Rekognition: {response}")
            # Extraer los nombres de las celebridades detectadas (si las hay)
            celebrities = response.get('CelebrityFaces', [])  # Devuelve una lista de celebridades detectadas
            celebrity_names = [celeb['Name'] for celeb in celebrities]
            # Preparar el mensaje de resultado basado en si se encontraron celebridades o no
            if len(celebrity_names):
                result_message = f"Última celebridad reconocida: {', '.join(celebrity_names)}"
                # Inserta los datos en DynamoDB
                table.put_item(
                    Item={
                        'id': f"{imageName}{timestamp}",     # Nombre del archivo como ID
                        'timestamp': timestamp,     # Timestamp de subida
                        'fileName': imageName,
                        'url': f"https://{bucket_name}.s3.amazonaws.com/{imageName}",
                        'uploadDate': timestamp,
                        'celebrities': ', '.join(celebrity_names)
                    }
                )

            else:
                result_message = "No se reconocieron celebridades en la imagen más reciente."
            logger.info(result_message)     
            return {
                'statusCode': 200,
                'body': {
                    'message': result_message,  # Mensaje de resultado
                    'celebrities': celebrity_names  # Lista de celebridades detectadas
                }
            }
    except Exception as e:
        logger.error(f"Error al procesar el evento: {str(e)}")  
        return {
            'statusCode': 500, 
            'body': f"Error: {str(e)}"  
        }