import pymysql
# Tengo que instalar esto pip install python-decouple 
from decouple import config

USERS_TABLE = """CREATE TABLE users(
    id INT UNSIGNED AUTO_INCREMENT  PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email  VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

"""

if __name__  == '__main__':
    
    try:
        print (config('DB_MYSQL'))
        connect = pymysql.Connect(host='localhost', 
                                  port=3306, 
                                  user=config('USER_MYSQL'), 
                                  passwd=config('PASWORD_MYSQL'), 
                                  db=config('DB_MYSQL'))
        with connect.cursor() as cursor:

            cursor.execute(USERS_TABLE)

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
