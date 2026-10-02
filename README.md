# Laboratorio Python AWS S3

*Tutoria S3 - Laboratorio 3.1 (AWS Academy)*

Script en Python (boto3) para practicar operaciones basicas de S3: probar conexion,
crear/listar/eliminar buckets, subir, listar, descargar y eliminar objetos.

## Historias de usuario y criterios de aceptacion

Las estimaciones son una primera ronda de Planning Poker con escala Fibonacci
(`1, 2, 3, 5, 8, 13`). Son puntos relativos, no horas, y deben recalibrarse con el equipo.
Estimacion inicial del alcance: **42 puntos**.

### Acceso y buckets

**US-01 · Verificar acceso a AWS (2 puntos)**

Como estudiante, quiero probar la conexion con AWS para confirmar que mis credenciales del
laboratorio funcionan.

- Con credenciales validas del perfil `default`, la prueba obtiene la identidad mediante STS y lista los buckets.
- Si AWS devuelve un error de cliente, se informa el fallo de conexion.

**US-02 · Consultar buckets (2 puntos)**

Como estudiante, quiero listar los buckets de mi cuenta para conocer los recursos disponibles.

- La lista muestra el nombre y la fecha de creacion de cada bucket.
- Si no hay buckets, el programa indica que la lista esta vacia.

**US-03 · Crear un bucket (3 puntos)**

Como estudiante, quiero crear un bucket con un nombre unico para almacenar mis objetos.

- Puedo proporcionar un nombre o aceptar uno sugerido; el nombre enviado incluye un sufijo unico.
- El programa informa si AWS crea el bucket o devuelve un error.

**US-04 · Seleccionar el bucket de trabajo (2 puntos)**

Como estudiante, quiero seleccionar un bucket existente para dirigir a el las operaciones
siguientes.

- El nombre introducido queda como bucket actual y aparece en el menu.
- Las operaciones que requieren bucket se detienen con un aviso si no hay uno seleccionado.

### Objetos

**US-05 · Subir un archivo (3 puntos)**

Como estudiante, quiero subir un archivo local al bucket actual y asignarle una key de S3.

- El programa solicita una ruta local; si el archivo existe, permite indicar la key y realiza la subida.
- Si la ruta no existe, informa el error y permite reintentar; una entrada vacia cancela la subida.

**US-06 · Listar objetos (2 puntos)**

Como estudiante, quiero ver las keys y tamanos de los objetos de mi bucket actual.

- Para un bucket con objetos, se muestra cada key y su tamano en bytes.
- Para un bucket vacio, se informa que no contiene objetos.

**US-07 · Descargar un objeto (5 puntos)**

Como estudiante, quiero descargar un objeto existente a una ruta local para consultar su contenido.

- El programa verifica que la key exista antes de pedir el destino; si no existe, informa y permite reintentar.
- Si el destino requiere carpetas que no existen, las crea; al completar la descarga informa la ruta resultante.
- Una entrada vacia cancela el flujo y los errores de AWS o del sistema de archivos se informan.

**US-08 · Eliminar un objeto (2 puntos)**

Como estudiante, quiero eliminar una key del bucket actual para retirar un objeto que ya no necesito.

- La key indicada se envia a S3 para su eliminacion y el programa informa el resultado.
- Si AWS rechaza la solicitud, se muestra el error.

**US-09 · Vaciar un bucket (8 puntos)**

Como estudiante, quiero eliminar todos los objetos del bucket actual antes de borrarlo.

- La operacion solo continua si escribo exactamente el nombre del bucket; cualquier otro valor cancela el vaciado.
- Se recorren todas las paginas de resultados y se informa el total eliminado y los errores por objeto.
- Si el versionado esta habilitado o suspendido, tambien se eliminan las versiones y los marcadores de eliminacion.

**US-10 · Eliminar un bucket vacio (2 puntos)**

Como estudiante, quiero eliminar el bucket actual cuando ya no lo necesito.

- El programa solicita a AWS eliminar el bucket actual e informa el resultado.
- Si el bucket no esta vacio o AWS rechaza la solicitud, se informa el error sin ocultarlo.

### Politicas de bucket

**US-11 · Aplicar una politica desde JSON (8 puntos)**

Como estudiante, quiero elegir y aplicar una politica JSON a un bucket para practicar el
control de acceso en S3.

- Se enumeran los archivos `politica*.json` de las subcarpetas; la seleccion invalida o un JSON mal formado se informa sin llamar a S3.
- Antes de aplicar, se reemplaza `NOMBRE-DE-TU-BUCKET` en los recursos y se advierte que la politica puede permitir lectura publica.
- Solo con confirmacion `s` se llama a `put_bucket_policy`; otra respuesta cancela la operacion.

**US-12 · Eliminar la politica de un bucket (3 puntos)**

Como estudiante, quiero retirar la politica actual de un bucket y confirmar la accion antes
de cambiar su acceso.

- Solo con confirmacion `s` se llama a `delete_bucket_policy` para el bucket indicado.
- Si cancelo o AWS rechaza la solicitud, el programa informa la cancelacion o el error.

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
9. **Eliminar todos los objetos del bucket actual**: pide escribir el nombre exacto del
   bucket para confirmar el vaciado, incluidas las versiones y marcadores de eliminacion si
   el versionado esta habilitado o suspendido.
10. **Eliminar bucket actual**: borra el bucket; AWS requiere que este vacio primero.
0. **Salir**.

## Gestion de politicas de bucket

Ejecuta el segundo script desde la carpeta del proyecto:

```powershell
python s3_policies.py
```

Elige una de las operaciones del menu e introduce el nombre de un bucket existente:

1. **Aplicar politica desde JSON**: selecciona por numero una plantilla encontrada en `politicas/`.
   El script sustituye `NOMBRE-DE-TU-BUCKET` por el bucket indicado y solo la aplica si confirmas con `s`.
2. **Eliminar politica del bucket**: elimina la politica completa del bucket si confirmas con `s`.

Cualquier otra respuesta a la confirmacion cancela la operacion. Al aplicar una politica,
la politica actual del bucket se reemplaza. Las plantillas incluidas conceden lectura publica
(`s3:GetObject`):

- `politica_solo_carpetas.json`: lectura publica de objetos bajo `pagina-web/`.
- `politica_solor_carpetas_archivos.json`: lectura publica bajo `pagina-web/`, `docs/` y para `index.html`.
- `politicapublica.json`: lectura publica de todos los objetos del bucket.

Revisa el contenido y el alcance de la plantilla antes de confirmar. No la uses en buckets
con datos sensibles. AWS puede rechazar una politica publica si la configuracion de bloqueo
de acceso publico del bucket o de la cuenta lo impide; el script informa el error.

## Arquitectura

El diagrama de componentes Draw.io y la arquitectura del proyecto se encuentran en
[arquitectura/arquitectura_s3.drawio](arquitectura/arquitectura_s3.drawio). Abre el archivo
con Draw.io y selecciona la pestaña **Componentes**. El mismo archivo incluye también las
vistas **Despliegue UML**, **Actividad operaciones s3** y **Actividad políticas**.

## Archivos del proyecto

- `s3_operations.py` : script principal con el menu interactivo.
- `s3_policies.py` : aplica o elimina la politica de un bucket mediante plantillas JSON.
- `requirements.txt` : dependencias (`boto3`).
- `archivo_prueba.txt` : archivo de ejemplo para probar la subida.
- `politicas/` : plantillas JSON de politicas para buckets S3.
- `arquitectura/arquitectura_s3.drawio` : diagramas de arquitectura del proyecto.

## Sprint Backlog

Propuesta de trabajo basada en las estimaciones de las historias. Cada tarea queda pendiente
hasta que el equipo la tome; los puntos pertenecen a las historias, no son horas por tarea.
La division supone 21 puntos por sprint y debe ajustarse a la capacidad y velocidad reales.

### Sprint 1 · Acceso y operaciones de objetos (21 puntos)

**Objetivo:** permitir conectarse a AWS y administrar buckets y objetos de forma habitual.

- [ ] **SB1-01 · US-01:** comprobar la identidad con STS usando el perfil `default` e informar errores de conexion.
- [ ] **SB1-02 · US-02:** listar buckets con nombre y fecha de creacion, incluyendo el estado sin resultados.
- [ ] **SB1-03 · US-03:** generar nombres sugeridos unicos y crear buckets en la region configurada; mostrar errores de AWS.
- [ ] **SB1-04 · US-04:** mantener el bucket seleccionado en el menu y bloquear las opciones dependientes si no hay uno seleccionado.
- [ ] **SB1-05 · US-05:** validar la ruta local, solicitar la key, subir el archivo y permitir reintentar o cancelar.
- [ ] **SB1-06 · US-06:** listar keys y tamanos, e informar cuando el bucket esta vacio.
- [ ] **SB1-07 · US-07:** verificar la key, solicitar destino, crear carpetas locales y gestionar errores de descarga.
- [ ] **SB1-08 · US-08:** eliminar una key del bucket actual e informar el resultado o error de S3.

### Sprint 2 · Limpieza segura y politicas (21 puntos)

**Objetivo:** completar la eliminacion segura de recursos y la administracion de politicas de bucket.

- [ ] **SB2-01 · US-09:** confirmar el nombre exacto del bucket, recorrer paginas de objetos/versiones, eliminar marcadores y reportar errores y conteo.
- [ ] **SB2-02 · US-10:** eliminar el bucket actual y presentar el error si no esta vacio o AWS rechaza la solicitud.
- [ ] **SB2-03 · US-11:** descubrir y validar politicas JSON, sustituir el marcador del bucket, advertir sobre acceso publico y aplicar solo con confirmacion.
- [ ] **SB2-04 · US-12:** solicitar confirmacion antes de eliminar la politica y gestionar cancelaciones y errores de AWS.

### Definicion de terminado

- [ ] Los criterios de aceptacion de la historia asociada se cumplen.
- [ ] Los casos de exito, cancelacion y error se prueban sin depender de credenciales reales de AWS.
- [ ] La guia del menu y las instrucciones de uso reflejan el comportamiento implementado.
