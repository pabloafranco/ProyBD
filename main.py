import os
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

def system_clear(function):
    def wrapper(connect, cursor):

        os.system("cls")

        function(connect, cursor)

        input("")

        os.system("cls")

    wrapper.__doc__ = function.__doc__
    return wrapper

@system_clear
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

@system_clear
def list_users(connect, cursor):
    """B) Listar Usarios """

    query = "Select id, username, email from USERS"
    cursor.execute(query)

    for id, username, email in cursor.fetchall():
        print (id, '-', username, '-', email)

    print ("Listado de Usuarios")
    
def user_exists(function):

    def wrapper(connect, cursor):
        id=input("Ingrese el id Usuario a actualizar: ")
        query = "Select id, username, email from USERS where id = %s"
        cursor.execute(query, (id,))

        user =cursor.fetchone()
        if user:
            function(id, connect, cursor)
        else:
            print ("No existe un usuario con ese id, intenta nuevaemtente")    

    wrapper.__doc__ = function.__doc__
    return wrapper

@system_clear
@user_exists
def update_users(id, connect, cursor):
    """C) Actualizar Usario """
   
    username=input("Ingresa un nuevo username: ")
    email=input("Ingresa un nuevo email: ")
    
    query="UPDATE  users SET username = %s, email = %s WHERE id =  %s "
    #creo una tupla de valores
    values=(username, email, id)

    cursor.execute(query, values)
    connect.commit()
        
    print (">>> Usuario Actualizado exitosamente!")
    
@system_clear    
@user_exists
def delete_users(id, connect, cursor):
    """D) Eliminar Usario """

    query = "Delete from users where id = %s"
    cursor.execute(query, (id,))
    connect.commit()

    print (">>> Usuario eliminado exitosamente!")

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
