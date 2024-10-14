import pyodbc

#LIBRERÍA PARA EXPLORAR LA BASE DE DATOS POR CÓDIGO

def getSvList(sv,uid,psw):
    try:
        connectionString = f'DRIVER={{SQL SERVER}};SERVER={sv};UID={uid};PWD={psw}'
        conn = pyodbc.connect(connectionString)
        print("Conectado correctamente")
        cursor=conn.cursor()
        
        sql_statement=f"SELECT name, database_id, create_date FROM sys.databases;"
        for row in cursor.execute(sql_statement):
            print(row.name,row.database_id,)
            
        cursor.close()
        conn.close()
    except ConnectionError as exc:
        print(exc)

#Devuelve los nombres de todas las tablas en la base de datos señalada
def getDBList(sv,uid,pwd,db):
    try:
        connectionString = f'DRIVER={{SQL SERVER}};SERVER={sv};UID={uid};DATABASE={db};PWD={pwd};'
        conn = pyodbc.connect(connectionString)
        print("Conectado correctamente")
        cursor=conn.cursor()
        sql_statement=f"""
                        SELECT table_name, table_schema, table_type
                        FROM information_schema.tables
                        ORDER BY table_name ASC;"""
        for row in cursor.execute(sql_statement):
            print(row.table_name)
        print("Mustreo correcto!")
        cursor.close()
        conn.close()
    except ConnectionError as exc:
        print(exc)
        
#Devuelve los nombres de todas las tablas en la base de datos señalada
def getTableColumnNames(sv,uid,pwd,db,tb):
    try:
        connectionString = f'DRIVER={{SQL SERVER}};SERVER={sv};UID={uid};DATABASE={db};PWD={pwd}'
        conn = pyodbc.connect(connectionString)
        print("Conectado correctamente a ==>>"+tb)
        cursor=conn.cursor()
        sql_statement=f"""
                        SELECT column_name
                        FROM INFORMATION_SCHEMA.COLUMNS
                        WHERE TABLE_NAME = N'{tb}';"""
        for row in cursor.execute(sql_statement):
            print(row.column_name)
        print("Mustreo correcto!")
        cursor.close()
        conn.close()
    except ConnectionError as exc:
        print(exc)
        
def getTableData(sv,uid,pwd,db,tb,cl,ignorenull=False):
    try:
        connectionString = f'DRIVER={{SQL SERVER}};SERVER={sv};UID={uid};DATABASE={db};PWD={pwd}'
        conn = pyodbc.connect(connectionString)
        print("Conectado correctamente a ==>>"+ tb)
        cursor=conn.cursor()
        
        if ignorenull==False:
            sql_statement=f"""
                            SELECT {cl}
                            FROM {tb}"""
        else:
            sql_statement=f"""
                            SELECT {cl}
                            FROM {tb}
                            WHERE {ignorenull} IS NOT NULL"""
                            
        lineas_count=0
        for row in cursor.execute(sql_statement):
            print(row)
            lineas_count+=1
        print("MUESTREO CORRECTO DE "+str(lineas_count)+" elementos")
        cursor.close()
        conn.close()
    except ConnectionError as exc:
        print(exc)

def getQuery(sv,uid,pwd,db,QUERY):
    try:
        connectionString = f'DRIVER={{SQL SERVER}};SERVER={sv};UID={uid};DATABASE={db};PWD={pwd}'
        conn = pyodbc.connect(connectionString)
        print("Conectado correctamente")
        cursor=conn.cursor()
        sql_statement=f"""
                        {QUERY}"""
        rowCount=0
        for row in cursor.execute(sql_statement):
            print(row)
            rowCount+=1
        print(rowCount," Filas")
        print("Muestreo correcto de datos")
        cursor.close()
        conn.close()
    except ConnectionError as exc:
        print(exc)

def updateDb(sv,uid,pwd,db,QUERY):
    try:
        connectionString = f'DRIVER={{SQL SERVER}};SERVER={sv};UID={uid};DATABASE={db};PWD={pwd}'
        conn = pyodbc.connect(connectionString)
        print("Conectado correctamente")
        cursor=conn.cursor()
        sql_statement=f"""
                        {QUERY}"""
        
        cursor.execute(sql_statement)
        conn.commit()
        cursor.close()
        conn.close()
    except ConnectionError as exc:
        print(exc)