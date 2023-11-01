import os
from analizador import analizador

class principal(object):

    def __init__(self):
        self.presentar()

    def presentar(self):
        print("********************************************")
        print("********************************************")
        print("***  MANEJO E IMPLEMENTACION DE ARCHIVOS ***")
        print("********************************************")
        print("*************** PROYECTO 1 *****************")
        print("*************** 201602659 ******************")
        print("************ CECILIA COTZAJAY **************")
        print("********************************************")
        print("********************************************")
        ter = input("--->>>>presione Cero 0 para continuar--->>>>     ")
        if ter == '0':
            self.leer()

    def leer(self):
        #os.system('clear')
        print("***************************************************************************************")
        print("***************************************************************************************")
        path_archivo_Execute = input("Esperando comando:  ")
        if(path_archivo_Execute =="salir"):
            os.system('exit')
            print("***************************************************************************************")
        else:
            cad_sin_espacios = path_archivo_Execute.replace(" ","")
            archivo_execute = cad_sin_espacios.split('-')
            if(archivo_execute[0].lower() == "execute"):
                print("comando execute".upper())
                parametros = archivo_execute[1].split('=')
                if(parametros[0] == "path"):
                    path_archivo = parametros[1]
                    print(path_archivo)
                    print("*****************************************************************************")
                    an = analizador()
                    #try:
                    with open(path_archivo) as file:
                        contenidoOriginal = file.read()
                        contenido = contenidoOriginal.lower()
                        listaInstrucciones = contenido.split('\n')
                        for a in listaInstrucciones:
                            #print("----------------")
                            print(a)
                            an.analizar(a)
                    #except:
                    #    print(">>>>Error: no existe el archivo, Path no existe..")
                    #    print("*****************************************************************************")
            #self.leer()

obj = principal()