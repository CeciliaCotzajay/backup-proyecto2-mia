import time
import io
from estructuras import MBR, bloqueApuntadores, bloqueArchivos, bloqueCarpetas, superBloque, tablaInodos, Journal, idsRep
import singleton


class mkfs:
    INICIO_PARTITION = 0
    FIN_PARTITION = 0

    def __init__(self):
        self.ids = "" #string
        self.type = "" #string
        self.fs = ""   #string 

    def make_mkfs(self):
        singleton.objL.respuesta['mensaje']+= ">haciendo mkfs"+"\n"
        #SI EL PARAMETRO NO ESTA VACIO
        if(self.ids != ""):
            # EL FORMATEO SI O SI TIENE QUE SER FULL AUNQUE NO VENGA EN EL COMANDO
            self.type = "full"
            if(self.fs == ""):
                self.fs = "2fs"
            if(self.fs == "2fs" or self.fs == "3fs"):
                #OBTIENE EL PATH DEL DISCO POR MEDIO DEL ID, OBTIENE EL MBR
                path_Disco = self.obtener_path()
                if(path_Disco != ""):
                    mbr = self.obtener_mbr(path_Disco)
                    namePartitino = self.obtener_nombre()
                    #VERIFICAR QUE LA PARTICION SEA PRIMARIA Y OBTENER INICIO Y FINAL DE PARTICION
                    #***AVISO***: SOLO PUEDO FORMATEAR PARTICIONES PRIMARIAS
                    if(self.verificar_extendida(namePartitino,mbr)):
                        #EMPIEZA FORMATEO
                        tam_part = self.FIN_PARTITION-self.INICIO_PARTITION
                        n = 0
                        super_Bloque = superBloque()
                        tabla_inodos = tablaInodos()
                        bloque_archivo = bloqueArchivos()
                        journal = Journal()
                        cant_Inodos = 0
                        cant_Bloques = 0
                        auxfs=2
                        #APLICACION DE FORMULA PARA OBTENER N
                        n = tam_part-super_Bloque.get_size()
                        if(self.fs == "2fs"):
                            n = n//(4+tabla_inodos.get_size()+3*bloque_archivo.get_size())
                        elif(self.fs == "3fs"):
                            auxfs=3
                            n = n//(4+tabla_inodos.get_size()+3*bloque_archivo.get_size()+journal.get_size())
                        #APLICANDO FLOOR
                        cant_Inodos = n # AL USAR // SE APLICA 'FLOOR' EN PYHTON
                        cant_Bloques = cant_Inodos*3
                        tam_inodos = tabla_inodos.get_size()*cant_Inodos
                        #CREAR SUPER BLOQUE
                        super_Bloque.type = auxfs
                        super_Bloque.i_count = cant_Inodos
                        super_Bloque.b_count = cant_Bloques
                        super_Bloque.free_i = cant_Inodos
                        super_Bloque.free_b = cant_Bloques
                        super_Bloque.m_time = self.obtener_time()
                        super_Bloque.um_time = 00000000
                        super_Bloque.nm_count = 0
                        super_Bloque.magic = int(0xEF53)
                        super_Bloque.i_s = tabla_inodos.get_size()
                        super_Bloque.b_s = bloque_archivo.get_size()
                        super_Bloque.first_i = 0
                        super_Bloque.first_b = 0
                        #GUARDA EL INICIO DE BITMAP DE INODOS
                        if(self.fs == "2fs"):
                            super_Bloque.bmi_start = self.INICIO_PARTITION+super_Bloque.get_size()
                        elif(self.fs == "3fs"):
                            super_Bloque.bmi_start = self.INICIO_PARTITION+super_Bloque.get_size()+journal.get_size()
                        #------------------------------------
                        super_Bloque.bmb_start = super_Bloque.bmi_start+cant_Inodos
                        super_Bloque.i_start = super_Bloque.bmb_start+cant_Bloques
                        super_Bloque.b_start = super_Bloque.i_start+tam_inodos
                        #ESCRIBIR SUPER-BLOQUE EN EL ARCHIVO AL INICIO DE LA PARTICION
                        self.escribir_super_bloque(super_Bloque,path_Disco,self.INICIO_PARTITION)
                        self.guardar_DatosRep(self.ids,path_Disco,super_Bloque,self.INICIO_PARTITION)
                        singleton.objL.respuesta['mensaje']+= "SUPER-BLOQUE inicializado correctamente!"+"\n"
                        #ESCRIBIR BITMAP DE INODOS
                        self.escribir_bitmap(cant_Inodos,super_Bloque.bmi_start,path_Disco)
                        #ESCRIBIR BITMAP DE BLOQUES
                        self.escribir_bitmap(cant_Bloques,super_Bloque.bmb_start,path_Disco)
                        #CREAR CARPETA RAIZ
                        self.crear_directorio(super_Bloque,path_Disco,"/","/",0)
                        self.escribir_super_bloque(super_Bloque,path_Disco,self.INICIO_PARTITION)
                        #CREAR ARCHIVO USERS
                        texto_users = "1,G,root\n1,U,root,root,123\n"
                        self.crear_archivosEscritos("/users.txt",True,texto_users,28,path_Disco)  
                        #if(self.fs == "3fs"):
                        #    escribir_journal(self.INICIO_PARTITION+super_Bloque.get_size(),cantInodos,path_Disco)
                    else:
                        singleton.objL.respuesta['mensaje']+= ">>>>Error: NO se puede formatear una partición extendida.>>>>"+"\n"
                        print("*****************************************************************************")    
                else:
                    singleton.objL.respuesta['mensaje']+= ">>>>Error: La partición no esta montada>>>>"+"\n"
                    print("*****************************************************************************")            
            else:
                singleton.objL.respuesta['mensaje']+= ">>>>Error: parámetros obligatorios: id>>>>"+"\n"
                print("*****************************************************************************")
        else:
            singleton.objL.respuesta['mensaje']+= ">>>>Error: parámetros obligatorios: id>>>>"+"\n"
            print("*****************************************************************************")
    
    def obtener_path(self):
        path_en = ""
        if(singleton.objL.list_Mounts):
            for m in singleton.objL.list_Mounts:
                if(m.idmount == self.ids):
                    path_en = m.path
                    break
        return path_en
    
    def obtener_mbr(self, path_Disco):
        mbr = MBR(0,0,0,' ')
        bytes = mbr.get_bytes()
        mbr_aux = MBR(0,0,0,' ')
        with open(path_Disco, "rb+") as file:
            bytes_obtenidos = file.read(len(bytes))
            mbr_aux.set_bytes(bytes_obtenidos)
        return mbr_aux
    
    def obtener_super_bloque(self, path_Disco):
        sb = superBloque()
        bytes = sb.get_bytes()
        with open(path_Disco, "rb+") as file:
            file.seek(self.INICIO_PARTITION)
            bytes_obtenidos = file.read(len(bytes))
            sb.set_bytes(bytes_obtenidos)
        return sb
    
    def obtener_nombre(self):
        name_en = ""
        if(singleton.objL.list_Mounts):
            for m in singleton.objL.list_Mounts:
                if(m.idmount == self.ids):
                    name_en = m.name
                    break
        return name_en

    def ajustar_cadena(self,tam,cadena):
        if(len(cadena)<tam):
            dif = tam-len(cadena)
            for i in range(0,dif):
                cadena = cadena + " "
        if(len(cadena)>tam):
            new_cadena = ""
            for i in range(0,tam):
                new_cadena = new_cadena + cadena[i]
            cadena = new_cadena
        return cadena
    
    def verificar_extendida(self, nombre, mbr):
        nombre = nombre.replace("\"","")
        nombre = self.ajustar_cadena(16,nombre)
        for part in mbr.partitions:
            if(part.name == nombre):
                if(part.type == 'e'):
                    return False
                #OBTENGO DE UNA VEZ LA POSICION
                else:
                    #SI ES PRIMARIA
                    if(part.type == 'p'):
                        self.INICIO_PARTITION = part.start
                        self.FIN_PARTITION = int(part.start + part.s - 1)
                    #SI ES LOGICA
                    elif(part.type == 'l' ):
                        singleton.objL.respuesta['mensaje']+= ">>>>Aviso: Solo puedo formatear particiones primarias>>>>"+"\n"
                        print("*****************************************************************************")
                        return False
                    else:
                        return False
        return True
    
    def obtener_time(self):
        timeA = int(time.time())
        return timeA
    
    def escribir_super_bloque(self,super_Bloque,path_Disco,initPart):
        with open(path_Disco, "rb+") as file:
            bytes = super_Bloque.get_bytes()
            #print(bytes)
            #print(len(bytes))
            file.seek(initPart)
            file.write(bytes)

    def escribir_bitmap(self, cant, bm_start, path_Disco):
        with open(path_Disco, "rb+") as file:
            temp = 0
            file.seek(bm_start)
            while(temp<cant):
                file.write("0".encode('utf-8'))
                temp+=1

    def getBM_index(self, primer_BM, ultimo_BM, path_Disco):
        with open(path_Disco, "rb+") as file:
            #UBICAR EL PUNTERO AL INICIO DE BITMAP
            file.seek(primer_BM)
            aux = ''
            #VALOR DEL INDICE
            cont = 0
            flag = True
            #LEER BITMAPS HASTA LA ULTIMA POSICION ENVIADA
            while(cont < ultimo_BM):
                aux = file.read(len(aux))
                if(aux == '0'):
                    #VERIFICAR QUE EL BIT NO HAYA SIDO MARCADO
                    if(flag):
                        #UBICAR EL PUNTERO AL FINAL
                        file.seek(primer_BM+cont-1)
                        #SE ESCRIBE EL 1 EN ESA POSICION PARA MARCAR EL BITMAP
                        file.write("1".encode('utf-8'))
                        flag = False
                    else:
                        break
                cont+=1
            return cont

    def obtener_inodo(self, path_Disco, inicio):
        inodo = tablaInodos()
        bytes = inodo.get_bytes()
        inodoRet = None
        with open(path_Disco, "rb+") as file:
            file.seek(inicio)
            bytes_obtenidos = file.read(len(bytes))
            if inodoRet is None:
                inodoRet = tablaInodos()
            inodoRet.set_bytes(bytes_obtenidos)
        return inodoRet

    def escribir_inodo(self, inodo,path_Disco,inicio):
        with open(path_Disco, "rb+") as file:
            bytes = inodo.get_bytes()
            file.seek(inicio)
            file.write(bytes)

    def get_inodoInicial(self, auxsuper_bloque, indice):
        return auxsuper_bloque.i_start + (auxsuper_bloque.i_s * indice)

    def crear_inodo(self, tipo, permisos, tam):
        nuevo_inodo = tablaInodos()
        nuevo_inodo.i_uid = 1
        nuevo_inodo.i_gid = 1
        nuevo_inodo.i_s = tam
        nuevo_inodo.i_atime = self.obtener_time()
        nuevo_inodo.i_ctme = self.obtener_time()
        nuevo_inodo.i_mtime = self.obtener_time()
        nuevo_inodo.i_type = str(tipo)
        nuevo_inodo.i_perm = permisos
        return nuevo_inodo

    def agregar_bloqueApuntadores(self, inodo, indiceInodo, bl, bloque, path_Disco):
        #VERIFICAR EL ESPACIO LIBRE
        if(inodo.i_block[indiceInodo] != -1):
            libre = 0
            res = self.get_bloqueApuntadorLibre(indiceInodo, inodo, inodo.i_block[indiceInodo], path_Disco, bloque, libre)
            if(res == -1):
                singleton.objL.respuesta['mensaje']+= ">>>>Error: Espacio insuficiente, no se crearon mas carpetas o archivos.>>>>"+"\n" 
                print("*****************************************************************************")
                return False
                #return ERR_LEVEL_FULL
            #LEER EL BLOQUE DE APUNTADORES
            point = self.obtener_bloquesApuntadores(path_Disco, self.get_bloqueInicial(bloque, res))
            point.b_pointers[libre] = bloque.first_b
            #ESCRIBIR EN EL DISCO
            self.escribir_bloqueApuntadores(point, path_Disco, self.get_bloqueInicial(bloque, res))
            self.guardar_bloqueArchivos(bl, bloque, path_Disco)
        else:
            #CREAR UN NUEVO BLOQUE
            newIndice = 0
            block = self.crear_apuntadorInd(indiceInodo, newIndice, bloque, path_Disco)
            #VALIDAR LA CREACION DEL BLOQUE
            if(block == -1):
                singleton.objL.respuesta['mensaje']+= ">>>>Error: Espacio insuficiente, no se crearon mas carpetas o archivos.>>>>"+"\n" 
                print("*****************************************************************************")
                return False
                #return ERR_LEVEL_FULL
            inodo.i_block[indiceInodo] = block
            point = self.obtener_bloquesApuntadores(path_Disco, self.get_bloqueInicial(bloque, newIndice))
            #ESCRIBIR UN NUEVO BLOQUE
            self.guardar_bloqueArchivos(bl, bloque, path_Disco)
        return True

    def obtener_bloquesApuntadores(self, path_Disco, inicio):
        bloque = bloqueApuntadores()
        bytes = bloque.get_bytes()
        bloqueRet = None
        with open(path_Disco, "rb+") as file:
            file.seek(inicio)
            bytes_obtenidos = file.read(len(bytes))
            if bloqueRet is None:
                bloqueRet = bloqueApuntadores()
            bloqueRet.set_bytes(bytes_obtenidos)
        return bloqueRet

    def escribir_bloqueApuntadores(self, bloque, path_Disco, inicio):
        with open(path_Disco, "rb+") as file:
            bytes = bloque.get_bytes()
            file.seek(inicio)
            file.write(bytes)

    def obtener_BloquesCarpetas(self, path_Disco, inicio):
        bloque = bloqueCarpetas()
        bytes = bloque.get_bytes()
        bloqueRet = None
        with open(path_Disco, "rb+") as file:
            #UBICAR EL PUNTERO AL INICIO DEL BLOQUE
            file.seek(inicio)
            #LEER EL ARCHIVO
            bytes_obtenidos = file.read(len(bytes))
            if bloqueRet is None:
                bloqueRet = bloqueCarpetas()
            bloqueRet.set_bytes(bytes_obtenidos)
        return bloqueRet

    def escribir_bloquesCarpetas(self, auxsuperb, path_Disco,inicio):
        with open(path_Disco, "rb+") as file:
            bytes = auxsuperb.get_bytes()
            file.seek(inicio)
            file.write(bytes)

    def crear_bloque_carpetas(self,name,indiceDir,namePad, indicePad):
        block = bloqueCarpetas()
        name = self.ajustar_cadena(12,name)
        block.b_content[0].b_name = name
        block.b_content[0].b_inodo = indiceDir
        namePad = self.ajustar_cadena(12,namePad)
        block.b_content[1].b_name = namePad
        block.b_content[1].b_inodo = indicePad
        return block

    def crear_nodoCarpeta(self, dirPad, dirName, path_Disco, super_bloque, indiceInodoPadre, indiceBloqueActual):
        indice_libre = -1
        #TIPO DE BLOQUE = 1:ARCHIVO, 2:DIRECTORIO, 3:APUNTADOR
        type = 2
        #CREAR DIRECTORIO EN EL ESPACIO LIBRE
        res = self.get_bloqueCarpetasLibre(dirPad, path_Disco, super_bloque, indiceBloqueActual, indiceInodoPadre, indice_libre, type)
        #VALIDAR
        if(res == False):
            return False
        if(indice_libre == -1):
            singleton.objL.respuesta['mensaje']+= ">>>>Error: Espacio insuficiente, no se crearon mas carpetas o archivos.>>>>"+"\n"
            print("*****************************************************************************") 
            return False
        #ESCRIBIR UN DIRECTORIO
        newIndice = self.crear_directorio(super_bloque, path_Disco, dirName, dirPad, indiceInodoPadre)
        #VALIDAR QUE SEA UN DIRECTORIO PARA ESCRIBIRLO
        if(type == 2):
            #LEER EL BLOQUE
            bl = self.obtener_BloquesCarpetas(path_Disco, self.get_bloqueInicial(super_bloque, indiceBloqueActual))
            bl.b_content[indice_libre].b_inodo = newIndice
            dirname2 = str(dirName)
            dirname2 = self.ajustar_cadena(12,dirname2)
            bl.b_content[indice_libre].b_name = dirname2
            #ESCRIBIR EL BLOQUE DE DIRECTORIOS
            self.escribir_bloquesCarpetas(bl, path_Disco, self.get_bloqueInicial(super_bloque, indiceBloqueActual))
        elif(type == 3):
            #LEER EL BLOQUE DE APUNTADORES
            pointbl = self.obtener_bloquesApuntadores(path_Disco, self.get_bloqueInicial(super_bloque, indiceBloqueActual))
            pointbl.b_pointers[indice_libre] = newIndice
            #ESCRIBIR EL BLOQUE DE APUNTADORES
            self.escribir_bloqueApuntadores(pointbl, path_Disco, self.get_bloqueInicial(super_bloque, indiceBloqueActual))
        indiceInodoPadre = newIndice

    def buscarCarpeta(self,nameDir, path_Disco, indiceInodoActual, super_bloque):
        dirname2 = str(nameDir)
        dirname2 = self.ajustar_cadena(12,dirname2)
        #LEER EL INODO
        inodo = self.obtener_inodo(path_Disco, self.get_inodoInicial(super_bloque, indiceInodoActual))
        if(inodo.i_s == 0):
            return -1
        indexBlock = 0
        bl = bloqueCarpetas()
        for indexBlock in range(0,12):
            if(inodo.i_block[indexBlock] != -1):
                #SI ES TIPO DIRECTORIO : 0
                if(inodo.i_type == 0):
                    bl = self.obtener_BloquesCarpetas(path_Disco, self.get_bloqueInicial(super_bloque, inodo.i_block[indexBlock]))
                    """if(bl == NULL):
                        return -1
                    }"""
                    for i in range(2,4):
                        if(bl.b_content[i].b_inodo != -1):
                            if(len(bl.b_content[i].b_name) == len(dirname2)):
                                indiceInodoActual = bl.b_content[i].b_inodo
                                inodo = self.obtener_inodo(path_Disco, self.get_inodoInicial(super_bloque, indiceInodoActual))
                                if(inodo.i_s == 0):
                                    return -1
                                return inodo.i_block[0]
        for indexBlock in range(12,14):
            index = self.buscar_carpetaBloqueApuntadores(indexBlock - 11, inodo.i_block[indexBlock], indiceInodoActual, nameDir, super_bloque, path_Disco)
            """if(index != -1):
                return index
            }"""
        return -1

    def crear_bloqueApuntadores():
        bloque = bloqueApuntadores()
        return bloque

    def buscar_carpetaBloqueApuntadores(self, level, indiceBloque, indiceInodoActual, nameDir, bloque, path_Disco):
        dirname2 = str(nameDir)
        dirname2 = self.ajustar_cadena(12,dirname2)
        #VALIDAR EL NIVEL DEL APUNTADOR
        if(level == 1):
            #LEER EL BLOQUE DE APUNTADORES
            pointers = self.obtener_bloquesApuntadores(path_Disco, self.get_bloqueInicial(bloque, indiceBloque))
            for indiceApuntador in range(0,14):
                if(pointers.b_pointers[indiceApuntador] != -1):
                    #BUSCAR EL INODO
                    inodo = self.obtener_inodo(path_Disco, self.get_inodoInicial(bloque, pointers.b_pointers[indiceApuntador]))
                    if(inodo == None):
                        return -1
                    bl = bloqueCarpetas()
                    for indiceBloque in range(0,12):
                        if(inodo.i_block[indiceBloque] != -1):
                            #CREAR INODO DE NUEVA CARPETA(ARCHIVO:1,CARPETA:0)
                            if(inodo.i_type == 0):
                                bl = self.obtener_BloquesCarpetas(path_Disco, self.get_bloqueInicial(bloque, inodo.i_block[indiceBloque]))
                                if(bl == None):
                                    return -1
                                i = 0
                                if(bl.b_content[i].b_inodo != -1):
                                    if(len(bl.b_content[i].b_name) == len(dirname2)):
                                        indiceInodoActual = bl.b_content[0].b_inodo
                                        return inodo.i_block[indiceBloque]
        else:
            point = self.obtener_bloquesApuntadores(path_Disco, self.get_bloqueInicial(bloque, indiceBloque))
            for indexF in range(0,14):
                if(point.b_pointers[indexF] != -1):
                    i = self.buscar_carpetaBloqueApuntadores(level -1, point.b_pointers[indexF], indiceInodoActual, nameDir, bloque, path_Disco)
                    if(i != -1):
                        return i
        return -1

    def get_bloqueCarpetasLibre(self, nomDir, path_Disco, bloque, indiceBloqueActual, indiceInodoActual,indiceLibre, type):
        dirname2 = str(nomDir)
        dirname2 = self.ajustar_cadena(12,dirname2)
        #TIPO DE BLOQUE = 1:ARCHIVO, 2:DIRECTORIO, 3:APUNTADOR
        #LEER EL INODO
        inodo = tablaInodos()
        inodo = self.obtener_inodo(path_Disco, self.get_inodoInicial(bloque, indiceInodoActual))
        #VALIDAR QUE EL DIRECTORIO EXISTA
        if(inodo.i_s == 0):
            singleton.objL.respuesta['mensaje']+= ">>>>Error: No existe el disco>>>>"+"\n"
            print("*****************************************************************************")
            return False
        idPoint = 0
        flag_directo = True
        blcarpeta = bloqueCarpetas()
        encontrado = False
        #RECORRER LOS INODOS HASTA ENCONTRAR EL DESEADO
        while(idPoint < singleton.objL.tam_bloques_inodos and encontrado == True):
            if(inodo.i_block[idPoint] != -1):
                if(flag_directo):
                    #LEER EL BLOQUE DE CARPETAS
                    blcarpeta = self.obtener_BloquesCarpetas(path_Disco, self.get_bloqueInicial(bloque, inodo.i_block[idPoint]))
                    #VERIFICAR QUE EXISTA EL BLOQUE
                    if(len(blcarpeta.b_content[0].b_name) == len(dirname2)):
                        #OBTENER EL INDICE DEL BLOQUE ENCONTRADO
                        indiceBloqueActual = inodo.i_block[idPoint]
                        indiceBloque = 2
                        #RECORRER LOS BLOQUES 
                        while(indiceBloque < 4):
                            #VALIDAR QUE EL ESPACIO ESTE LIBRE
                            if(blcarpeta.b_content[indiceBloque].b_inodo == -1):
                                #ASIGNAR EL VALOR AL PARAMETRO POR REFERENCIA
                                indiceLibre = indiceBloque
                                encontrado = True
                                break
                            indiceBloque+=1
                else:
                    #LEER APUNTADOR INDIRECTO
                    type = 3
                    indiceBloqueActual = inodo.i_block[idPoint]
                    #OBTENER EL BLOQUE DE APUNTADORES LIBRE
                    bl = self.get_bloqueApuntadorLibre(idPoint, inodo, indiceBloqueActual, path_Disco, bloque, indiceLibre)
                    #ESCRIBIR EL INODO EN EL DISCO
                    self.escribir_inodo(inodo, path_Disco, self.get_inodoInicial(bloque, indiceInodoActual))
                    #VERIFICAR QUE SE HAYA CREADO EL BLOQUE
                    if(bl == -1):
                        idPoint+=1
                        continue
                    encontrado = True
                    indiceBloqueActual = bl
            else:
                #VALIDAR SI ES APUNTADOR DIRECTO
                if(flag_directo):
                    #CREAR UN NUEVO BLOQUE DE CARPETAS
                    nuevo = self.crear_bloque_carpetas(blcarpeta.b_content[0].b_name, blcarpeta.b_content[0].b_inodo,blcarpeta.b_content[1].b_name, blcarpeta.b_content[1].b_inodo)
                    #APUNTAR AL PRIMER BLOQUE
                    inodo.i_block[idPoint] = bloque.first_b
                    #ESCRIBIR EL BLOQUE DE DIRECTORIOS
                    self.escribir_bloquesCarpetas(nuevo, path_Disco, self.get_bloqueInicial(bloque, bloque.first_b))
                    #ESCRIBIR EL INODO
                    self.escribir_inodo(inodo, path_Disco, self.get_inodoInicial(bloque, *indiceInodoActual))
                    #RESTAR UN INODO Y UN BLOQUE DEL SUPER BLOQUE
                    indiceBloqueActual = bloque.first_b
                    indiceLibre = 2
                    encontrado = True
                    #MARCAR LOS BITMAPS
                    bloque.first_b = self.getBM_index(bloque.bmb_start, bloque.b_count, path_Disco)
                    bloque.free_b-=1
                else:
                    #CREAR UN NUEVO BLOQUE
                    bl = self.crear_apuntadorInd(idPoint, indiceBloqueActual, bloque, path_Disco)
                    #VALIDAR QUE HAYA ESPACIO PARA CREAR EL BLOQUE
                    if(bl == -1):
                        singleton.objL.respuesta['mensaje']+= ">>>>Error: Espacio insuficiente, no se crearon mas carpetas o archivos.>>>>"+"\n"
                        print("*****************************************************************************")
                        return False
                    inodo.i_block[idPoint] = bl
                    #ESCRIBIR EL INODO
                    self.escribir_inodo(inodo, path_Disco, self.get_inodoInicial(bloque, *indiceInodoActual))
                    indice_libre = 0
                    type = 3
                    encontrado = True
            idPoint+=1
            #VALIDAR QUE EL PUNTERO SEA DIRECTO
            if(idPoint > 11):
                flag_directo = False
        return True

    def get_bloqueApuntadorLibre(self, level, inodo, indiceBloqueActual, path_Disco, bloque, indice_libre):
        #VALIDAR QUE EXISTA EL BLOQUE
        if(inodo.i_block[level] != -1):
            #VALIDAR QUE SEA BLOQUE DE APUNTADORES
            if(level == 12):
                #LEER EL BLOQUE DE APUNTADORES
                apuntadores = self.obtener_bloquesApuntadores(path_Disco, self.get_bloqueInicial(bloque, indiceBloqueActual))
                #VALIDAR QUE SE HAYA LEIDO LA INFORMACION
                if(apuntadores == None):
                    singleton.objL.respuesta['mensaje']+= ">>>>Error: El directorio no existe.>>>>"+"\n"
                    print("*****************************************************************************")
                    return False
                #RECORRER LOS APUNTADORES
                for indiceBloqueAp in range(0,singleton.objL.tam_bloques_inodos):
                    #VALIDAR QUE SEA EL PRIMER APUNTADOR
                    if(apuntadores.b_pointers[indiceBloqueAp] == -1):
                        #ASIGNAR EL VALOR AL ESPACIO LIBRE
                        indice_libre = indiceBloqueAp
                        #RETORNAR EL INDICE ACTUAL
                        return indiceBloqueActual
            else:
                #LEER EL BLOQUE DE APUNTADORES SI EL PRIMERO NO ESTA LIBRE
                ap = self.obtener_bloquesApuntadores(path_Disco, self.get_bloqueInicial(bloque, indiceBloqueActual))
                #VALIDAR QUE SE HAYA LEIDO LA INFORMACION
                if(ap == None):
                    singleton.objL.respuesta['mensaje']+= ">>>>Error: El directorio no existe.>>>>"+"\n"
                    print("*****************************************************************************")
                    return False
                #VALIDAR RECURSIVAMENTE QUE SE ESTEN LEYENDO TODOS LOS APUNTADORES DEL BLOQUE 
                for indiceBloqueP in range(0,singleton.objL.tam_bloques_inodos):
                    #VALIDAR QUE SE LEAN LOS APUNTADORES DEL BLOQUE
                    if(ap.b_pointers[indiceBloqueP] != -1):
                        res = self.get_bloqueApuntadorLibre(level - 1, inodo, ap.b_pointers[indiceBloqueP], path_Disco, bloque, indice_libre)
                        #RETORNAR EL BLOQUE LIBRE
                        if(res != -1):
                            return False
                    else:
                        #ASIGNAR EL BLOQUE ACTUAL COMO EL PADRE
                        bloquePadre = indiceBloqueActual
                        #CREAR LOS APUNTADORES
                        bloqueS = self.crear_apuntadorInd(level -1, indiceBloqueActual, bloque, path_Disco)
                        if(bloqueS == -1):
                            singleton.objL.respuesta['mensaje']+= ">>>>Error: Espacio insuficiente, no se crearon mas carpetas o archivos.>>>>"+"\n" 
                            print("*****************************************************************************")
                            return False
                        #ASIGNAR LOS APUNTADORES CREADOS AL BLOQUE
                        ap.b_pointers[indiceBloqueP] = bloqueS
                        #ESCRIBIR EN EL DISCO
                        self.escribir_bloqueApuntadores(ap, path_Disco, self.get_bloqueInicial(bloque, bloquePadre))
                        indice_libre = 0
                        return bloqueS
        return -1

    def crear_apuntadorInd(self, idPoint, idBloqueActual, bloque, path_Disco):
        #VALIDAR QUE EL APUNTADOR SEA INDIRECTO
        if(idPoint -11 == 1):
            #OBTENER EL BLOQUE DE APUNTADORES
            aux = self.crear_bloqueApuntadores()
            #OBTENER EL ID
            idBloque = bloque.first_b
            #ESCRIBIR EL BLOQUE EN EL DISCO
            self.escribir_bloqueApuntadores(aux, path_Disco, self.get_bloqueInicial(bloque, bloque.s_first_blo))
            #MARCAR EL BITMAP
            bloque.s_first_blo = self.getBM_index(bloque.s_bm_block_start, bloque.s_blocks_count, path_Disco)
            #RESTAR EL CONTADOR DE BITMAP 
            bloque.s_free_blocks_count-=1
            #ASIGNAR EL ID
            idBloqueActual = idBloque
            return idBloque
        else:
            #SI NO HAY BLOQUE DE APUNTADORES SENALADO SE GENERA UNO NUEVO
            #CREAR APUNTADORES RECURSIVAMENTE
            res = self.crear_apuntadorInd(idPoint -1, idBloqueActual, bloque, path_Disco)
            #CREAR BLOQUE
            aux = self.crear_bloqueApuntadores()
            #ASIGNAR EL APUNTADOR CREADO
            aux.b_pointers[0] = res
            #ASIGNAR EL BLOQUE AL INICIO
            res = bloque.s_first_blo
            #ESCRIBIR EL BLOQUE DE APUNTADORES EN EL DISCO
            self.escribir_bloqueApuntadores(aux, path_Disco, self.get_bloqueInicial(bloque, bloque.s_first_blo))
            #MARCAR EL BITMAP
            bloque.s_first_blo = self.getBM_index(bloque.s_bm_block_start, bloque.s_blocks_count, path_Disco)
            #RESTAR CONTADOR DEL BITMAP DE BLOQUES
            bloque.s_free_blocks_count-=1
            #RETORNAR EL ID DEL PRIMER BLOQUE
            return res
        return -1

    def escribir_bloqueCarpetas(self, auxsuper_bloque, path_Disco, inicio):
        with open(path_Disco, "rb+") as file:
            bytes = auxsuper_bloque.get_bytes()
            file.seek(inicio)
            file.write(bytes)

    def get_bloqueInicial(self, bloque, indice):
        return bloque.b_start + (bloque.b_s * indice)

    def crear_directorio(self,bloque,path_Disco,nomDir,nomPad,indicePad):
        #CREAR INODO DE NUEVA CARPETA(ARCHIVO:1,CARPETA:0)
        aux_inodo = self.crear_inodo(0, 777, -1)
        indice_I = bloque.first_i
        #CREAR BLOQUE DE DIRECTORIOS
        bloque2 = self.crear_bloque_carpetas(nomDir, indice_I, nomPad, indicePad)
        #ASIGNAR EL BLOQUE A LA CARPETA CREADA
        aux_inodo.i_block[0] = bloque.first_b
        #ESCRIBIR EL INODO
        self.escribir_inodo(aux_inodo, path_Disco, self.get_inodoInicial(bloque, indice_I))
        #ESCRIBIR BLOQUE DE DIRECTORIOS
        self.escribir_bloqueCarpetas(bloque2, path_Disco, self.get_bloqueInicial(bloque, bloque.first_b))
        #MARCAR BITMAPS
        bloque.first_i = self.getBM_index(bloque.bmi_start, bloque.i_count, path_Disco)
        bloque.first_b = self.getBM_index(bloque.bmb_start, bloque.b_count, path_Disco)
        #RESTAR CONTADORES DE ESPACIOS LIBRES PARA BLOQUES DE CARPETAS Y DE INDODOS CREADOS
        bloque.free_b-=1
        bloque.free_i-=1
        return indice_I

    def escribir_bloquesArchivos(self, bloque, path_Disco, inicio):
        with open(path_Disco, "rb+") as file:
            bytes = bloque.get_bytes()
            file.seek(inicio)
            file.write(bytes)

    def guardar_bloqueArchivos(self, bloqueA, bloqueS,path_Disco):
        #ESCRIBIR EL BLOQUE DE ARCHIVOS EN EL DISCO
        self.escribir_bloquesArchivos(bloqueA, path_Disco, self.get_bloqueInicial(bloqueS, bloqueS.first_b))
        #OBTENER LA DIRECCION DEL PRIMER BLOQUE EN LOS BITMAPS
        bloqueS.first_b = self.getBM_index(bloqueS.bmb_start, bloqueS.b_count, path_Disco)
        #RESTAR EL ESPACIO DISPONIBLE EN LOS BLOQUES
        bloqueS.free_b-=1

    def crear_bloqueArchivos(self):
        bloque = bloqueArchivos()
        return bloque

    def crear_nodoArchivo(self, size, texto, path_Disco, dirpad, name, super_bloque, indiceBloqueActual, indiceInodoPadre):
        dirname2 = str(name)
        dirname2 = self.ajustar_cadena(12,dirname2)
        texto = self.ajustar_cadena(64,texto)
        indice_libre = -1
        #CREAR INODO DE NUEVA CARPETA(ARCHIVO:1,CARPETA:0)
        type = 0
        #OBTENER EL BLOQUE DE CARPETAS LIBRE
        res = self.get_bloqueCarpetasLibre(dirpad, path_Disco, super_bloque, indiceBloqueActual, indiceInodoPadre, indice_libre, type)
        #VALIDAR QUE SE HAYA ESCRITO
        if(res == False):
            return False
        #CREAR EL INODO DEL ARCHIVO
        inodo = self.crear_inodo(1, 664, size)
        #CREAR EL BLOQUE DE ARCHIVO
        bl = self.crear_bloqueArchivos()
        indiceInodo = 0
        indiceCar = 0
        contCar = 0
        guardado = True
        #CICLO INFINITO PARA ESCRIBIR EL ARCHIVO
        while(guardado):
            if(contCar >= 64 or indiceCar >= size):
                #VALIDAR LOS APUNTADORES DIRECTOS
                if(indiceInodo < 12):
                    inodo.i_block[indiceInodo] = super_bloque.first_b
                    #ESCRIBIR LA INFORMACION EN EL DISCO
                    self.guardar_bloqueArchivos(bl, super_bloque, path_Disco)
                    indiceInodo+=1
                else:
                    #AGREAR BLOQUES DE APUNTADORES
                    resp = self.agregar_bloqueApuntadores(inodo, indiceInodo, bl, super_bloque, path_Disco)
                    #VERIFICAR QUE HAYA ESPACIO EN EL BLOQUE
                    if(resp == False):
                        if(indiceInodo < 14):
                            indiceInodo+=1
                            continue
                    elif(resp != True):
                        return False
                #CREAR UN NUEVO BLOQUE DE ARCHIVOS
                bl = self.crear_bloqueArchivos()
                #REINICIAR EL CONTADOR DE CARACTERES
                contCar = 0
            #ASIGNAR EL CONTENIDO AL BLOQUE
            bl.b_content[contCar] = texto[indiceCar]
            #VERIFICAR QUE EL CONTENIDO SEA ACORDE AL TAMANO
            if(indiceCar >= size):
                break
            contCar+=1
            indiceCar+=1
        #ESCRIBIR EL INODO
        self.escribir_inodo(inodo,path_Disco,self.get_inodoInicial(super_bloque,super_bloque.first_i))
        #LEER EL BLOQUE DE CARPETAS
        aux_carpetas = self.obtener_BloquesCarpetas(path_Disco, self.get_bloqueInicial(super_bloque, indiceBloqueActual))
        aux_carpetas.b_content[indice_libre].b_inodo = super_bloque.first_i
        #CREAR UN NUEVO BLOQUE DE CARPETAS
        aux_carpetas.b_content[indice_libre].b_name = str(dirname2)
        self.escribir_bloquesCarpetas(aux_carpetas, path_Disco, self.get_bloqueInicial(super_bloque, indiceBloqueActual))
        #MARCAR EL BITMAP
        super_bloque.first_i = self.getBM_index(super_bloque.bmi_start, super_bloque.i_count, path_Disco)
        #RESTAR EL CONTADOR DE INODOS
        super_bloque.free_i-=1
        return True

    def crear_archivosEscritos(self,newPath,createPath,text,size,path_Disco):
        #VALIDAR SI HAY ESPACIO PARA CREAR INODOS Y BLOQUES
        #OBTENER SUPER BLOQUE DEL DISCO
        super_bloque = self.obtener_super_bloque(path_Disco)
        indexInodoPadre = 0
        dirPad="/"
        indexBloqueActual = 0
        tokens = newPath.split('/')
        for token in tokens:
            if(token!=""):
                #SI HA LLEGADO AL ULTIMO ELEMENTO
                if (token == tokens[-1]):
                    self.crear_nodoArchivo(size,text,path_Disco,dirPad[0],token[0],super_bloque,indexBloqueActual,indexInodoPadre)
                else:
                    indexBloque = self.buscarCarpeta(token[0],path_Disco,indexInodoPadre,super_bloque)
                    if(indexBloque!=-1):
                        indexBloqueActual = indexBloque
                    else:
                        if(createPath):
                            rs = self.crear_nodoCarpeta(dirPad[0],token[0],path_Disco,super_bloque,indexInodoPadre,indexBloqueActual)
                        else:
                            singleton.objL.respuesta['mensaje']+= ">>>>Error: No existe el disco>>>>"+"\n"
                            print("*****************************************************************************")    
                dirPad = token
        self.escribir_super_bloque(super_bloque,path_Disco,self.INICIO_PARTITION)

    def guardar_DatosRep(self, idmount,path_disco,supBloque,inicio):
        new_idsRep = idsRep(idmount,path_disco,supBloque,inicio)
        singleton.objL.list_idsRep.append(new_idsRep)