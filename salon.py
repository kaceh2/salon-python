import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import find_dotenv, load_dotenv
import sys



dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

conn = None
cur = None

try : 
    conn = psycopg2.connect(host = os.getenv("HOST"),
                            dbname = "postgres",
                            user = os.getenv("USER"),
                            password = os.getenv("PASSWORD"),
                            port = os.getenv("PORT"))

    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    print("La conexión a la base de datos postgres se ha realizado con exito!")
except psycopg2.OperationalError : 
    sys.exit("Ha ocurrido un error en la conexión")
    

#acciones a realizar

try : 
    cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier("salon")))
    print("Se ha creado la base de datos salon.")

except psycopg2.errors.DuplicateDatabase :
    print("La base de datos salon ya existe")

finally : 
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()
        print("Se ha cerrado la conexión a la base de datos con exito.")

#Se conecta a la base de datos salon
try : 
    conn = psycopg2.connect(host = os.getenv("HOST"),
                            dbname = "salon",
                            user = os.getenv("USER"),
                            password = os.getenv("PASSWORD"),
                            port = os.getenv("PORT"))

    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    print("La conexión a la base de datos salon se ha realizado con exito!")

except psycopg2.OperationalError : 
    sys.exit("Ha ocurrido un error en la conexión")

#acciones a realizar

#Crear tablas
cur.execute("""CREATE TABLE IF NOT EXISTS customers()""")
cur.execute("""CREATE TABLE IF NOT EXISTS appointments()""")
cur.execute("""CREATE TABLE IF NOT EXISTS services()""")

#Crear claves primarias de tablas

cur.execute("""ALTER TABLE customers ADD COLUMN IF NOT EXISTS customer_id SERIAL PRIMARY KEY""")
cur.execute("""ALTER TABLE appointments ADD COLUMN IF NOT EXISTS appointment_id SERIAL PRIMARY KEY""")
cur.execute("""ALTER TABLE services ADD COLUMN IF NOT EXISTS service_id SERIAL PRIMARY KEY""")

#Crear campos restantes

cur.execute("""ALTER TABLE customers ADD COLUMN IF NOT EXISTS phone VARCHAR(30) UNIQUE""")
cur.execute("""ALTER TABLE customers ADD COLUMN IF NOT EXISTS name VARCHAR(30)""")
cur.execute("""ALTER TABLE services ADD COLUMN IF NOT EXISTS name VARCHAR(30)""")
cur.execute("""ALTER TABLE appointments ADD COLUMN IF NOT EXISTS time VARCHAR(30)""")
cur.execute("""ALTER TABLE appointments ADD COLUMN IF NOT EXISTS customer_id INTEGER""")
cur.execute("""ALTER TABLE appointments ADD COLUMN IF NOT EXISTS service_id INTEGER""")

#Añadir claves foraneas
try :
    cur.execute("""ALTER TABLE appointments ADD CONSTRAINT fk_customer  FOREIGN KEY (customer_id) REFERENCES customers (customer_id)""")
    cur.execute("""ALTER TABLE appointments ADD CONSTRAINT fk_service FOREIGN KEY (service_id) REFERENCES services (service_id)""")

except psycopg2.errors.DuplicateObject :
    print("Las llaves foraneas fk_customer y fk_service ya existen")

cur.execute("""SELECT * FROM services""")
if (cur.fetchall() == []) : 
    cur.execute("""INSERT INTO services(name) VALUES ('cut')""")
    cur.execute("""INSERT INTO services(name) VALUES ('color')""")
    cur.execute("""INSERT INTO services(name) VALUES ('perm')""")
    cur.execute("""INSERT INTO services(name) VALUES ('style')""")
    cur.execute("""INSERT INTO services(name) VALUES ('trim')""")



cur.close()
conn.close()
print("Se ha cerrado la conexión a la base de datos con exito.")