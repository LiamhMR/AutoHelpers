from StringMngr import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

#Recibe el navegador, el id de un elemento y el color con el que se quiere compara
#Retorna true si el color del elemento es igual al color ingresado
#variable color debe ser ingresada en formato rgb, ejemplo "rgb(0, 0, 0)"
def cmpIdColor(driver,id,color):
    """Retorna True si rgb del id igual al rgb del 'color'
        @driver : Navegador
        @id     : Id del elemento a revisar.
        @color  : Color con el que comparar, formar str rgb(r,g,b)
    """
    getcolor_js="""
    return getComputedStyle(document.getElementById('"""+id+"""')).getPropertyValue("color");
    """
    idcolor=driver.execute_script(getcolor_js)
    #print(idcolor+" = "+ color)
    if idcolor.replace(" ","")==color.replace(" ",""):
        #print("Color Identico.",idcolor.replace(" ",""),color.replace(" ",""))
        return True
    else:
        #print("Color diferente.",idcolor.replace(" ",""),color.replace(" ",""))
        return False
    
def cmpIdBackgroundColor(driver,id,color):
    """Retorna True si rgb del fondo de id igual al rgb del 'color'
        @driver : Navegador
        @id     : Id del elemento a revisar.
        @color  : Color con el que comparar, formar str rgb(r,g,b)
    """
    getcolor_js="""
    return getComputedStyle(document.getElementById('"""+id+"""')).getPropertyValue("background-color");
    """
    idcolor=driver.execute_script(getcolor_js)
    #print(idcolor+" = "+ color)
    if idcolor.replace(" ","")==color.replace(" ",""):
        #print("Color Identico.",idcolor.replace(" ",""),color.replace(" ",""))
        return True
    else:
        #print("Color diferente.",idcolor.replace(" ",""),color.replace(" ",""))
        return False

def inputcompare(entrada,ref,cmptype):
    """Retorna True si entrada igual o similar a la referencia.
    @entrada    : Entrada a comparar.
    @ref        : Valor de referencia 
    @cmtype     : Tipo de comparación | 0 => ref contiene la entrada | 1 => ref igual a la entrada
    """
    #print(ststr(ref)+"=="+ststr(entrada))
    if cmptype==0:
        if ststr(ref)==ststr(entrada) or ststr(entrada) in ststr(ref):
            #print(ststr(ref)+"=="+ststr(entrada))
            return True
    elif cmptype==1:
        if ststr(ref)==ststr(entrada):
            return True

    return False
    
#Recibe tres parámetros obligatorios, el driver, el id del select y el elemento del select 
# que se desee seleccionar; retorna True si el procedimiento fue exitoso
#cmptype es el tipo de comparación para seleccionar el elemento, por defecto 0
#cmptype=> 0 para comparación flexible => 1 para comparación exacta
#xpath_sel es el xpath del select, idealmente incluirlo en los argumentos, sobre todo
#si el select posee un clickevent.
#query_sel en caso de que el select form sea construido mediante labels
#Por ahora el query selector debe incluir el '#INDEX#' dentro del selector para recorrer los labels con 
#<<<n n=índice desde el que inicia el recorrido del label
def llenarSelectForm(driver,id_select,entrada,cmptype=0,xpath_sel="",query_sel=""):
    """ Completa el select de un formulario HTML
    @driver     : Navegador
    @id_select  : id del elemento Select.
    @entrada    : Seleccion.
    @cmtype     : Tipo de comparacion | Similar(0) o estricta(1)
    """
    #Recorrer selectform
    i=0
    while True:
        texto_Elemento=None
        try:
            js_textoElementoSF=f"""return $("#{id_select} option")[{i}].innerText;"""
            js_valorElementoSF=f"""return $("#{id_select} option")[{i}].value;"""
            try:
                texto_Elemento=driver.execute_script(js_textoElementoSF)
                valor_Elemento=driver.execute_script(js_valorElementoSF)
            except Exception as catchnt:
                WebDriverWait(driver,60).until(EC.element_to_be_clickable((By.ID,id_select))).click()
                texto_Elemento=driver.execute_script(js_textoElementoSF)
                valor_Elemento=driver.execute_script(js_valorElementoSF)
                
            if inputcompare(entrada,texto_Elemento,cmptype):
                if xpath_sel!="":
                    sel=Select(driver.find_element(By.XPATH,xpath_sel))
                    sel.select_by_value(valor_Elemento)
                    #Como esto está pensado para selects con clickevent dejar un tiempo de carga puede ser bueno
                    time.sleep(2)
                elif query_sel!="":
                    start_index=int(query_sel[query_sel.find('#INDEX:')+7])
                    query_sel=query_sel.replace("#INDEX:"+str(start_index),str(i+start_index))
                    js_querySelector=f"""document.querySelector('{query_sel}').click();"""
                    driver.execute_script(js_querySelector)
                else:
                    try:
                        js_seleccionarElemento=f"""document.getElementById("{id_select}").value={valor_Elemento};"""
                        driver.execute_script(js_seleccionarElemento)
                    except:
                        #CASO DE QUE EL VALUE SEA UN STRING
                        js_seleccionarElemento=f"""document.getElementById("{id_select}").value='{valor_Elemento}';"""
                        driver.execute_script(js_seleccionarElemento)
                
                return True#ÉXITO EN LA SELECCIÓN
        
        except Exception as exc:
            print("Error en xpath:"+id_select)
            print("Probablemente se excedió el límite del select")
            print(exc)
            return False
            
        #Mientras el elemento no esté vacío
        if texto_Elemento==None:
            break

        i+=1
        
        
    return False

#Scrollea hasta el que el elemento sea visible
def scrollFullDown(driver,xpathlmnt={}):
    """Scrollea hasta el final."""
    wait = WebDriverWait(driver, 10)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

def fillField(driver,xpath_arr,entrada_arr,entrada_arr_aux=[],id_arr=[]):
    """Recibe una lista de campos y otra lista de entradas y llena los campos hasta el tamaño de la lista más pequeño
    @driver : Navegador
    @xpath_arr : lista de xpath de los campos
    @entrada_arr :arreglo con las entradas de datos
    @entrada_arr_aux: opcional | entrada auxiliar en caso de error
    """
    current=""
    try:
        curr_id=0
        for entrada,xpath in zip(entrada_arr,xpath_arr):
            current=xpath
            clickable=True
            if id_arr!=[]:
                id=id_arr[curr_id]
                ro_js=f"""return document.getElementById('{id}').getAttribute("readonly");"""
                readonly=driver.execute_script(ro_js)
                if readonly!=None:
                    clickable=False

            if entrada!="" and clickable:
                try:
                    if id_arr==[]:
                        driver.find_element(By.XPATH,xpath).send_keys(entrada)
                    else:
                        driver.find_element(By.ID,id_arr[curr_id]).send_keys(entrada)
                except Exception as excsend:
                    print("Error en sendkeys")
                    print(excsend)
                    try:
                        print("Se necesita conversion decimal")
                        driver.find_element(By.XPATH,xpath).send_keys(getDecimal(entrada))
                    except Exception as excgd:
                            print("Error en getDecimal")
                            print(excgd)
                    
            curr_id+=1
    except:
        try:
            curr_id=0
            for entrada,xpath in zip(entrada_arr_aux,xpath_arr):
                clickable=True
                current=xpath
                if id_arr!=[]:
                    id=id_arr[curr_id]
                    ro_js=f"""return document.getElementById('{id}').getAttribute("readonly");"""
                    readonly=driver.execute_script(ro_js)
                    if readonly!=None:
                        clickable=False
                    
                if entrada!="" and clickable:
                    try:
                        if id_arr==[]:
                            driver.find_element(By.XPATH,xpath).send_keys(entrada)
                        else:
                            driver.find_element(By.ID,id_arr[curr_id]).send_keys(entrada)
                    except Exception as excsend:
                        print("Error en sendkeys : "+excsend)
                        try:
                            print("Se necesita conversion decimal")
                            driver.find_element(By.XPATH,xpath).send_keys(getDecimal(entrada))
                        except Exception as excgd:
                            print("Error en getDecimal : "+excgd)
                curr_id+=1
        except Exception as exc:
            print("Error de contexto en xpath: "+current)
            print(exc)