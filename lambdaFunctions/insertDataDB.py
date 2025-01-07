import boto3
import datetime

# Inicializa el cliente de DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('s3events')  # Nombre de tu tabla

def lambda_handler(event, context):
    # Procesa cada registro de evento S3
    
    if dynamodb is None:
        return {
            'statusCode': 500,
            'body': 'Error al conectar con DynamoDB'
        }
    if table is None:
        return {
            'statusCode': 500,
            'body': 'Error al obtener tabla'
        }
    
    for record in event['Records']:
        # Extrae el nombre del archivo del evento
        imageName = record['s3']['object']['key']
        
        # Obtiene el timestamp actual en formato ISO 8601
        timestamp = datetime.datetime.utcnow().isoformat()

        # Inserta los datos en DynamoDB
        table.put_item(
            Item={
                'id': imageName,     # Nombre del archivo como ID
                'timestamp': timestamp     # Timestamp de subida
            }
        )

    return {
        'statusCode': 200,
        'body': 'Evento almacenado con éxito en DynamoDB'
    }