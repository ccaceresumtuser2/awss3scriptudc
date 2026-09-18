"""
Operaciones basicas de S3 con boto3 - Tutoria "programacion en la nube aws"
Laboratorio 3.1 (AWS Academy). Usa las credenciales temporales de ~/.aws/credentials
(perfil "default") generadas por el laboratorio.
"""

import os
import sys
import uuid

import boto3
from botocore.exceptions import ClientError

REGION = "us-east-1"

session = boto3.Session(profile_name="default", region_name=REGION)
s3 = session.client("s3")


def nombre_bucket_sugerido():
    return f"tutoria-s3-lab31-{uuid.uuid4().hex[:8]}"


def probar_conexion():
    try:
        identidad = session.client("sts").get_caller_identity()
        print("Conexion OK.")
        print(f" - Account: {identidad['Account']}")
        print(f" - ARN: {identidad['Arn']}")
        listar_buckets()
    except ClientError as e:
        print(f"Error de conexion: {e}")


def crear_bucket(nombre):
    try:
        if REGION == "us-east-1":
            s3.create_bucket(Bucket=nombre)
        else:
            s3.create_bucket(
                Bucket=nombre,
                CreateBucketConfiguration={"LocationConstraint": REGION},
            )
        print(f"Bucket '{nombre}' creado.")
    except ClientError as e:
        print(f"Error al crear el bucket: {e}")


def listar_buckets():
    resp = s3.list_buckets()
    buckets = resp.get("Buckets", [])
    if not buckets:
        print("No hay buckets.")
        return
    print("Buckets disponibles:")
    for b in buckets:
        print(f" - {b['Name']} (creado: {b['CreationDate']})")


def subir_archivo(bucket, ruta_local, key):
    try:
        s3.upload_file(ruta_local, bucket, key)
        print(f"Archivo '{ruta_local}' subido como '{key}' en '{bucket}'.")
    except ClientError as e:
        print(f"Error al subir el archivo: {e}")
    except FileNotFoundError:
        print(f"No se encontro el archivo local: {ruta_local}")


def listar_objetos(bucket):
    try:
        resp = s3.list_objects_v2(Bucket=bucket)
    except ClientError as e:
        print(f"Error al listar objetos: {e}")
        return
    objetos = resp.get("Contents", [])
    if not objetos:
        print(f"El bucket '{bucket}' esta vacio.")
        return
    print(f"Objetos en '{bucket}':")
    for obj in objetos:
        print(f" - {obj['Key']} ({obj['Size']} bytes)")


def objeto_existe(bucket, key):
    try:
        s3.head_object(Bucket=bucket, Key=key)
        return True
    except ClientError as e:
        codigo = e.response.get("Error", {}).get("Code")
        if codigo in ("404", "NoSuchKey", "NotFound"):
            return False
        raise


def descargar_archivo(bucket, key, ruta_local):
    if ruta_local.endswith(("/", "\\")) or os.path.isdir(ruta_local):
        ruta_local = os.path.join(ruta_local, os.path.basename(key))
    carpeta = os.path.dirname(ruta_local)
    if carpeta:
        try:
            os.makedirs(carpeta, exist_ok=True)
        except OSError as e:
            print(f"Error al crear la carpeta de destino: {e}")
            return False
    try:
        s3.download_file(bucket, key, ruta_local)
        print(f"Objeto '{key}' descargado en '{ruta_local}'.")
        return True
    except ClientError as e:
        print(f"Error al descargar el archivo: {e}")
        return False
    except OSError as e:
        print(f"Error al escribir el archivo local: {e}")
        return False


def eliminar_objeto(bucket, key):
    try:
        s3.delete_object(Bucket=bucket, Key=key)
        print(f"Objeto '{key}' eliminado de '{bucket}'.")
    except ClientError as e:
        print(f"Error al eliminar el objeto: {e}")


def eliminar_bucket(bucket):
    try:
        s3.delete_bucket(Bucket=bucket)
        print(f"Bucket '{bucket}' eliminado.")
    except ClientError as e:
        print(f"Error al eliminar el bucket (debe estar vacio primero): {e}")


def menu():
    bucket_actual = None
    while True:
        print(f"{'='*40}")
        print("\n--- Operaciones basicas S3 (Lab 3.1) ---")
        print(f"Bucket actual: {bucket_actual or '(ninguno)'}")
        print("1. Probar conexion")
        print("2. Crear bucket")
        print("3. Listar buckets")
        print("4. Seleccionar bucket actual")
        print("5. Subir archivo")
        print("6. Listar objetos del bucket actual")
        print("7. Descargar objeto")
        print("8. Eliminar objeto")
        print("9. Eliminar bucket actual")
        print("0. Salir")
        opcion = input("Elige una opcion: ").strip()
        print(f"{'='*40}")
        if opcion == "1":
            probar_conexion()
        elif opcion == "2":
            nombre = input(
                f"Nombre del nuevo bucket ]: "
            ).strip() or nombre_bucket_sugerido()
            bucket_actual = f"{nombre}-{uuid.uuid4().hex[:8]}"
            crear_bucket(bucket_actual)
        elif opcion == "3":
            listar_buckets()
        elif opcion == "4":
            bucket_actual = input("Nombre del bucket a usar: ").strip()
        elif opcion == "5":
            if not bucket_actual:
                print("Primero selecciona o crea un bucket.")
                continue
            ruta_local = ""
            while True:
                ruta_local = input(
                    "Ruta del archivo local a subir (vacio para cancelar): "
                ).strip()
                if not ruta_local:
                    print("Subida cancelada.")
                    break
                if os.path.isfile(ruta_local):
                    key = input(
                        "Nombre (key) en S3 [igual al archivo]: "
                    ).strip() or ruta_local
                    subir_archivo(bucket_actual, ruta_local, key)
                    break
                print(f"El archivo '{ruta_local}' no existe en local. Intenta de nuevo.")
        elif opcion == "6":
            if not bucket_actual:
                print("Primero selecciona o crea un bucket.")
                continue
            listar_objetos(bucket_actual)
        elif opcion == "7":
            if not bucket_actual:
                print("Primero selecciona o crea un bucket.")
                continue
            while True:
                key = input(
                    "Key del objeto a descargar (vacio para cancelar): "
                ).strip()
                if not key:
                    print("Descarga cancelada.")
                    break
                try:
                    existe = objeto_existe(bucket_actual, key)
                except ClientError as e:
                    print(f"Error al verificar el objeto: {e}")
                    continue
                if not existe:
                    print(
                        f"La key '{key}' no existe en el bucket "
                        f"'{bucket_actual}'. Intenta de nuevo."
                    )
                    continue
                while True:
                    ruta_local = input(
                        "Ruta local de destino (vacio para cancelar): "
                    ).strip()
                    if not ruta_local:
                        print("Descarga cancelada.")
                        break
                    if descargar_archivo(bucket_actual, key, ruta_local):
                        break
                break
        elif opcion == "8":
            if not bucket_actual:
                print("Primero selecciona o crea un bucket.")
                continue
            key = input("Key del objeto a eliminar: ").strip()
            eliminar_objeto(bucket_actual, key)
        elif opcion == "9":
            if not bucket_actual:
                print("Primero selecciona o crea un bucket.")
                continue
            eliminar_bucket(bucket_actual)
            bucket_actual = None
        elif opcion == "0":
            print("Hasta luego.")
            sys.exit(0)
        else:
            print("Opcion invalida.")


if __name__ == "__main__":
    menu()
