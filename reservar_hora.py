import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import find_dotenv, load_dotenv
import re

def conectarDatabase() :

    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)

    
    conn = None
    cur = None

    try : 
        conn = psycopg2.connect(host = os.getenv("HOST"),
                                dbname = "salon",
                                user = os.getenv("USER"),
                                password = os.getenv("PASSWORD"),
                                port = os.getenv("PORT"))
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        print("La conexión a la base de datos salon se ha realizado con exito!")
        return conn, cur

    except psycopg2.OperationalError : 
        sys.exit("Ha ocurrido un error en la conexión")


def main() :
    

    conn, cur =  conectarDatabase()
    print("~~~~~ MY SALON ~~~~~")
    print("Welcome to My Salon, how can I help you?")
    aux = True

    while (aux == True) :
        cur.execute("""SELECT * FROM services;""")
        for service in cur.fetchall() : 
            print(f"{service[0]}) {service[1]}")
        print("\nEnter number of service you want : ")
        serviceIdSelected = input()
        if (re.search("^[1-5]+$",serviceIdSelected) == None) :
            print("\nI could not find that service. What would you like today? : ")
        else : 
            aux = False

    aux = True
    print("\nWhat is your phone number? (8-digit) : ")
    while (aux == True) :
        customerPhone = str(input()) #conversion a string por si necesitaba guiones en el numero
        if (re.search("^[0-9]{8}$",customerPhone) == None) :
            print("\nIncorrect number format, make sure you enter an 8-digit number : ")
        else : 
            aux = False

    cur.execute(f"""SELECT customer_id FROM customers WHERE phone = '{customerPhone}'""")
    aux = True
    if (cur.fetchall() == []) :
        print("\nI don't have a record for that phone number, what's your name? : ")
        while (aux == True) :
            customerName = input()
            if (re.search("^\D+$",customerName) == None) :
                print("\nIncorrect name format, make sure you enter only non digit characters : ")
            else : 
                aux = False
        cur.execute(f"""INSERT INTO customers(name,phone) VALUES('{customerName}','{customerPhone}')""")
    
    cur.execute(f"""SELECT customer_id FROM customers WHERE phone = '{customerPhone}'""")
    customerId = cur.fetchall()[0][0]
    cur.execute(f"""SELECT name FROM services WHERE service_id='{serviceIdSelected}'""")
    serviceName = cur.fetchall()[0][0]
    cur.execute(f"""SELECT name FROM customers WHERE phone = '{customerPhone}'""")
    customerName = cur.fetchall()[0][0]
    aux= True
    print(f"\nWhat time would you like your {serviceName}, {customerName}? (Between 10 AM to 19 PM)")
    while (aux == True) : 
        serviceTime = input()
        if (re.search("^1[0-9]$",serviceTime) == None) :
            print("\nIncorrect range or format, Enter an integer number from 10 to 19 : ")
        else : 
             aux = False
    cur.execute(f"""INSERT INTO appointments(customer_id,service_id,time) VALUES('{customerId}','{serviceIdSelected}','{serviceTime}')""")
    print(f"\nI have put you down for a {serviceName} at {serviceTime}, {customerName}")
    conn.close()
    cur.close()


if __name__ == "__main__":
    main()
