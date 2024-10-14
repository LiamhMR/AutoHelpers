import pyodbc

# HELPER PARA EXPLORAR UNA DB POR CÓDIGO, PENSADA PARA MICROSOFT SQL SERVER

def getSvList(sv, uid, psw):
    """
    Conecta a un servidor SQL Server y obtiene una lista de bases de datos disponibles.

    :param sv: Dirección del servidor SQL.
    :param uid: Nombre de usuario para la conexión.
    :param psw: Contraseña para la conexión.
    """
    try:
        connectionString = f'DRIVER={{SQL SERVER}};SERVER={sv};UID={uid};PWD={psw}'
        conn = pyodbc.connect(connectionString)
        print("Conectado correctamente")
        cursor = conn.cursor()

        sql_statement = "SELECT name, database_id, create_date FROM sys.databases;"
        for row in cursor.execute(sql_statement):
            print(row.name, row.database_id)

        cursor.close()
        conn.close()
    except ConnectionError as exc:
        print(exc)

def getDBList(sv, uid, pwd, db):
    """
    Devuelve los nombres de todas las tablas en la base de datos especificada.

    :param sv: Dirección del servidor SQL.
    :param uid: Nombre de usuario para la conexión.
    :param pwd: Contraseña para la conexión.
    :param db: Nombre de la base de datos.
    """
    try:
        connectionString = f'DRIVER={{SQL SERVER}};SERVER={sv};UID={uid};DATABASE={db};PWD={pwd};'
        conn = pyodbc.connect(connectionString)
        print("Conectado correctamente")
        cursor = conn.cursor()

        sql_statement = """
                        SELECT table_name, table_schema, table_type
                        FROM information_schema.tables
                        ORDER BY table_name ASC;"""
        for row in cursor.execute(sql_statement):
            print(row.table_name)
        print("Muestreo correcto!")
        cursor.close()
        conn.close()
    except ConnectionError as exc:
        print(exc)

def getTableColumnNames(sv, uid, pwd, db, tb):
    """
    Devuelve los nombres de las columnas de la tabla especificada.

    :param sv: Dirección del servidor SQL.
    :param uid: Nombre de usuario para la conexión.
    :param pwd: Contraseña para la conexión.
    :param db: Nombre de la base de datos.
    :param tb: Nombre de la tabla.
    """
    try:
        connectionString = f'DRIVER={{SQL SERVER}};SERVER={sv};UID={uid};DATABASE={db};PWD={pwd}'
        conn = pyodbc.connect(connectionString)
        print(f"Conectado correctamente a ==> {tb}")
        cursor = conn.cursor()

        sql_statement = f"""
                        SELECT column_name
                        FROM INFORMATION_SCHEMA.COLUMNS
                        WHERE TABLE_NAME = N'{tb}';"""
        for row in cursor.execute(sql_statement):
            print(row.column_name)
        print("Muestreo correcto!")
        cursor.close()
        conn.close()
    except ConnectionError as exc:
        print(exc)

def getTableData(sv, uid, pwd, db, tb, cl, ignorenull=False):
    """
    Obtiene y muestra datos de la tabla especificada, con opción de ignorar valores nulos.

    :param sv: Dirección del servidor SQL.
    :param uid: Nombre de usuario para la conexión.
    :param pwd: Contraseña para la conexión.
    :param db: Nombre de la base de datos.
    :param tb: Nombre de la tabla.
    :param cl: Columnas a seleccionar.
    :param ignorenull: Si es True, ignora filas donde la columna especificada es NULL.
    """
    try:
        connectionString = f'DRIVER={{SQL SERVER}};SERVER={sv};UID={uid};DATABASE={db};PWD={pwd}'
        conn = pyodbc.connect(connectionString)
        print(f"Conectado correctamente a ==> {tb}")
        cursor = conn.cursor()

        if ignorenull == False:
            sql_statement = f"SELECT {cl} FROM {tb}"
        else:
            sql_statement = f"SELECT {cl} FROM {tb} WHERE {ignorenull} IS NOT NULL"

        lineas_count = 0
        for row in cursor.execute(sql_statement):
            print(row)
            lineas_count += 1
        print(f"Muestreo correcto de {lineas_count} elementos")
        cursor.close()
        conn.close()
    except ConnectionError as exc:
        print(exc)

def getQuery(sv, uid, pwd, db, QUERY):
    """
    Ejecuta una consulta SQL proporcionada y muestra los resultados.

    :param sv: Dirección del servidor SQL.
    :param uid: Nombre de usuario para la conexión.
    :param pwd: Contraseña para la conexión.
    :param db: Nombre de la base de datos.
    :param QUERY: Consulta SQL a ejecutar.
    """
    try:
        connectionString = f'DRIVER={{SQL SERVER}};SERVER={sv};UID={uid};DATABASE={db};PWD={pwd}'
        conn = pyodbc.connect(connectionString)
        print("Conectado correctamente")
        cursor = conn.cursor()
        sql_statement = f"{QUERY}"
        
        rowCount = 0
        for row in cursor.execute(sql_statement):
            print(row)
            rowCount += 1
        print(f"{rowCount} Filas")
        print("Muestreo correcto de datos")
        cursor.close()
        conn.close()
    except ConnectionError as exc:
        print(exc)

def updateDb(sv, uid, pwd, db, QUERY):
    """
    Ejecuta una consulta SQL de actualización en la base de datos.

    :param sv: Dirección del servidor SQL.
    :param uid: Nombre de usuario para la conexión.
    :param pwd: Contraseña para la conexión.
    :param db: Nombre de la base de datos.
    :param QUERY: Consulta SQL de actualización a ejecutar.
    """
    try:
        connectionString = f'DRIVER={{SQL SERVER}};SERVER={sv};UID={uid};DATABASE={db};PWD={pwd}'
        conn = pyodbc.connect(connectionString)
        print("Conectado correctamente")
        cursor = conn.cursor()
        sql_statement = f"{QUERY}"

        cursor.execute(sql_statement)
        conn.commit()
        cursor.close()
        conn.close()
    except ConnectionError as exc:
        print(exc)
