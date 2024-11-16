import pandas as pd
import oracledb
import os
from dotenv import load_dotenv
load_dotenv()
oracle_admin_password = os.environ['oracle_admin_password']
oracle_db_dsn = os.environ['oracle_db_dsn']
oracle_cert_path = os.environ['oracle_cert_path']

def create_connection(config_dir, user, password, dsn, wallet_dir, wallet_password):
     return oracledb.connect(config_dir=config_dir, user=user, password=password, dsn=dsn, wallet_location=wallet_dir, wallet_password=wallet_password)

def create_cursor(connection):
     return connection.cursor()

def get_table(table_name:str, cursor):
     query = f"""
     SELECT *
     FROM {table_name}
     """
     cursor.execute(query)
     rows = cursor.fetchall()
     columns = [col[0] for col in cursor.description]
     return pd.DataFrame(rows, columns=columns)

def get_conversation_messages(table_name:str, conversation_id:str, cursor):
     query = f"""
     SELECT *
     FROM {table_name}
     WHERE CONVERSATION_ID = '{conversation_id}'
     """
     cursor.execute(query)
     rows = cursor.fetchall()



if __name__=="__main__":
     connection=oracledb.connect(
          config_dir=oracle_cert_path,
          user="ADMIN",
          password=oracle_admin_password,
          dsn=oracle_db_dsn,
          wallet_location=oracle_cert_path,
          wallet_password=oracle_admin_password)

     # Create a cursor to execute a query
     cursor = connection.cursor()

     # Query to fetch messages table
     query = """
     SELECT *
     FROM messages
     where conversation_id = 'A'
     """

     # Execute the query
     cursor.execute(query)

     # Fetch and display the rows
     rows = cursor.fetchall()
     for row in rows:
          print(row)
     print(rows)

     cursor.close()
     connection.close()