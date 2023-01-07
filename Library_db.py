

import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Bismillah"
)

cur = db.cursor()



# create database
cur.execute("CREATE DATABASE IF NOT EXISTS Library")

cur.execute("DROP TABLE IF EXISTS Library.days_record_for_view")

cur.execute("CREATE table IF NOT EXISTS Library.days_record_for_view(book_name char(255), "
            "amount int, sale_price int, total_price int, book_id int AUTO_INCREMENT, PRIMARY KEY(book_id))")

cur.execute("ALTER TABLE Library.days_record_for_view AUTO_INCREMENT = 1")

cur.execute("CREATE DATABASE IF NOT EXISTS client_info")

cur.execute("CREATE TABLE IF NOT EXISTS Library.users(user_name char(75), phone_number char(11),"
            "e_mail char(45), password char(75), remember char(45), PRIMARY KEY(user_name))")

cur.execute("CREATE TABLE IF NOT EXISTS Library.current_user(user_name char(75), PRIMARY KEY(user_name))")


# ================== Create tables ============================
# books table

def create_all_tables():
    cur.execute("CREATE table IF NOT EXISTS Library.books(book_name char(255), category char(75), "
                "author char(100), publisher char(255), book_code char(45), import_price int, "
                "sale_price int, amount int, extra_comment char(255), added_date char(45), "
                "up_dated_date char(45), PRIMARY KEY (book_name))")

    # days record
    cur.execute("CREATE table IF NOT EXISTS Library.days_record_for_sale(book_name char(255), "
                "amount int, sale_price int, total_price int, salesman char(45), date_time char(40), "
                "record_id int AUTO_INCREMENT, PRIMARY KEY(record_id))")

    cur.execute("ALTER TABLE Library.days_record_for_sale AUTO_INCREMENT = 1")

    # days record for view
    cur.execute("CREATE table IF NOT EXISTS Library.days_record_for_view(book_name char(255), "
                "amount int, sale_price int, total_price int, book_id int AUTO_INCREMENT, PRIMARY KEY(book_id))")

    cur.execute("ALTER TABLE Library.days_record_for_view AUTO_INCREMENT = 1")

    # users table
    cur.execute("CREATE TABLE IF NOT EXISTS Library.users(user_name char(75), phone_number char(11),"
                "e_mail char(45), password char(75), remember char(45), PRIMARY KEY(user_name))")

    # client table
    cur.execute("CREATE TABLE IF NOT EXISTS Library.client(client_name char(75), phone_number char(11),"
                "e_mail char(75), address char(255), balance bigint, start_time char(45), "
                "end_time char(45), client_no int AUTO_INCREMENT,"
                "PRIMARY KEY(client_no))")
    cur.execute("ALTER TABLE Library.client AUTO_INCREMENT = 2020")

    # category table
    cur.execute("CREATE TABLE IF NOT EXISTS Library.category(category_name char(75), category_id INT NOT NULL "
                "AUTO_INCREMENT, PRIMARY KEY(category_id))")

    # publisher table
    cur.execute("CREATE TABLE IF NOT EXISTS Library.publisher(publisher_name char(100),"
                "publisher_id INT NOT NULL AUTO_INCREMENT, PRIMARY KEY(publisher_id))")

    # author table
    cur.execute("CREATE TABLE IF NOT EXISTS Library.author(author_name char(75),"
                "author_id INT NOT NULL AUTO_INCREMENT, PRIMARY KEY(author_id))")


# ================== Create tables ============================


# ================== Add info to the tables ============================

def get_columns_list(table_name):
    cur.execute(f"DESCRIBE Library.{table_name}")
    column_list = cur.fetchall()
    column_list = [names[0] for names in column_list]
    return column_list


def get_column_names(table_name):
    column_list = get_columns_list(table_name)
    column_name = ", ".join(column_list)
    return column_name


def get_all_table_data(table_name):
    cur.execute(f"SELECT * FROM Library.{table_name}")
    result = cur.fetchall()
    return result


def search_from_column(table_name, column_name, text):
    cur.execute(f"SELECT * FROM Library.{table_name} WHERE({column_name} = '{text}')")
    result = cur.fetchall()
    return result


def search_from_column_like(table_name, search_from_column, column_name, text):
    cur.execute(f"SELECT {search_from_column} FROM Library.{table_name} WHERE({column_name} LIKE '%{text}%')")
    result = cur.fetchall()
    result = [result[0] for result in result]
    return result


def add_info_one_column_table(table_name, list_of_value, key, column_for_key):
    if key == "" or key.isspace():
        return "empty"
    else:
        cur.execute(f"SELECT {column_for_key} FROM Library.{table_name} WHERE({column_for_key} = '{key}')")
        da_ta = cur.fetchall()
        if not da_ta:
            column_list = get_columns_list(table_name)

            values = ""
            for val_ue in list_of_value:
                values = values + "'" + val_ue + "', "
            values = values[:-2]

            cur.execute(f"INSERT INTO Library.{table_name}({column_list[0]})VALUES({values})")
            db.commit()
            return "added"
        else:
            return "exist"


def add_info(table_name, list_of_value, key, column_for_key):
    data = search_from_column(table_name, column_for_key, key)
    if not data:
        column_names = get_column_names(table_name)
        values = ""
        for val_ue in list_of_value:
            values = values + "'" + str(val_ue) + "', "
        values = values[:-2]
        cur.execute(f"INSERT INTO Library.{table_name}({column_names})VALUES({values})")
        db.commit()
        return "added"
    else:
        return "exist"


def add_books_to_table(table_name, list_of_value):
    column_names = get_column_names(table_name)
    values = ""
    for val_ue in list_of_value:
        values = values + "'" + str(val_ue) + "', "
    values = values[:-2]
    cur.execute(f"INSERT INTO Library.{table_name}({column_names})VALUES({values})")
    db.commit()


def add_info_to_table(table_name, list_of_value):
    column_names = get_column_names(table_name)
    values = ""
    for val_ue in list_of_value:
        values = values + "'" + str(val_ue) + "', "
    values = values[:-2]
    cur.execute(f"INSERT INTO Library.{table_name}({column_names})VALUES({values})")
    db.commit()
    return "added"


def up_date_table_info(table_name, values, key_column, key_value):
    column_names = get_columns_list(table_name)
    for new_name, new_value in zip(column_names, values):
        cur.execute(f"UPDATE Library.{table_name}"
                               f" SET {new_name} = '{new_value}'"
                               f"WHERE({key_column} = '{key_value}')")
        db.commit()


def check_user(table_name, user_name):
    cur.execute(f"SELECT * FROM Library.{table_name} WHERE (user_name = '{user_name}')")
    res_ult = cur.fetchall()
    return res_ult


db.commit()
