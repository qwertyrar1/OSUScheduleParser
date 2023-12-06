import psycopg2
from db_config import host, user, password, db_name, States


def get_group_number(faculty, group_class, group_name):
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(f"""
        SELECT number FROM groups WHERE faculty = '{faculty}' AND class = '{group_class}' AND name = '{group_name}';
        """)
    received_num = cursor.fetchone()[0]
    if connection:
        connection.close()
        cursor.close()
    return received_num


def get_group_name_from_db(faculty, group_class):
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(f"""
            SELECT name FROM groups WHERE faculty = '{faculty}' AND class = '{group_class}';
            """)
    received_names = cursor.fetchall()
    if connection:
        connection.close()
        cursor.close()
    return received_names


def create_state(user_id, value):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(f"""
                    INSERT INTO users VALUES ({user_id}, {value});
                    """)
        if connection:
            connection.close()
            cursor.close()
        return True
    except:
        return False


def update_state(user_id, value):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(f"""
                    UPDATE users SET status_code = {value} WHERE id = {user_id};
                    """)
        if connection:
            connection.close()
            cursor.close()
        return True
    except:
        return False


def get_current_state(user_id):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(f"""
                        SELECT status_code FROM users WHERE id = {user_id};
                        """)
        received_names = cursor.fetchone()
        if connection:
            connection.close()
            cursor.close()
        return received_names[0]
    except TypeError:
        return States.S_START.value
