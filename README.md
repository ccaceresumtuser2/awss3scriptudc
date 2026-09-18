# Laboratorio Python AWS S3

*Tutoria S3 - Laboratorio 3.1 (AWS Academy)*

Script en Python (boto3) para practicar operaciones basicas de S3: probar conexion,
crear/listar/eliminar buckets, subir, listar, descargar y eliminar objetos.

## Que es boto3

[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) es el SDK
oficial de AWS para Python. Permite crear, configurar y administrar servicios de AWS
(como S3, EC2, DynamoDB, etc.) directamente desde codigo Python, usando las mismas
credenciales que la AWS CLI. En este proyecto se usa el cliente `boto3.client("s3")`
para llamar a las operaciones de S3 (crear bucket, subir/descargar objetos, listar,
eliminar) sin necesidad de ejecutar comandos `aws s3` manualmente.

## Requisitos previos

### 1. Instalar AWS CLI

Descarga e instala AWS CLI v2 desde:
https://awscli.amazonaws.com/AWSCLIV2.msi

Verifica la instalacion:

```powershell
aws --version
```

### 2. Instalar Python y las dependencias

```powershell
python --version
pip install -r requirements.txt
```

### 3. Configurar las credenciales del Laboratorio 3.1

1. En AWS Academy, entra al **Laboratorio 3.1** y haz clic en **Start Lab**. Espera a que el
   circulo junto a AWS quede en verde.
2. Haz clic en **AWS Details** y luego en **Show** junto a "AWS CLI".
3. Copia el bloque completo (empieza con `[default]`).
4. Crea (o edita) la carpeta y los archivos de configuracion de AWS en tu usuario de Windows:

   - `C:\Users\<tu_usuario>\.aws\config`
     ```ini
     [default]
     region=us-east-1
     output=json
     ```

   - `C:\Users\<tu_usuario>\.aws\credentials`
     ```ini
     [default]
     aws_access_key_id=PEGA_AQUI_TU_ACCESS_KEY
     aws_secret_access_key=PEGA_AQUI_TU_SECRET_KEY
     aws_session_token=PEGA_AQUI_TU_SESSION_TOKEN
     ```

   Puedes crear la carpeta con:

   ```powershell
   New-Item -ItemType Directory -Force "$env:USERPROFILE\.aws"
   ```

> Importante: las credenciales del Learner Lab son temporales y expiran cuando detienes el
> laboratorio (normalmente en unas horas). Si el script falla con `InvalidToken`,
> `ExpiredToken` o `InvalidClientTokenId`, repite este paso con una sesion activa del lab.

### 4. Crear las carpetas de trabajo local

- `C:\upload` : coloca aqui el o los archivos que quieras subir a S3.
- `C:\download` : carpeta donde el script guardara los archivos descargados (se crea
  automaticamente si no existe, pero puedes crearla tu mismo).

```powershell
New-Item -ItemType Directory -Force "C:\upload"
New-Item -ItemType Directory -Force "C:\download"
```

Copia el archivo de prueba incluido en este proyecto (`archivo_prueba.txt`) dentro de
`C:\upload`, o usa cualquier archivo propio.

## Ejecutar el script

```powershell
cd "C:\tutorias\programacion en la nube aws\tutoria s3\apps3"
python s3_operations.py
```

## Uso del menu

1. **Probar conexion**: verifica que las credenciales del lab son validas (llama a
   `sts:GetCallerIdentity` y lista los buckets existentes). Hazlo primero siempre.
2. **Crear bucket**: pide un nombre y le agrega un sufijo aleatorio para que sea unico;
   queda seleccionado como bucket actual.
3. **Listar buckets**: muestra todos los buckets de la cuenta.
4. **Seleccionar bucket actual**: para operar sobre un bucket ya existente.
5. **Subir archivo**: pide la ruta local (por ejemplo `C:\upload\archivo_prueba.txt`);
   valida que exista y vuelve a preguntar si no la encuentra, hasta que subas el archivo o
   dejes la respuesta vacia para cancelar.
6. **Listar objetos del bucket actual**: muestra los objetos (keys) subidos.
7. **Descargar objeto**: pide la key (valida que exista en el bucket) y luego la carpeta o
   ruta de destino (por ejemplo `C:\download\`); crea la carpeta si hace falta y reintenta
   hasta lograr la descarga o cancelar.
8. **Eliminar objeto**: borra una key del bucket actual.
9. **Eliminar bucket actual**: borra el bucket (debe estar vacio primero, usa la opcion 8
   para vaciarlo).
0. **Salir**.

## Archivos del proyecto

- `s3_operations.py` : script principal con el menu interactivo.
- `requirements.txt` : dependencias (`boto3`).
- `archivo_prueba.txt` : archivo de ejemplo para probar la subida.
