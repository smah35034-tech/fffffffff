import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

class Database():
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            self.cursor = self.connection.cursor()
            return True
        except Error as e:
            print(f"Ошибка подключения к MySQL: {e}")
            return False

    def disconnect(self):
        if self.connection:
            self.connection.close()
    def authenticate_user(self, login, password):
        try:
            query = """
                SELECT role, full_name
                FROM users
                WHERE login = %s and password = %s
            """
            print(login , password)
            self.cursor.execute(query, (login, password))
            return self.cursor.fetchall()
        except Error:
            return None


    def create_user(self, login, password):
        try:
            query = """
                       INSERT INTO users (login , password , role) VALUES
                       (%s , %s , %s)
                   """
            print(login, password)
            self.cursor.execute(query, (login, password , "Авторизированный клиент"))
            self.connection.commit()
            return True
        except Error:
            return False
    def give_items(self):
        try:
            query = """
                    SELECT full_name,price, quantity, photo_path , unit_m , send_by , discount 
                    FROM tovar
                """
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error:
            return None

    def give_items_sort(self , find_word):
        try:
            query = f"""
                    SELECTSELECT full_name,price, quantity, photo_path , unit_m , send_by , discount 
                    FROM tovar
                    where full_name LIKE '%{find_word}%'
                """
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(e)
            return None

    def take_custom_query(self , query , state = "W"):
        try:
            self.cursor.execute(query)
            if state == "READ":
                return self.cursor.fetchall()
            else:
                self.connection.commit()
                return True
        except Exception as e:
            if state == "READ":
                print(e)
                return None
            else:
                return False
