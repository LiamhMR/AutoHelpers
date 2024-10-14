import random
import re
from unicodedata import normalize
import hashlib
import os
"""
Helper de manejo de strings
"""

def hash_pass(password):
    """
    Codifica la contraseña utilizando SHA-256 y un salt aleatorio.
    
    @password: Entrada para codificar.
    """
    # Generar un salt aleatorio
    salt = os.urandom(16)
    
    # Concatenar el salt a la contraseña y codificar en SHA-256
    hash_object = hashlib.sha256(salt + password.encode())
    
    # Obtener el hash en formato hexadecimal
    hashed_password = hash_object.hexdigest()
    
    # Retornar hash y su salt
    return salt.hex() + ":" + hashed_password

""" 
<<<<<<<<<CODE PASS Y DECODE PASS>>>>>>>>>>>
Cifrado de strings para no guardar contraseñas brutas, bidireccional para uso de contraseñas en funciones lógicas internas.
El objetivo es enmascarar las contraseñas en el código y evitar su uso explícito.
La barrera de seguridad es bastante baja, no usarla como medida de seguridad, o al menos no la única. Usa orígenes de contraseña en archivos seguros.
"""
def code_pass(password):
    """
        @password : Entrada para codificar.
    """
    crp_pass=""
    
    start_index=random.randint(63,122)
    crp_pass+=chr(start_index)
    len_pass=len(password)
    crp_pass+=chr(len_pass+50)
    
    index=0
    while index<(start_index//2):
         rand_char=random.randint(63,122)
         crp_pass+=chr(rand_char)
         index+=1
    
    for c in password:
        if ord(c)%2==0:
            crp_pass+=chr(ord(c)-5)
        else:
            crp_pass+=chr(ord(c)+5)
    
    index=0
    while index<(start_index//2):
         rand_char=random.randint(63,122)
         crp_pass+=chr(rand_char)
         index+=1
        
    return crp_pass

def decode_pass(code_password):
    """
        @code_password  : Una entrada codificada por la def de esta misma librería.
    """
    dcd_pass=""
    index=0
    stop_decode=0
    for c in code_password:
        if index==0:
            start_index=ord(c)//2
        elif index==1:
            len_pass=ord(c)-50
        elif index>start_index+1:
            if stop_decode<len_pass:
                if ord(c)%2!=0:
                    dcd_pass+=chr(ord(c)+5)
                else:
                    dcd_pass+=chr(ord(c)-5)
                stop_decode+=1
            else:
                break
        index+=1
    return dcd_pass

def ststr(strarr):
    """Estandariza un string eliminando símbolos y espacios y lo deja en minúsculas, útil para comparar entre strings.
        @strarr : Entrada en string.
    """
    newstr=strarr.replace(" ","")
    
    newstr=newstr.lower()
    newstr=newstr.replace('ñ','n')
    newstr=re.sub(
        r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
        normalize( "NFD", newstr), 0, re.I
    )
    newstr="".join(char for char in newstr if char.isalnum())

    return newstr

def getDecimal(strdec):
    """ Recibe una entrada en formato decimal y lo retorna spliteado en '
        @strdec : Entrada en formato Decimal.
    """
    try:
        splitstr=(strdec.split("'"))[1]
    except:
        return None
    return splitstr
