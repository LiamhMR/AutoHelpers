"""
Realizar logs sencilos y coopera en la realización de reportes.
"""
import json
from os import path
import datetime as dt

def logger( path , text :str):
    """Crea o abre un archivo log y escribe en la última línea el elemento de log.
        @path -- Ruta del archivo log
        @text -- Texto a añadir al log
    """
    try:
        with open ( path , "a" ) as mf:
            mf.write( str(simplifyTime(dt.datetime.now()))+ " : " + str(text) + "\n")
        return True
    except:
        with open( path , "w" ) as mf:
            mf.write( str(simplifyTime(dt.datetime.now()))+ " : " + str(text) + "\n")
            return True
 
def simplifyTime(time):
    """Retorna una hora en formato simple HH:MM:SS
        @time : En formato data time HH:MM:SS:XXXX 
    """
    c_time=str(time)
    c_time=c_time.split(" ")
    date=c_time[0].split("-")
    date=str(date[2])+"/"+str(date[1])+"/"+str(date[0])
    
    
    hour=c_time[1]
    hour=hour.split(".")[0]
    simple_time=str(date)+" "+str(hour)
    return simple_time
         
def appendJSON(path,id,new_state):
    """Cambia el valor de un elemento de un JSON
    """
    update={id:new_state}
    diccionario={}
    with open ( path , "r" ) as mf:
        diccionario=json.load(mf)
       
    try:
        diccionario[str(id)]=new_state
    except:
        diccionario.update({id:new_state})      
    with open(path, 'w') as file:
        json.dump(diccionario, file, indent=4)
        
def getJSON(path):
    """Retorna un JSON diccionario."""
    with open ( path , "r" ) as mf:
        diccionario=json.load(mf)
        return diccionario
    


    
