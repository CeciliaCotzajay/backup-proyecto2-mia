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
        # RECORRER LAS LISTAS
        if(singleton.objL.list_pathsReports):
            for i1, i2 in zip(singleton.objL.list_pathsReports, singleton.objL.list_nameReports):
                # Sube el archivo al bucket
                s3.upload_file(i1, self.bucket_name, i2)
                print(f"Se ha subido {i1} a {self.bucket_name}")
                print("*****************************************************************************")
        else:
            print("error no hay paths de reportes guardados")
            print("*****************************************************************************")
