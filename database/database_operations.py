import pandas as pd
import mysql.connector
from mysql.connector import Error

def create_connection(host, database, user, password):
    """Cria conexão com o banco de dados"""
    try:
        conn = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        return conn
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

def execute_sql_file(conn, file_path):
    """Executa um arquivo SQL"""
    try:
        cursor = conn.cursor()
        
        with open(file_path, 'r') as sql_file:
            sql_commands = sql_file.read().split(';')
            
            for command in sql_commands:
                if command.strip():
                    cursor.execute(command)
        
        conn.commit()
        cursor.close()
    except Error as e:
        print(f"Erro ao executar arquivo SQL: {e}")

def import_csv_to_table(conn, csv_path, table_name):
    """Importa dados de CSV para tabela"""
    try:
        df = pd.read_csv(csv_path)
        cursor = conn.cursor()
        
        for _, row in df.iterrows():
            # Construir query de inserção dinâmica
            columns = ', '.join(row.index)
            placeholders = ', '.join(['%s'] * len(row))
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            
            cursor.execute(query, tuple(row))
        
        conn.commit()
        cursor.close()
    except Error as e:
        print(f"Erro ao importar CSV: {e}")