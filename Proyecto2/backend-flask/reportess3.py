import boto3
import os
import singleton
from dotenv import load_dotenv

class reportess3:


    # Nombre del archivo fuente .dot y archivo de salida .jpg
    #archivo_dot = "reporte.dot"
    archivo_png1 = "reporte.png"
    # Define las credenciales directamente en el código
    load_dotenv('my.env')
    aws_access_key_id = os.getenv('ACCESS_ID')
    aws_secret_access_key = os.getenv('SECRET_ID')
    bucket_name = os.getenv('BUCKET_NAME')

    # Comando para ejecutar Graphviz
    #comando = ["dot", "-Tpng", archivo_dot, "-o", archivo_png]

    # Ejecutar el comando
    #subprocess.run(comando, check=True)

    #print(f"Se ha creado el archivo {archivo_png}")

    def subir_Imagen(self):
    # Crea un cliente de S3
        s3 = boto3.client('s3', aws_access_key_id=self.aws_access_key_id, aws_secret_access_key=self.aws_secret_access_key)
        #clave = singleton.objL.list_nameReports[0]
        archivo_png = singleton.objL.list_pathsReports[0]
        nombre_archivo_png = singleton.objL.list_nameReports[0]
        # Sube el archivo al bucket
        s3.upload_file(archivo_png, self.bucket_name, 'images/' + nombre_archivo_png)

        print(f"Se ha subido {archivo_png} a {self.bucket_name}")
        print("*****************************************************************************")
