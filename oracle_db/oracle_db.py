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

def get_table(table_name:str, connection):
     query = f"""
     SELECT *
     FROM {table_name}
     """
     with connection.cursor() as cursor:
          cursor.execute(query)
          rows = cursor.fetchall()
          rows = [(row[0],row[1],row[2],row[3],row[4].read()) for row in rows] #convert oracle lob message to string
          columns = [col[0] for col in cursor.description]
     return pd.DataFrame(rows, columns=columns).sort_values(['MESSAGE_TIME'])

def get_conversation_messages(table_name:str, conversation_id:str, connection):
     query = f"""
     SELECT *
     FROM {table_name}
     WHERE CONVERSATION_ID = '{conversation_id}'
     """
     with connection.cursor() as cursor:
          cursor.execute(query)
          rows = cursor.fetchall()
     return [row[4].read() for row in rows]

def write_conversation_message(table_name:str, conversation_id:str, message_sender:str, message:str, connection):
     query = f"""
     INSERT INTO {table_name} (conversation_id, sender_name, message_text)
     VALUES (:conversation_id, :sender_name, :message_text)
     """
     try:
          with connection.cursor() as cursor:
               cursor.execute(query, {
                    'conversation_id':conversation_id, 
                    'sender_name':message_sender, 
                    'message_text':message
                    })
               connection.commit()
          return "Success"
     except Exception as error:
          return f"{error}"

def delete_conversation(table_name:str, conversation_id:str, connection):
     query = f"""
     DELETE FROM {table_name}
     WHERE CONVERSATION_ID = '{conversation_id}'
     """
     try:
          with connection.cursor() as cursor:
               cursor.execute(query)
               connection.commit()
          return "Success"
     except Exception as error:
          return f"{error}"

if __name__=="__main__":
     connection = create_connection(
          config_dir=oracle_cert_path,
          user="ADMIN",
          password=oracle_admin_password,
          dsn=oracle_db_dsn,
          wallet_dir=oracle_cert_path,
          wallet_password=oracle_admin_password
     )

     messages_df = get_table(table_name="MESSAGES", connection=connection)

     write_conversation_message(
          table_name="MESSAGES",
          conversation_id="A",
          message_sender="USER",
          message="Tell me a joke please!",
          connection=connection
     )

     delete_conversation(
          table_name="MESSAGES",
          conversation_id="A",
          connection=connection
     )

     curr_df = get_table(
          table_name="MESSAGES",
          connection=connection
     )

     connection.close()