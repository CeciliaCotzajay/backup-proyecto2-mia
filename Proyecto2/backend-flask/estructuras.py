from abc import ABC, abstractmethod

#*****************************************ABSTRACTA********************************************
class Objeto(ABC):
    @abstractmethod
    def get_bytes(self):
        pass
    @abstractmethod
    def set_bytes(self, bytes):
        pass    
    @abstractmethod
    def get_size(self):
        pass

#*****************************************MBR**************************************************
class MBR(Objeto):

    def __init__(self, size, date, signature, fit): #125
        self.size = size # int (4 bytes)
        self.date = date # double (8 bytes)
        self.signature = signature # int (4 bytes)
        self.fit = fit # char (1 byte)
        self.partitions = [] #27bytes por cada una, 108 total
        self.partitions.append(Partition('n',' ',' ',0,0,"                "))
        self.partitions.append(Partition('n',' ',' ',0,0,"                "))
        self.partitions.append(Partition('n',' ',' ',0,0,"                "))
        self.partitions.append(Partition('n',' ',' ',0,0,"                "))

    def get_bytes(self):
        bytes = bytearray()
        bytes += self.size.to_bytes(4, byteorder='big')
        bytes += self.date.to_bytes(8, byteorder='big')
        bytes += self.signature.to_bytes(4, byteorder='big')
        bytes += self.fit.encode('utf-8')
        #print(len(bytes))
        for partition in self.partitions:
            bytes += partition.get_bytes()
            #print(len(bytes))
        return bytes

    def set_bytes(self, bytes):
        #print(len(bytes))
        self.size = int.from_bytes(bytes[0:4], byteorder='big')
        self.date = int.from_bytes(bytes[4:12], byteorder='big')
        self.signature = int.from_bytes(bytes[12:16], byteorder='big')
        self.fit = bytes[16:17].decode('utf-8')
        self.partitions = [] #108,27
        ini =17
        fin =ini+27
        for i in range(0,4):
            temp = Partition(' ',' ',' ',0,0,"                ")
            temp.set_bytes(bytes[ini:fin])
            self.partitions.append(temp)
            ini=fin
            fin+=27


    def get_size(self):
        size = 0
        size += 4
        size += 8
        size += 4
        size += 1
        for partition in self.partitions:
            size += partition.get_size()
        return size
            
    
#*****************************************PARTITION********************************************
class Partition(Objeto):

    def __init__(self, status, type, fit, start, s, name):# 27
        self.status = status #char (1 byte) ; activa o no activa, 's','n','m',e'
        self.type = type #char (1 byte)     ; p,e,l
        self.fit = fit #char (1 byte)       ; f,b,w
        self.start = start #int (4 bytes)   ; byte donde inicia
        self.s = s #int (4 bytes)           ; tamanio bytes
        self.name = name #char (16 bytes)   ; nombre

    def get_bytes(self):
        bytes = bytearray()
        bytes += self.status.encode('utf-8')
        bytes += self.type.encode('utf-8')
        bytes += self.fit.encode('utf-8')
        bytes += self.start.to_bytes(4, byteorder='big')
        bytes += self.s.to_bytes(4, byteorder='big')
        bytes += self.name.encode('utf-8')
        return bytes

    def set_bytes(self, bytes):
        self.status = bytes[0:1].decode('utf-8')
        self.type = bytes[1:2].decode('utf-8')
        self.fit = bytes[2:3].decode('utf-8')
        self.start = int.from_bytes(bytes[3:7], byteorder='big')
        self.s = int.from_bytes(bytes[7:11], byteorder='big')
        self.name = bytes[11:27].decode('utf-8')

    def get_size(self):
        size = 0
        size += 1
        size += 1
        size += 1
        size += 4
        size += 4
        size += 16
        return size
    
#********************************************EBR***********************************************

class EBR(Objeto):

    def __init__(self,status,fit,start,s,nextB,name):#30
        self.status = status # char (1 byte)    ; activa o no activa, 's','n','m',e'
        self.fit = fit # char (1 byte)          ; b,f,w
        self.start = start # int (4 bytes)      ; byte donde inicia
        self.s = s # int (4 bytes)              ; tamanio bytes
        self.nextB = nextB # int (4 bytes)      ; byte donde inicia el siguiente EBR
        self.name = name #char (16 bytes)       ; nombre

    def get_bytes(self):
        bytes = bytearray()
        bytes += self.status.encode('utf-8')
        bytes += self.fit.encode('utf-8')
        bytes += self.start.to_bytes(4, byteorder='big')
        bytes += self.s.to_bytes(4, byteorder='big')
        bytes += self.nextB.to_bytes(4, byteorder='big')
        bytes += self.name.encode('utf-8')
        #print(len(bytes))
        return bytes

    def set_bytes(self, bytes):
        #print(len(bytes))
        self.status = bytes[0:1].decode('utf-8')
        self.fit = bytes[1:2].decode('utf-8')
        self.start = int.from_bytes(bytes[2:6], byteorder='big')
        self.s = int.from_bytes(bytes[6:10], byteorder='big')
        self.nextB = int.from_bytes(bytes[10:14], byteorder='big')
        self.name = bytes[14:30].decode('utf-8')


    def get_size(self):
        size = 0
        size += 1
        size += 1
        size += 4
        size += 4
        size += 4
        size += 16
        return size
    
#****************************************SUPER-BLOQUE******************************************

class superBloque(Objeto):

    def __init__(self): #76
        self.type = 2 # int (4 bytes)               # ext2 o ext3
        self.i_count = 0 # int (4 bytes)            # Guarda el número total de inodos
        self.b_count = 0 # int (4 bytes)            # Guarda el número total de bloques
        self.free_i = 0 # int (4 bytes)             # Contiene el número de bloques libres
        self.free_b = 0 # int (4 bytes)             # Contiene el número de inodos libres
        self.m_time = 0 # int (8 bytes)             # Última fecha en el que el sistema fue montado
        self.um_time = 0 # int (8 bytes)            # Última fecha en que el sistema fue desmontado
        self.nm_count = 0 # int (4 bytes)           # Indica cuantas veces se ha montado el sistema
        self.magic = 0 # int (4 bytes)              # Valor que identifica al sistema de archivos, tendrá 0xEF53
        self.i_s = 0 # int (4 bytes)                # Tamaño del inodo
        self.b_s = 0 # int (4 bytes)                # Tamaño del bloque
        self.first_i = 0 # int (4 bytes)            # Primer inodo libre
        self.first_b = 0 # int (4 bytes)            # Primer bloque libre
        self.bmi_start = 0 # int (4 bytes)          # Guardará el inicio del bitmap de inodos
        self.bmb_start = 0 # int (4 bytes)          # Guardará el inicio del bitmap de bloques
        self.i_start = 0 # int (4 bytes)            # Guardará el inicio de la tabla de inodos
        self.b_start = 0 # int (4 bytes)            # Guardará el inicio de la tabla de bloques

    def get_bytes(self):
        bytes = bytearray()
        bytes += self.type.to_bytes(4, byteorder='big')
        bytes += self.i_count.to_bytes(4, byteorder='big')
        bytes += self.b_count.to_bytes(4, byteorder='big')
        bytes += self.free_i.to_bytes(4, byteorder='big')
        bytes += self.free_b.to_bytes(4, byteorder='big')
        bytes += self.m_time.to_bytes(8, byteorder='big')
        bytes += self.um_time.to_bytes(8, byteorder='big')
        bytes += self.nm_count.to_bytes(4, byteorder='big')
        bytes += self.magic.to_bytes(4, byteorder='big')
        bytes += self.i_s.to_bytes(4, byteorder='big')
        bytes += self.b_s.to_bytes(4, byteorder='big')
        bytes += self.first_i.to_bytes(4, byteorder='big')
        bytes += self.first_b.to_bytes(4, byteorder='big')
        bytes += self.bmi_start.to_bytes(4, byteorder='big')
        bytes += self.bmb_start.to_bytes(4, byteorder='big')
        bytes += self.i_start.to_bytes(4, byteorder='big')
        bytes += self.b_start.to_bytes(4, byteorder='big')
        #print(len(bytes))
        return bytes

    def set_bytes(self, bytes):
        #print(len(bytes))
        self.type = int.from_bytes(bytes[0:4], byteorder='big')
        self.i_count = int.from_bytes(bytes[4:8], byteorder='big')
        self.b_count = int.from_bytes(bytes[48:52], byteorder='big')
        self.free_i = int.from_bytes(bytes[8:12], byteorder='big')
        self.free_b = int.from_bytes(bytes[12:16], byteorder='big')
        self.m_time = int.from_bytes(bytes[16:20], byteorder='big')
        self.um_time = int.from_bytes(bytes[20:28], byteorder='big')
        self.nm_count = int.from_bytes(bytes[28:36], byteorder='big')
        self.magic = int.from_bytes(bytes[36:40], byteorder='big')
        self.i_s = int.from_bytes(bytes[40:44], byteorder='big')
        self.b_s = int.from_bytes(bytes[44:48], byteorder='big')
        self.first_i = int.from_bytes(bytes[52:56], byteorder='big')
        self.first_b = int.from_bytes(bytes[56:60], byteorder='big')
        self.bmi_start = int.from_bytes(bytes[60:64], byteorder='big')
        self.bmb_start = int.from_bytes(bytes[64:68], byteorder='big')
        self.i_start = int.from_bytes(bytes[68:72], byteorder='big')
        self.b_start = int.from_bytes(bytes[72:76], byteorder='big')

    def get_size(self):
        size = 76
        return size

#****************************************TABLA-INODOS******************************************

class tablaInodos(Objeto):

    def __init__(self): #101
        self.i_uid = 0 # int (4 bytes)
        self.i_gid =0 # int (4 bytes)
        self.i_s = 0 # int (4 bytes)
        self.i_atime = 0 # int (8 bytes)
        self.i_ctme = 0 # int (8 bytes)
        self.i_mtime = 0 # int (8 bytes)
        self.i_type = ' ' # char (1 byte)
        self.i_perm = 0 # int (4 bytes)
        self.i_block = [] # 60 bytes
        for i in range(0,15):
            self.i_block.append(-1)# int (4 bytes)

    def get_bytes(self):
        bytes = bytearray()
        bytes += self.i_uid.to_bytes(4, byteorder='big')
        bytes += self.i_gid.to_bytes(4, byteorder='big')
        bytes += self.i_s.to_bytes(4, byteorder='big', signed=True)
        bytes += self.i_atime.to_bytes(8, byteorder='big')
        bytes += self.i_ctme.to_bytes(8, byteorder='big')
        bytes += self.i_mtime.to_bytes(8, byteorder='big')
        bytes += self.i_type.encode('utf-8')
        bytes += self.i_perm.to_bytes(4, byteorder='big')
        for c in self.i_block:
            bytes += c.to_bytes(4, byteorder='big', signed=True)
        #print(len(bytes))
        return bytes

    def set_bytes(self, bytes):
        #print(len(bytes))
        self.i_uid = int.from_bytes(bytes[0:4], byteorder='big')
        self.i_gid = int.from_bytes(bytes[4:8], byteorder='big')
        self.i_s = int.from_bytes(bytes[8:12], byteorder='big')
        self.i_atime = int.from_bytes(bytes[12:20], byteorder='big')
        self.i_ctme = int.from_bytes(bytes[20:28], byteorder='big')
        self.i_mtime = int.from_bytes(bytes[28:36], byteorder='big')
        self.i_type = bytes[36:37].decode('utf-8')
        self.i_perm = int.from_bytes(bytes[37:41], byteorder='big')
        self.i_block = [] #15,4
        ini =0
        fin =ini+4
        for i in range(0,15):
            c = 0
            c = int.from_bytes(bytes[ini:fin], byteorder='big', signed=True)
            self.i_block.append(c)
            ini=fin
            fin+=4

    def get_size(self):
        size = 0
        size += 41
        size += 60
        return size

#****************************************CONTENT******************************************

class Content(Objeto):

    def __init__(self, b_name, b_inodo):#16
        self.b_name = b_name #char (12 bytes)
        self.b_inodo = b_inodo #int (4 bytes)

    def get_bytes(self):
        bytes = bytearray()
        bytes += self.b_name.encode('utf-8')
        bytes += self.b_inodo.to_bytes(4, byteorder='big', signed=True)
        #print(len(bytes))
        return bytes

    def set_bytes(self, bytes):
        #print(len(bytes))
        self.b_name = bytes[0:12].decode('utf-8')
        self.b_inodo = int.from_bytes(bytes[12:16], byteorder='big', signed=True)

    def get_size(self):
        size = 0
        size += 12
        size += 4
        return size
            
#****************************************BLOQUE-CARPETA******************************************

class bloqueCarpetas(Objeto):

    def __init__(self):#64
        self.b_content = [] #16bytes por cada una, 64 total
        self.b_content.append(Content("            ",-1))
        self.b_content.append(Content("            ",-1))
        self.b_content.append(Content("            ",-1))
        self.b_content.append(Content("            ",-1))

    def get_bytes(self):
        bytes = bytearray()
        for conte in self.b_content:
            bytes += conte.get_bytes()
            #print(len(bytes))
        return bytes

    def set_bytes(self, bytes):
        self.b_content = [] #64,16
        ini =0
        fin =ini+16
        for i in range(0,4):
            temp = Content("            ",-1)
            temp.set_bytes(bytes[ini:fin])
            self.b_content.append(temp)
            ini=fin
            fin+=16

    def get_size(self):
        size = 0
        for conte in self.b_content:
            size += conte.get_size()
        return size
    
#****************************************BLOQUE-ARCHIVO******************************************

class bloqueArchivos(Objeto):

    def __init__(self):#64
        self.b_content = [] #char (64 bytes)
        for i in range(0,64):
            self.b_content.append(" ")

    def get_bytes(self):
        bytes = bytearray()
        for c in self.b_content:
            bytes += c.encode('utf-8')
            #print(len(bytes))
        return bytes

    def set_bytes(self, bytes):   
        self.b_content = [] #64,1
        ini =0
        fin =ini+1
        for i in range(0,64):
            c = ""
            c = bytes[ini:fin].decode('utf-8')
            self.b_content.append(c)
            ini=fin
            fin+=1

    def get_size(self):
        size = 0
        size += 64
        return size

#****************************************BLOQUE-APUNTADORES*************************************

class bloqueApuntadores(Objeto):

    def __init__(self):#DEBERIA SER 64, DIRECTO,SIMPLES,DOBLES,TRIPLES
        self.b_pointers = [] #int (16 bytes)
        for i in range(0,16):
            self.b_pointers.append(-1)

    def get_bytes(self):
        bytes = bytearray()
        for c in self.b_pointers:
            bytes += c.to_bytes(4, byteorder='big', signed=True)
            #print(len(bytes))
        return bytes

    def set_bytes(self, bytes):
        
        self.b_pointers = []#16,1
        ini =0
        fin =ini+1
        for i in range(0,16):
            c = ""
            c = int.from_bytes(bytes[ini:fin], byteorder='big', signed=True)
            self.b_pointers.append(c)
            ini=fin
            fin+=1

    def get_size(self):
        size = 0
        size += 16        
        return size
    
#*******************************************JOURNAL*********************************************

class Journal(Objeto):

    def __init__(self):#250 
        self.date = 0      #int (8 bytes)
        self.path = ""     #char (16 bytes)
        self.line = ""     #char (228 bytes)

    def get_bytes(self):
        bytes = bytearray()
        bytes += self.date.to_bytes(8, byteorder='big')
        bytes += self.path.encode('utf-8')
        bytes += self.line.encode('utf-8')
        #print(len(bytes))
        return bytes

    def set_bytes(self, bytes):
        #print(len(bytes))
        self.date = int.from_bytes(bytes[0:8], byteorder='big')
        self.path = bytes[8:24].decode('utf-8')
        self.line = bytes[24:250].decode('utf-8')


    def get_size(self):
        size = 0
        size += 250
        return size
    
#*******************************************PARA_REP*********************************************

    
class idsRep:

    def __init__(self,idmount,path_disco,supBloque,inicio):
        self.idmount = idmount      
        self.path_disco = path_disco    
        self.supBloque = supBloque
        self.inicio = inicio
        self.inodos = []
        self.bm_inodo = []
        self.bm_bloque = []