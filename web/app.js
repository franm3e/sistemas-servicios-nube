// Configuración de AWS S3
const bucketName = 'reconoce-famosos';
const region = 'us-east-1';
const accessKeyId = '';
const secretAccessKey = '';
const sessionToken = '';

let LAST_ITEM = '';

AWS.config.update({
  region,
  accessKeyId,
  secretAccessKey,
  sessionToken
});

const s3 = new AWS.S3();
const dynamodb = new AWS.DynamoDB.DocumentClient();
const tableName = 's3events';

document.getElementById('uploadForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const fileInput = document.getElementById('fileInput');
  const file = fileInput.files[0];
  if (!file) {
    displayMessage('Por favor, selecciona un archivo.', 'danger');
    return;
  }

  try {
    const params = {
      Bucket: bucketName,
      Key: `${file.name}`,
      Body: file,
      ContentType: file.type
    };

    const result = await s3.upload(params).promise();

    displayMessage(`Archivo subido exitosamente. <a href="${result.Location}" target="_blank">Ver Imagen</a>`, 'success');

    // Mostrar la imagen subida en la pantalla
    showUploadedImage(result.Location);

  } catch (error) {
    console.error('Error al subir el archivo:', error);
    displayMessage('Ocurrió un error al subir el archivo.', 'danger');
  }
});

function showUploadedImage(url) {
    const imagePreview = document.getElementById('imagePreview');
    const uploadedImage = document.getElementById('uploadedImage');
    
    // Mostrar el contenedor de vista previa
    imagePreview.style.display = 'block';
  
    // Establecer la URL de la imagen
    uploadedImage.src = url;
  }

function displayMessage(message, type) {
  const responseMessage = document.getElementById('responseMessage');
  responseMessage.innerHTML = `<div class="alert alert-${type}" role="alert">${message}</div>`;
}

// Obtener la lista de famosos reconocidos
async function fetchFamousList(initial=false) {
    try {
        const params = {
            TableName: tableName,
            ScanIndexForward: false // Ordenar por fecha descendente
        };

        const data = await dynamodb.scan(params).promise();
        data.Items.sort((a, b) => new Date(b.uploadDate) - new Date(a.uploadDate));

        const tbody = document.getElementById('famousList');
        tbody.innerHTML = '';

        data.Items.forEach((item, index) => {
            if(index === 0 && initial) {
                LAST_ITEM = item.id;
            }
            const row = document.createElement('tr');
            if (!initial && index==0 && LAST_ITEM !== item.id) {
                row.className = "table-success";
            }
            row.innerHTML = `
                <td>${index + 1}</td>
                <td>${new Date(item.uploadDate).toLocaleString()}</td>
                <td>${item.fileName}</td>
                <td><a href="${item.url}" target="_blank">Ver Imagen</a></td>
                <td>${item.celebrities}</td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('Error al obtener la lista de famosos:', error);
    }
}

fetchFamousList(true);
// Cargar la lista de famosos al iniciar
setInterval(fetchFamousList, 4000);