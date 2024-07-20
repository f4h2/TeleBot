import psycopg2
import psycopg2.extras

hostname = 'localhost'
database = 'Telegram_2002'
username = 'postgres'
pwd = '12345678'
port_id = 5432

def get_db_connection():
    return psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=pwd,
        port=port_id
    )

def create_table_message():
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            create_table_script = '''
                CREATE TABLE IF NOT EXISTS messageTele (
                    id SERIAL PRIMARY KEY,
                    message_id BIGINT NOT NULL,
                    sender_id BIGINT NOT NULL,
                    name_sender TEXT,
                    content_message TEXT,
                    tele_message TEXT,
                    date TIMESTAMP
                )
            '''
            cur.execute(create_table_script)
        conn.commit()
    except Exception as error:
        print(f"Error creating table: {error}")
    finally:
        if conn is not None:
            conn.close()

def save_message_to_db_message(message_id, sender_id, name_sender, content_message, tele_message, date):
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            insert_script = '''
                INSERT INTO messageTele (message_id, sender_id, name_sender, content_message, tele_message, date)
                VALUES (%s, %s, %s, %s, %s, %s)
            '''
            cur.execute(insert_script, (message_id, sender_id, name_sender, content_message, tele_message, date))
        conn.commit()
    except Exception as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def create_table_user():
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            create_table_script = '''
                CREATE TABLE IF NOT EXISTS InfoUser (
                    id SERIAL PRIMARY KEY,
                    first_name text NOT NULL,
                    last_name text NOT NULL
                )
            '''
            cur.execute(create_table_script)
        conn.commit()
    except Exception as error:
        print(f"Error creating table: {error}")
    finally:
        if conn is not None:
            conn.close()

def user_exists(first_name, last_name):
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            select_script = '''
                SELECT * FROM InfoUser
                WHERE first_name = %s AND last_name = %s
            '''
            cur.execute(select_script, (first_name, last_name))
            user = cur.fetchone()
            return user is not None
    except Exception as error:
        print(error)
        return False
    finally:
        if conn is not None:
            conn.close()

def save_user_to_db(first_name, last_name):
    if user_exists(first_name, last_name):
        print(f"User {first_name} {last_name} already exists.")
        return
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            insert_script = '''
                INSERT INTO InfoUser (first_name, last_name)
                VALUES (%s, %s)
            '''
            cur.execute(insert_script, (first_name, last_name))
        conn.commit()
    except Exception as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
