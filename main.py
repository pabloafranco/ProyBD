import pymysql
# Tengo que instalar esto pip install python-decouple 
from decouple import config

if __name__  == '__main__':
    
    connect = pymysql.Connect(host='localhost', 
                                  port=3306, 
                                  user=config('USER_MYSQL'), 
                                  passwd=config('PASWORD_MYSQL'), 
                                  db=config('DB_MYSQL'))


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