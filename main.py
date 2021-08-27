import pymysql
# Tengo que instalar esto pip install python-decouple 
from decouple import config

DROP_USERS_TABLE = """DROP TABLE IF EXISTS users"""

USERS_TABLE = """CREATE TABLE users(
    id INT UNSIGNED AUTO_INCREMENT  PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email  VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

"""

def  create_user(connect, cursor):
    """A) Crear Usario """

    
    username=input("Ingresa un username: ")
    email=input("Ingresa un email: ")
    
    query="INSERT INTO users( username, email ) values ( %s, %s ) "
    #creo una tupla de valores
    values=(username, email)

    cursor.execute(query, values)
    connect.commit()
    

    print (">>> Usuario Creado")

def list_users(connect, cursor):
    """B) Listar Usarios """

    query = "Select id, username, email from USERS"
    cursor.execute(query)

    for id, username, email in cursor.fetchall():
        print (id, '-', username, '-', email)

    print ("Listado de Usuarios")
    

def update_users(connect, cursor):
    """C) Actualizar Usario """

    print ("Usuario Actualizado")
    pass

def delete_users(connect, cursor):
    """D) Eliminar Usario """

    print ("Usuario Eliminado")
    pass

def default(*args):
    print ("Opcion no valida")

if __name__  == '__main__':
    
    options = {
        'a': create_user,
        'b': list_users,
        'c': update_users,
        'd': delete_users
    }

    try:
        #print (config('DB_MYSQNEW'))
        connect = pymysql.Connect(host='localhost', 
                                  port=3306, 
                                  user=config('USER_MYSQL'), 
                                  passwd=config('PASWORD_MYSQL'), 
                                  db=config('DB_MYSQNEW'))
        with connect.cursor() as cursor:
            #cursor.execute(DROP_USERS_TABLE)
            #cursor.execute(USERS_TABLE)

            while True:

                for function in options.values():
                    #Lista los comentarios de la funcion!!!!
                    print(function.__doc__)

                print ("quit para salir")

                option = input("Selecciona una opción válida:").lower()

                if option == "quit" or option=="q":
                    break

                function = options.get(option, default)
                function(connect, cursor)

        connect.close

    except pymysql.err.OperationalError as err:
        print ('No fue posible hacer la conexion')
        print (err)


    """"
    # prepare a cursor object using cursor() method
    cursor = connect.cursor()

    # ejecuta el SQL query usando el metodo execute().
    cursor.execute("SELECT VERSION()")

    # procesa una unica linea usando el metodo fetchone().
    data = cursor.fetchone()
    print ("Database version : {0}".format(data))

    # desconecta del servidor
    connect.close()
    """
